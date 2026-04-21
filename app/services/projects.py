from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import Project, ProjectAccess, User
from app.schemas import ProjectCreateRequest, ProjectOut


def serialize_project(project: Project, access_type: str) -> ProjectOut:
    return ProjectOut(
        id=project.id,
        name=project.name,
        subdomain=project.subdomain,
        is_private=project.is_private,
        owner_id=project.owner_id,
        owner_username=project.owner.username,
        access_type=access_type,
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


def create_project_for_user(db: Session, user: User, payload: ProjectCreateRequest) -> ProjectOut:
    normalized_subdomain = payload.subdomain.strip().lower()
    if not settings.subdomain_re.fullmatch(normalized_subdomain):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="subdomain 只能包含小写字母、数字和中划线，且不能以中划线开头或结尾",
        )

    project = Project(
        name=payload.name.strip(),
        subdomain=normalized_subdomain,
        is_private=payload.is_private,
        owner_id=user.id,
    )
    db.add(project)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="subdomain 已被占用")

    db.refresh(project)
    return serialize_project(project, "owner")
