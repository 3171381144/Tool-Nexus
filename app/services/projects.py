import socket
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from fastapi import HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import Project, ProjectAccess, User
from app.schemas import ProjectAccessUpdateRequest, ProjectCreateRequest, ProjectDocsUpdateRequest, ProjectHealthOut, ProjectOut, UserOut


def _display_name(user: User) -> str:
    return user.nickname or user.username


def _user_out(user: User) -> UserOut:
    return UserOut(id=user.id, username=user.username, nickname=_display_name(user), is_admin=user.is_admin)


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


def create_project_for_user(db: Session, user: User, payload: ProjectCreateRequest) -> ProjectOut:
    normalized_subdomain = _normalize_subdomain(payload.subdomain)
    granted_users = _validate_whitelist_user_ids(db, user, payload.whitelist_user_ids)

    project = Project(
        name=payload.name.strip(),
        subdomain=normalized_subdomain,
        is_private=payload.is_private,
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

    db.commit()
    db.refresh(project)
    access_type = "owner" if project.owner_id == user.id else "admin"
    return serialize_project(project, access_type)


def _looks_like_frp_error_page(body: str) -> bool:
    normalized_body = body.lower()
    return "powered by frp" in normalized_body or "the page you requested was not found" in normalized_body


def _probe_project(project: Project) -> ProjectHealthOut:
    host = f"{project.subdomain}.{settings.root_domain}" if settings.root_domain else project.subdomain
    request = Request(settings.frp_http_probe_url, headers={"Host": host, "User-Agent": "Tool-Nexus-Health/1.0"})
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


