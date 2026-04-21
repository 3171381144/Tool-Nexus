from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import require_user
from app.db import get_db
from app.models import User
from app.schemas import ProjectCreateRequest, ProjectOut
from app.services.projects import create_project_for_user, list_accessible_projects


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
