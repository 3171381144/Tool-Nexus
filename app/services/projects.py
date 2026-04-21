from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import Project, ProjectAccess, User
from app.schemas import ProjectCreateRequest, ProjectOut, UserOut


def serialize_project(project: Project, access_type: str) -> ProjectOut:
    granted_users = [
        UserOut(id=access.user.id, username=access.user.username)
        for access in project.granted_users
    ]
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

    return sorted(projects_by_id.values(), key=lambda item: (item.access_type, item.subdomain))


def _validate_whitelist_user_ids(db: Session, owner: User, whitelist_user_ids: list[int]) -> list[User]:
    deduped_ids = sorted({user_id for user_id in whitelist_user_ids if user_id != owner.id})
    if not deduped_ids:
        return []

    users = db.scalars(select(User).where(User.id.in_(deduped_ids))).all()
    found_ids = {user.id for user in users}
    missing_ids = [user_id for user_id in deduped_ids if user_id not in found_ids]
    if missing_ids:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"????????: {missing_ids}")
    return users


def create_project_for_user(db: Session, user: User, payload: ProjectCreateRequest) -> ProjectOut:
    normalized_subdomain = payload.subdomain.strip().lower()
    if not settings.subdomain_re.fullmatch(normalized_subdomain):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="subdomain ????????????????????????????",
        )

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
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="subdomain ????")

    db.refresh(project)
    return serialize_project(project, "owner")
