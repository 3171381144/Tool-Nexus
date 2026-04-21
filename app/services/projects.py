from fastapi import HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import Project, ProjectAccess, User
from app.schemas import ProjectAccessUpdateRequest, ProjectCreateRequest, ProjectOut, UserOut


def _user_out(user: User) -> UserOut:
    return UserOut(id=user.id, username=user.username, is_admin=user.is_admin)


def serialize_project(project: Project, access_type: str) -> ProjectOut:
    granted_users = [_user_out(access.user) for access in project.granted_users]
    return ProjectOut(
        id=project.id,
        name=project.name,
        subdomain=project.subdomain,
        is_private=project.is_private,
        owner_id=project.owner_id,
        owner_username=project.owner.username,
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
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"用户不存在: {missing_ids}")
    return users


def _normalize_subdomain(subdomain: str) -> str:
    normalized_subdomain = subdomain.strip().lower()
    if not settings.subdomain_re.fullmatch(normalized_subdomain):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="子域名只能包含小写字母、数字和中划线，长度 3-63",
        )
    return normalized_subdomain


def create_project_for_user(db: Session, user: User, payload: ProjectCreateRequest) -> ProjectOut:
    normalized_subdomain = _normalize_subdomain(payload.subdomain)
    if payload.whitelist_user_ids and not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="只有管理员可以设置白名单")

    granted_users = _validate_whitelist_user_ids(db, user, payload.whitelist_user_ids) if user.is_admin else []

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
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="子域名已被占用")

    db.refresh(project)
    return serialize_project(project, "owner")


def update_project_access(db: Session, admin: User, project_id: int, payload: ProjectAccessUpdateRequest) -> ProjectOut:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="项目不存在")

    granted_users = _validate_whitelist_user_ids(db, project.owner, payload.whitelist_user_ids)
    db.execute(delete(ProjectAccess).where(ProjectAccess.project_id == project.id))
    for granted_user in granted_users:
        db.add(ProjectAccess(project_id=project.id, user_id=granted_user.id))
    db.commit()
    db.refresh(project)
    access_type = "owner" if project.owner_id == admin.id else "admin"
    return serialize_project(project, access_type)
