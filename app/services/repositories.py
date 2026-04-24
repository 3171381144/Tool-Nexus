import html
import os
import re
import shutil
import uuid
import zipfile
from pathlib import Path

from fastapi import HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import CodeRepository, RepositoryAccess, User
from app.schemas import (
    RepositoryAccessUpdateRequest,
    RepositoryFileEntryOut,
    RepositoryOut,
    RepositoryReadmeOut,
    RepositoryUpdateRequest,
    SimpleMessageResponse,
    UserOut,
)


README_CANDIDATES = {"readme.md", "readme.markdown", "readme.txt", "readme.rst"}
INLINE_CODE_RE = re.compile(r"`([^`]+)`")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^\s)]+)\)")
STRONG_RE = re.compile(r"\*\*([^*]+)\*\*")
EM_RE = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")
ORDERED_RE = re.compile(r"\d+\.\s+")


def ensure_repository_storage() -> None:
    Path(settings.repository_storage_dir).mkdir(parents=True, exist_ok=True)


def repository_storage_path(storage_key: str) -> Path:
    return Path(settings.repository_storage_dir) / storage_key


def delete_repository_storage(storage_key: str) -> None:
    path = repository_storage_path(storage_key)
    if path.exists():
        shutil.rmtree(path, ignore_errors=True)


def _display_name(user: User) -> str:
    return user.nickname or user.username


def _user_out(user: User) -> UserOut:
    return UserOut(id=user.id, username=user.username, nickname=_display_name(user), is_admin=user.is_admin)


def _repository_out(repository: CodeRepository, access_type: str) -> RepositoryOut:
    granted_users = [_user_out(access.user) for access in repository.granted_users]
    return RepositoryOut(
        id=repository.id,
        name=repository.name,
        description=repository.description or "",
        is_private=repository.is_private,
        owner_id=repository.owner_id,
        owner_username=repository.owner.username,
        owner_nickname=_display_name(repository.owner),
        access_type=access_type,
        archive_name=repository.archive_name or "",
        readme_path=repository.readme_path or "",
        granted_users=granted_users,
    )


def _validate_whitelist_user_ids(db: Session, owner: User, whitelist_user_ids: list[int]) -> list[User]:
    deduped_ids = sorted({user_id for user_id in whitelist_user_ids if user_id != owner.id})
    if not deduped_ids:
        return []

    users = db.scalars(select(User).where(User.id.in_(deduped_ids))).all()
    found_ids = {user.id for user in users}
    missing_ids = [user_id for user_id in deduped_ids if user_id not in found_ids]
    if missing_ids:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Users not found: {missing_ids}")
    return users


def _can_manage_repository(user: User, repository: CodeRepository) -> bool:
    return user.is_admin or repository.owner_id == user.id


def authorize_repository_access(db: Session, user: User, repository: CodeRepository) -> str:
    if repository.owner_id == user.id:
        return "owner"

    if not repository.is_private:
        return "public"

    access_row = db.scalar(
        select(RepositoryAccess).where(
            RepositoryAccess.repository_id == repository.id,
            RepositoryAccess.user_id == user.id,
        )
    )
    if access_row:
        return "shared"

    if user.is_admin:
        return "admin"

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission for this repository")


def list_accessible_repositories(db: Session, user: User) -> list[RepositoryOut]:
    repositories_by_id: dict[int, RepositoryOut] = {}

    owned_repositories = db.scalars(select(CodeRepository).where(CodeRepository.owner_id == user.id)).all()
    for repository in owned_repositories:
        repositories_by_id[repository.id] = _repository_out(repository, "owner")

    public_repositories = db.scalars(
        select(CodeRepository).where(CodeRepository.is_private.is_(False), CodeRepository.owner_id != user.id)
    ).all()
    for repository in public_repositories:
        repositories_by_id.setdefault(repository.id, _repository_out(repository, "public"))

    shared_repositories = db.scalars(
        select(CodeRepository)
        .join(RepositoryAccess, RepositoryAccess.repository_id == CodeRepository.id)
        .where(RepositoryAccess.user_id == user.id, CodeRepository.owner_id != user.id)
    ).all()
    for repository in shared_repositories:
        repositories_by_id[repository.id] = _repository_out(repository, "shared")

    if user.is_admin:
        all_repositories = db.scalars(select(CodeRepository)).all()
        for repository in all_repositories:
            repositories_by_id.setdefault(repository.id, _repository_out(repository, "admin"))

    return sorted(repositories_by_id.values(), key=lambda item: (item.access_type, item.name.lower()))


