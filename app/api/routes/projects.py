from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.deps import require_user
from app.db import get_db
from app.models import User
from app.schemas import ProjectAccessUpdateRequest, ProjectCreateRequest, ProjectDocsUpdateRequest, ProjectHealthOut, ProjectOut, SimpleMessageResponse
from app.services.projects import check_accessible_project_health, create_project_for_user, delete_project, get_project_media_file, list_accessible_projects, update_project_access, update_project_cover, update_project_demo_video, update_project_docs


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
    user: User = Depends(require_user),
    db: Session = Depends(get_db),
) -> ProjectOut:
    return update_project_access(db, user, project_id, payload)



@router.post("/projects/{project_id}/cover", response_model=ProjectOut)
async def upload_project_cover(
    project_id: int,
    cover: UploadFile = File(...),
    user: User = Depends(require_user),
    db: Session = Depends(get_db),
) -> ProjectOut:
    cover_bytes = await cover.read()
    return update_project_cover(db, user, project_id, cover.filename or "cover", cover_bytes)


@router.post("/projects/{project_id}/demo-video", response_model=ProjectOut)
async def upload_project_demo_video(
    project_id: int,
    video: UploadFile = File(...),
    user: User = Depends(require_user),
    db: Session = Depends(get_db),
) -> ProjectOut:
    video_bytes = await video.read()
    return update_project_demo_video(db, user, project_id, video.filename or "demo.mp4", video_bytes)


@router.get("/projects/{project_id}/media/{media_kind}", response_class=FileResponse)
def project_media(
    project_id: int,
    media_kind: str,
    user: User = Depends(require_user),
    db: Session = Depends(get_db),
) -> FileResponse:
    media_path, media_type = get_project_media_file(db, user, project_id, media_kind)
    return FileResponse(path=media_path, media_type=media_type)

@router.delete("/projects/{project_id}", response_model=SimpleMessageResponse)
def remove_project(
    project_id: int,
    user: User = Depends(require_user),
    db: Session = Depends(get_db),
) -> SimpleMessageResponse:
    return delete_project(db, user, project_id)

