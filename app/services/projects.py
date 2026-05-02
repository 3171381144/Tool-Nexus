import mimetypes
import shutil
import socket
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from fastapi import HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import Project, ProjectAccess, User
from app.schemas import ProjectAccessUpdateRequest, ProjectCreateRequest, ProjectDocsUpdateRequest, ProjectHealthOut, ProjectOut, SimpleMessageResponse, UserOut


def _display_name(user: User) -> str:
    return user.nickname or user.username


def _user_out(user: User) -> UserOut:
    return UserOut(id=user.id, username=user.username, nickname=_display_name(user), is_admin=user.is_admin)



IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
VIDEO_EXTENSIONS = {".mp4", ".webm", ".mov", ".m4v"}
IMAGE_MAX_BYTES = 10 * 1024 * 1024
VIDEO_MAX_BYTES = 200 * 1024 * 1024


def ensure_project_media_storage() -> None:
    Path(settings.project_media_dir).mkdir(parents=True, exist_ok=True)


def project_media_path(project_id: int) -> Path:
    return Path(settings.project_media_dir) / str(project_id)


def delete_project_media(project_id: int) -> None:
    path = project_media_path(project_id)
    if path.exists():
        shutil.rmtree(path, ignore_errors=True)


def _project_media_url(project: Project, media_kind: str) -> str:
    if media_kind == "cover" and project.cover_image_path:
        return f"/api/projects/{project.id}/media/cover"
    if media_kind == "demo-video" and project.demo_video_path:
        return f"/api/projects/{project.id}/media/demo-video"
    return ""


def _validate_project_media(file_name: str, file_bytes: bytes, media_kind: str) -> str:
    suffix = Path(file_name or "").suffix.lower()
    allowed_extensions = IMAGE_EXTENSIONS if media_kind == "cover" else VIDEO_EXTENSIONS
    max_bytes = IMAGE_MAX_BYTES if media_kind == "cover" else VIDEO_MAX_BYTES
    label = "cover image" if media_kind == "cover" else "demo video"
    if suffix not in allowed_extensions:
        allowed = ", ".join(sorted(allowed_extensions))
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Unsupported {label} type. Allowed: {allowed}")
    if not file_bytes:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"{label.title()} cannot be empty")
    if len(file_bytes) > max_bytes:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=f"{label.title()} is too large")
    return suffix


def _replace_project_media_file(project: Project, media_kind: str, file_name: str, file_bytes: bytes) -> None:
    ensure_project_media_storage()
    suffix = _validate_project_media(file_name, file_bytes, media_kind)
    directory = project_media_path(project.id)
    directory.mkdir(parents=True, exist_ok=True)
    stem = "cover" if media_kind == "cover" else "demo"
    for existing_file in directory.glob(f"{stem}.*"):
        if existing_file.is_file():
            existing_file.unlink()
    relative_path = Path(str(project.id)) / f"{stem}{suffix}"
    (Path(settings.project_media_dir) / relative_path).write_bytes(file_bytes)
    if media_kind == "cover":
        project.cover_image_path = relative_path.as_posix()
    else:
        project.demo_video_path = relative_path.as_posix()


def _can_view_project(db: Session, user: User, project: Project) -> bool:
    if user.is_admin or project.owner_id == user.id or not project.is_private:
        return True
    access_row = db.scalar(
        select(ProjectAccess).where(
            ProjectAccess.project_id == project.id,
            ProjectAccess.user_id == user.id,
        )
    )
    return access_row is not None

def serialize_project(project: Project, access_type: str) -> ProjectOut:
    granted_users = [_user_out(access.user) for access in project.granted_users]
    return ProjectOut(
        id=project.id,
        name=project.name,
        subdomain=project.subdomain,
        is_private=project.is_private,
        owner_id=project.owner_id,
        owner_username=project.owner.username,
        owner_nickname=_display_name(project.owner),
        description=project.description or "",
        usage_guide=project.usage_guide or "",
        entry_path=project.entry_path or "",
        cover_image_path=_project_media_url(project, "cover"),
        demo_video_path=_project_media_url(project, "demo-video"),
        access_type=access_type,
        granted_users=granted_users,
    )


