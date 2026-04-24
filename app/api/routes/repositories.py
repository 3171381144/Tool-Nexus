import json

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.deps import require_user
from app.db import get_db
from app.models import User
from app.schemas import (
    RepositoryAccessUpdateRequest,
    RepositoryOut,
    RepositoryReadmeOut,
    RepositoryUpdateRequest,
    SimpleMessageResponse,
)
from app.services.repositories import (
    create_repository_for_user,
    delete_repository,
    get_repository_download,
    get_repository_readme,
    list_accessible_repositories,
    replace_repository_archive,
    update_repository_access,
    update_repository_metadata,
)


router = APIRouter(tags=["repositories"])


def _parse_whitelist_user_ids(raw_value: str | None) -> list[int]:
    if not raw_value:
        return []
    try:
        parsed = json.loads(raw_value)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="whitelist_user_ids must be a JSON array") from exc
    if not isinstance(parsed, list) or any(not isinstance(item, int) for item in parsed):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="whitelist_user_ids must be a JSON array of integers")
    return parsed


@router.get("/my-repositories", response_model=list[RepositoryOut])
def my_repositories(user: User = Depends(require_user), db: Session = Depends(get_db)) -> list[RepositoryOut]:
    return list_accessible_repositories(db, user)


@router.post("/repositories", response_model=RepositoryOut, status_code=status.HTTP_201_CREATED)
async def create_repository(
    name: str = Form(...),
    description: str = Form(default=""),
    is_private: bool = Form(default=True),
    whitelist_user_ids: str = Form(default="[]"),
    archive: UploadFile = File(...),
    user: User = Depends(require_user),
    db: Session = Depends(get_db),
) -> RepositoryOut:
    archive_bytes = await archive.read()
    return create_repository_for_user(
        db,
        user,
        name=name,
        description=description,
        is_private=is_private,
        whitelist_user_ids=_parse_whitelist_user_ids(whitelist_user_ids),
        archive_name=archive.filename or "repository.zip",
        archive_bytes=archive_bytes,
    )


@router.patch("/repositories/{repository_id}", response_model=RepositoryOut)
def patch_repository(
    repository_id: int,
    payload: RepositoryUpdateRequest,
    user: User = Depends(require_user),
    db: Session = Depends(get_db),
) -> RepositoryOut:
    return update_repository_metadata(db, user, repository_id, payload)


@router.put("/repositories/{repository_id}/access", response_model=RepositoryOut)
def put_repository_access(
    repository_id: int,
    payload: RepositoryAccessUpdateRequest,
    user: User = Depends(require_user),
    db: Session = Depends(get_db),
) -> RepositoryOut:
    return update_repository_access(db, user, repository_id, payload)


@router.post("/repositories/{repository_id}/upload", response_model=RepositoryOut)
async def upload_repository_archive(
    repository_id: int,
    archive: UploadFile = File(...),
    user: User = Depends(require_user),
    db: Session = Depends(get_db),
) -> RepositoryOut:
    archive_bytes = await archive.read()
    return replace_repository_archive(
        db,
        user,
        repository_id,
        archive_name=archive.filename or "repository.zip",
        archive_bytes=archive_bytes,
    )


@router.get("/repositories/{repository_id}/readme", response_model=RepositoryReadmeOut)
def repository_readme(
    repository_id: int,
    user: User = Depends(require_user),
    db: Session = Depends(get_db),
) -> RepositoryReadmeOut:
    return get_repository_readme(db, user, repository_id)


@router.get("/repositories/{repository_id}/download", response_class=FileResponse)
def repository_download(
    repository_id: int,
    user: User = Depends(require_user),
    db: Session = Depends(get_db),
) -> FileResponse:
    archive_path, download_name = get_repository_download(db, user, repository_id)
    return FileResponse(path=archive_path, filename=download_name, media_type="application/zip")


@router.delete("/repositories/{repository_id}", response_model=SimpleMessageResponse)
def remove_repository(
    repository_id: int,
    user: User = Depends(require_user),
    db: Session = Depends(get_db),
) -> SimpleMessageResponse:
    return delete_repository(db, user, repository_id)