def _normalize_repository_name(name: str) -> str:
    normalized = name.strip()
    if not normalized:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Repository name cannot be empty")
    if len(normalized) > 128:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Repository name is too long")
    return normalized


def _normalize_description(description: str | None) -> str:
    return (description or "").strip()


def _extract_archive(archive_path: Path, extract_dir: Path) -> None:
    if extract_dir.exists():
        shutil.rmtree(extract_dir)
    extract_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(archive_path) as archive:
        for member in archive.infolist():
            member_path = extract_dir / member.filename
            resolved_path = member_path.resolve()
            if extract_dir.resolve() not in resolved_path.parents and resolved_path != extract_dir.resolve():
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Archive contains invalid paths")
        archive.extractall(extract_dir)


def _resolve_repository_root(extract_dir: Path) -> Path:
    current = extract_dir
    for _ in range(4):
        children = [child for child in current.iterdir() if child.name not in {"__MACOSX"}]
        files = [child for child in children if child.is_file()]
        directories = [child for child in children if child.is_dir()]
        if files or len(directories) != 1:
            return current
        current = directories[0]
    return current


def _find_readme_path(repository_root: Path) -> str:
    matches: list[tuple[int, str]] = []
    for path in repository_root.rglob("*"):
        if not path.is_file():
            continue
        relative_path = path.relative_to(repository_root).as_posix()
        if path.name.lower() in README_CANDIDATES:
            matches.append((relative_path.count("/"), relative_path))
    if not matches:
        return ""
    matches.sort(key=lambda item: (item[0], item[1].lower()))
    return matches[0][1]


def _apply_inline_markdown(text: str) -> str:
    escaped = html.escape(text)
    escaped = LINK_RE.sub(lambda match: f'<a href="{html.escape(match.group(2), quote=True)}" target="_blank" rel="noreferrer">{match.group(1)}</a>', escaped)
    escaped = INLINE_CODE_RE.sub(lambda match: f"<code>{match.group(1)}</code>", escaped)
    escaped = STRONG_RE.sub(lambda match: f"<strong>{match.group(1)}</strong>", escaped)
    escaped = EM_RE.sub(lambda match: f"<em>{match.group(1)}</em>", escaped)
    return escaped