def list_accessible_projects(db: Session, user: User) -> list[ProjectOut]:
    projects_by_id: dict[int, ProjectOut] = {}

    owned_projects = db.scalars(select(Project).where(Project.owner_id == user.id)).all()
    for project in owned_projects:
        projects_by_id[project.id] = serialize_project(project, "owner")

    public_projects = db.scalars(
        select(Project).where(Project.is_private.is_(False), Project.owner_id != user.id)
    ).all()
    for project in public_projects:
        projects_by_id.setdefault(project.id, serialize_project(project, "public"))

    shared_projects = db.scalars(
        select(Project)
        .join(ProjectAccess, ProjectAccess.project_id == Project.id)
        .where(ProjectAccess.user_id == user.id, Project.owner_id != user.id)
    ).all()
    for project in shared_projects:
        projects_by_id[project.id] = serialize_project(project, "shared")

    if user.is_admin:
        all_projects = db.scalars(select(Project)).all()
        for project in all_projects:
            projects_by_id.setdefault(project.id, serialize_project(project, "admin"))

    return sorted(projects_by_id.values(), key=lambda item: (item.access_type, item.subdomain))


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


def _normalize_subdomain(subdomain: str) -> str:
    normalized_subdomain = subdomain.strip().lower()
    if not settings.subdomain_re.fullmatch(normalized_subdomain):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Subdomain must be 3-63 chars and only contain lowercase letters, numbers, and hyphens",
        )
    return normalized_subdomain


def _normalize_entry_path(entry_path: str | None) -> str:
    normalized_entry_path = (entry_path or "").strip()
    if not normalized_entry_path:
        return ""
    lowered = normalized_entry_path.lower()
    if lowered.startswith("http://") or lowered.startswith("https://"):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Entry path must be a suffix like /login")
    if not normalized_entry_path.startswith("/"):
        normalized_entry_path = "/" + normalized_entry_path.lstrip()
    return normalized_entry_path


def _project_request_path(entry_path: str | None) -> str:
    normalized_entry_path = _normalize_entry_path(entry_path)
    if not normalized_entry_path:
        return "/"
    parsed = urlsplit(normalized_entry_path)
    request_path = parsed.path or "/"
    if parsed.query:
        request_path += f"?{parsed.query}"
    return request_path


def create_project_for_user(db: Session, user: User, payload: ProjectCreateRequest) -> ProjectOut:
    normalized_subdomain = _normalize_subdomain(payload.subdomain)
    normalized_entry_path = _normalize_entry_path(payload.entry_path)
    granted_users = _validate_whitelist_user_ids(db, user, payload.whitelist_user_ids)

    project = Project(
        name=payload.name.strip(),
        subdomain=normalized_subdomain,
        is_private=payload.is_private,
        entry_path=normalized_entry_path,
        owner_id=user.id,
    )
    db.add(project)
    try:
        db.flush()
        for granted_user in granted_users:
            db.add(ProjectAccess(project_id=project.id, user_id=granted_user.id))
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Subdomain already exists")

    db.refresh(project)
    return serialize_project(project, "owner")


def update_project_access(db: Session, user: User, project_id: int, payload: ProjectAccessUpdateRequest) -> ProjectOut:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    if not _can_edit_project(user, project):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owner or admin can edit project access")

    if payload.is_private is not None:
        project.is_private = payload.is_private

    granted_users = _validate_whitelist_user_ids(db, project.owner, payload.whitelist_user_ids)
    db.execute(delete(ProjectAccess).where(ProjectAccess.project_id == project.id))
    for granted_user in granted_users:
        db.add(ProjectAccess(project_id=project.id, user_id=granted_user.id))
    db.commit()
    db.refresh(project)
    access_type = "owner" if project.owner_id == user.id else "admin"
    return serialize_project(project, access_type)





def _can_edit_project(user: User, project: Project) -> bool:
    return user.is_admin or project.owner_id == user.id


