from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import require_admin, require_user
from app.db import get_db
from app.models import User
from app.schemas import UserCreateRequest, UserOut, UserUpdateRequest
from app.services.users import create_user, list_users, update_current_user


router = APIRouter(tags=["users"])


@router.get("/users", response_model=list[UserOut])
def users(_: User = Depends(require_user), db: Session = Depends(get_db)) -> list[UserOut]:
    return list_users(db)


@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def add_user(
    payload: UserCreateRequest,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
) -> UserOut:
    return create_user(db, payload)


@router.patch("/users/me", response_model=UserOut)
def update_me(
    payload: UserUpdateRequest,
    user: User = Depends(require_user),
    db: Session = Depends(get_db),
) -> UserOut:
    return update_current_user(db, user, payload)