def _render_markdown(markdown_text: str) -> str:
    if not markdown_text.strip():
        return "<p class=\"repo-empty\">README is empty.</p>"

    html_parts: list[str] = []
    paragraph_lines: list[str] = []
    list_items: list[str] = []
    list_kind: str | None = None
    in_code_block = False
    code_lines: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph_lines
        if paragraph_lines:
            html_parts.append(f"<p>{_apply_inline_markdown(' '.join(paragraph_lines))}</p>")
            paragraph_lines = []

    def flush_list() -> None:
        nonlocal list_items, list_kind
        if list_items and list_kind:
            html_parts.append(f"<{list_kind}>" + "".join(list_items) + f"</{list_kind}>")
        list_items = []
        list_kind = None

    for raw_line in markdown_text.splitlines():
        line = raw_line.rstrip("\n")
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_paragraph()
            flush_list()
            if in_code_block:
                html_parts.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")
                code_lines = []
                in_code_block = False
            else:
                in_code_block = True
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        if not stripped:
            flush_paragraph()
            flush_list()
            continue

        if stripped.startswith("#"):
            flush_paragraph()
            flush_list()
            heading_level = min(6, len(stripped) - len(stripped.lstrip("#")))
            heading_text = stripped[heading_level:].strip()
            html_parts.append(f"<h{heading_level}>{_apply_inline_markdown(heading_text)}</h{heading_level}>")
            continue

        if stripped.startswith("> "):
            flush_paragraph()
            flush_list()
            html_parts.append(f"<blockquote>{_apply_inline_markdown(stripped[2:].strip())}</blockquote>")
            continue

        if stripped.startswith(("- ", "* ")):
            flush_paragraph()
            if list_kind not in {None, "ul"}:
                flush_list()
            list_kind = "ul"
            list_items.append(f"<li>{_apply_inline_markdown(stripped[2:].strip())}</li>")
            continue

        if ORDERED_RE.match(stripped):
            flush_paragraph()
            if list_kind not in {None, "ol"}:
                flush_list()
            list_kind = "ol"
            item_text = ORDERED_RE.sub("", stripped, count=1)
            list_items.append(f"<li>{_apply_inline_markdown(item_text)}</li>")
            continue

        paragraph_lines.append(stripped)

    flush_paragraph()
    flush_list()
    if in_code_block:
        html_parts.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")

    return "\n".join(html_parts)


def _build_tree(repository_root: Path, limit: int = 200) -> list[RepositoryFileEntryOut]:
    entries: list[RepositoryFileEntryOut] = []
    if not repository_root.exists():
        return entries

    for path in sorted(repository_root.rglob("*"), key=lambda item: item.as_posix().lower()):
        if len(entries) >= limit:
            break
        relative_path = path.relative_to(repository_root).as_posix()
        if not relative_path:
            continue
        entry_type = "dir" if path.is_dir() else "file"
        size = 0 if path.is_dir() else path.stat().st_size
        entries.append(RepositoryFileEntryOut(path=relative_path, entry_type=entry_type, size=size))
    return entries


def _repository_root(repository: CodeRepository) -> Path:
    archive_root = repository_storage_path(repository.storage_key) / "files"
    if not archive_root.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Repository archive is missing")
    return _resolve_repository_root(archive_root)


def _store_repository_archive(repository: CodeRepository, archive_name: str, archive_bytes: bytes) -> str:
    if not archive_name.lower().endswith(".zip"):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Only .zip repository archives are supported")
    if not archive_bytes:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Repository archive cannot be empty")

    storage_root = repository_storage_path(repository.storage_key)
    storage_root.mkdir(parents=True, exist_ok=True)
    archive_path = storage_root / "source.zip"
    archive_path.write_bytes(archive_bytes)

    try:
        _extract_archive(archive_path, storage_root / "files")
    except zipfile.BadZipFile as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Uploaded file is not a valid zip archive") from exc

    repository_root = _resolve_repository_root(storage_root / "files")
    readme_path = _find_readme_path(repository_root)
    repository.archive_name = os.path.basename(archive_name)
    repository.readme_path = readme_path
    return readme_path


def create_repository_for_user(
    db: Session,
    user: User,
    *,
    name: str,
    description: str | None,
    is_private: bool,
    whitelist_user_ids: list[int],
    archive_name: str,
    archive_bytes: bytes,
) -> RepositoryOut:
    ensure_repository_storage()
    granted_users = _validate_whitelist_user_ids(db, user, whitelist_user_ids)
    repository = CodeRepository(
        name=_normalize_repository_name(name),
        description=_normalize_description(description),
        is_private=is_private,
        owner_id=user.id,
        storage_key=uuid.uuid4().hex,
    )
    db.add(repository)
    db.flush()

    try:
        _store_repository_archive(repository, archive_name, archive_bytes)
        for granted_user in granted_users:
            db.add(RepositoryAccess(repository_id=repository.id, user_id=granted_user.id))
        db.commit()
    except Exception:
        db.rollback()
        delete_repository_storage(repository.storage_key)
        raise

    db.refresh(repository)
    return _repository_out(repository, "owner")