def update_project_docs(db: Session, user: User, project_id: int, payload: ProjectDocsUpdateRequest) -> ProjectOut:
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    if not _can_edit_project(user, project):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owner or admin can edit project docs")

    if payload.description is not None:
        project.description = payload.description.strip()
    if payload.usage_guide is not None:
        project.usage_guide = payload.usage_guide.strip()
    if payload.entry_path is not None:
        project.entry_path = _normalize_entry_path(payload.entry_path)

    db.commit()
    db.refresh(project)
    access_type = "owner" if project.owner_id == user.id else "admin"
    return serialize_project(project, access_type)




def update_project_cover(db: Session, user: User, project_id: int, file_name: str, file_bytes: bytes) -> ProjectOut:
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    if not _can_edit_project(user, project):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owner or admin can update project cover")

    _replace_project_media_file(project, "cover", file_name, file_bytes)
    db.commit()
    db.refresh(project)
    access_type = "owner" if project.owner_id == user.id else "admin"
    return serialize_project(project, access_type)


def update_project_demo_video(db: Session, user: User, project_id: int, file_name: str, file_bytes: bytes) -> ProjectOut:
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    if not _can_edit_project(user, project):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owner or admin can update project demo video")

    _replace_project_media_file(project, "demo-video", file_name, file_bytes)
    db.commit()
    db.refresh(project)
    access_type = "owner" if project.owner_id == user.id else "admin"
    return serialize_project(project, access_type)


def get_project_media_file(db: Session, user: User, project_id: int, media_kind: str) -> tuple[Path, str]:
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    if not _can_view_project(db, user, project):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission for this project")

    relative_path = project.cover_image_path if media_kind == "cover" else project.demo_video_path
    if not relative_path:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project media not found")
    root = Path(settings.project_media_dir).resolve()
    file_path = (Path(settings.project_media_dir) / relative_path).resolve()
    if root not in file_path.parents:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project media not found")
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project media not found")
    media_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
    return file_path, media_type

def delete_project(db: Session, user: User, project_id: int) -> SimpleMessageResponse:
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    if not _can_edit_project(user, project):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owner or admin can delete project")

    project_name = project.name
    db.execute(delete(ProjectAccess).where(ProjectAccess.project_id == project.id))
    project_id_for_media = project.id
    db.delete(project)
    db.commit()
    delete_project_media(project_id_for_media)
    return SimpleMessageResponse(message=f"Project deleted: {project_name}")


def _looks_like_frp_error_page(body: str) -> bool:
    normalized_body = body.lower()
    return "powered by frp" in normalized_body or "the page you requested was not found" in normalized_body


def _probe_project(project: Project) -> ProjectHealthOut:
    host = f"{project.subdomain}.{settings.root_domain}" if settings.root_domain else project.subdomain
    request_url = settings.frp_http_probe_url.rstrip("/") + _project_request_path(project.entry_path)
    request = Request(request_url, headers={"Host": host, "User-Agent": "Tool-Nexus-Health/1.0"})
    try:
        with urlopen(request, timeout=2) as response:
            body = response.read(1024).decode("utf-8", errors="ignore")
            if _looks_like_frp_error_page(body):
                return ProjectHealthOut(project_id=project.id, subdomain=project.subdomain, online=False, reason="frpc not connected")
            return ProjectHealthOut(project_id=project.id, subdomain=project.subdomain, online=True, reason=f"HTTP {response.status}")
    except HTTPError as exc:
        body = exc.read(1024).decode("utf-8", errors="ignore")
        if _looks_like_frp_error_page(body) or exc.code == 404:
            return ProjectHealthOut(project_id=project.id, subdomain=project.subdomain, online=False, reason="frpc not connected")
        if exc.code in {502, 503, 504}:
            return ProjectHealthOut(project_id=project.id, subdomain=project.subdomain, online=False, reason="local service down")
        return ProjectHealthOut(project_id=project.id, subdomain=project.subdomain, online=True, reason=f"HTTP {exc.code}")
    except (URLError, socket.timeout, TimeoutError):
        return ProjectHealthOut(project_id=project.id, subdomain=project.subdomain, online=False, reason="probe failed")


def check_accessible_project_health(db: Session, user: User) -> list[ProjectHealthOut]:
    project_ids = [project.id for project in list_accessible_projects(db, user)]
    if not project_ids:
        return []
    projects = db.scalars(select(Project).where(Project.id.in_(project_ids))).all()
    return [_probe_project(project) for project in projects]




