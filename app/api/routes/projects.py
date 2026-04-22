from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import require_admin, require_user
from app.db import get_db
from app.models import User
from app.schemas import ProjectAccessUpdateRequest, ProjectCreateRequest, ProjectDocsUpdateRequest, ProjectHealthOut, ProjectOut
from app.services.projects import check_accessible_project_health, create_project_for_user, list_accessible_projects, update_project_access, update_project_docs


router = APIRouter(tags=["projects"])


@router.get("/my-projects", response_model=list[ProjectOut])
def my_projects(user: User = Depends(require_user), db: Session = Depends(get_db)) -> list[ProjectOut]:
    return list_accessible_projects(db, user)


@router.post("/projects", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(
    payload: ProjectCreateRequest,
    user: User = Depends(require_user),
    db: Session = Depends(get_db),
) -> ProjectOut:
    return create_project_for_user(db, user, payload)



@router.get("/projects/health", response_model=list[ProjectHealthOut])
def project_health(user: User = Depends(require_user), db: Session = Depends(get_db)) -> list[ProjectHealthOut]:
    return check_accessible_project_health(db, user)


@router.patch("/projects/{project_id}/docs", response_model=ProjectOut)
def update_docs(
    project_id: int,
    payload: ProjectDocsUpdateRequest,
    user: User = Depends(require_user),
    db: Session = Depends(get_db),
) -> ProjectOut:
    return update_project_docs(db, user, project_id, payload)
@router.put("/projects/{project_id}/access", response_model=ProjectOut)
def update_access(
    project_id: int,
    payload: ProjectAccessUpdateRequest,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
) -> ProjectOut:
    return update_project_access(db, admin, project_id, payload)