def update_repository_metadata(db: Session, user: User, repository_id: int, payload: RepositoryUpdateRequest) -> RepositoryOut:
    repository = db.get(CodeRepository, repository_id)
    if repository is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Repository not found")
    if not _can_manage_repository(user, repository):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owner or admin can edit repository")

    if payload.name is not None:
        repository.name = _normalize_repository_name(payload.name)
    if payload.description is not None:
        repository.description = _normalize_description(payload.description)

    db.commit()
    db.refresh(repository)
    access_type = "owner" if repository.owner_id == user.id else "admin"
    return _repository_out(repository, access_type)


def update_repository_access(db: Session, user: User, repository_id: int, payload: RepositoryAccessUpdateRequest) -> RepositoryOut:
    repository = db.get(CodeRepository, repository_id)
    if repository is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Repository not found")
    if not _can_manage_repository(user, repository):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owner or admin can edit repository access")

    if payload.is_private is not None:
        repository.is_private = payload.is_private

    granted_users = _validate_whitelist_user_ids(db, repository.owner, payload.whitelist_user_ids)
    db.execute(delete(RepositoryAccess).where(RepositoryAccess.repository_id == repository.id))
    for granted_user in granted_users:
        db.add(RepositoryAccess(repository_id=repository.id, user_id=granted_user.id))

    db.commit()
    db.refresh(repository)
    access_type = "owner" if repository.owner_id == user.id else "admin"
    return _repository_out(repository, access_type)


def replace_repository_archive(
    db: Session,
    user: User,
    repository_id: int,
    *,
    archive_name: str,
    archive_bytes: bytes,
) -> RepositoryOut:
    repository = db.get(CodeRepository, repository_id)
    if repository is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Repository not found")
    if not _can_manage_repository(user, repository):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owner or admin can upload repository archive")

    _store_repository_archive(repository, archive_name, archive_bytes)
    db.commit()
    db.refresh(repository)
    access_type = "owner" if repository.owner_id == user.id else "admin"
    return _repository_out(repository, access_type)


def get_repository_readme(db: Session, user: User, repository_id: int) -> RepositoryReadmeOut:
    repository = db.get(CodeRepository, repository_id)
    if repository is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Repository not found")

    access_type = authorize_repository_access(db, user, repository)
    repository_root = _repository_root(repository)
    tree = _build_tree(repository_root)
    readme_html = "<p class=\"repo-empty\">No README found in this repository.</p>"
    if repository.readme_path:
        readme_file = repository_root / repository.readme_path
        if readme_file.exists() and readme_file.is_file():
            readme_html = _render_markdown(readme_file.read_text(encoding="utf-8", errors="ignore"))

    return RepositoryReadmeOut(
        repository_id=repository.id,
        name=repository.name,
        description=repository.description or "",
        access_type=access_type,
        archive_name=repository.archive_name or "",
        readme_path=repository.readme_path or "",
        readme_html=readme_html,
        tree=tree,
    )


def get_repository_download(db: Session, user: User, repository_id: int) -> tuple[Path, str]:
    repository = db.get(CodeRepository, repository_id)
    if repository is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Repository not found")

    authorize_repository_access(db, user, repository)
    archive_path = repository_storage_path(repository.storage_key) / "source.zip"
    if not archive_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Repository archive is missing")
    download_name = repository.archive_name or f"{repository.name}.zip"
    return archive_path, download_name


def delete_repository(db: Session, user: User, repository_id: int) -> SimpleMessageResponse:
    repository = db.get(CodeRepository, repository_id)
    if repository is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Repository not found")
    if not _can_manage_repository(user, repository):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owner or admin can delete repository")

    storage_key = repository.storage_key
    repository_name = repository.name
    db.execute(delete(RepositoryAccess).where(RepositoryAccess.repository_id == repository.id))
    db.delete(repository)
    db.commit()
    delete_repository_storage(storage_key)
    return SimpleMessageResponse(message=f"Repository deleted: {repository_name}")
