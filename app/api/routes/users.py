from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import require_user
from app.db import get_db
from app.models import User
from app.schemas import UserCreateRequest, UserOut
from app.services.users import create_user, list_users


router = APIRouter(tags=["users"])


@router.get("/users", response_model=list[UserOut])
def users(_: User = Depends(require_user), db: Session = Depends(get_db)) -> list[UserOut]:
    return list_users(db)


@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def add_user(
    payload: UserCreateRequest,
    _: User = Depends(require_user),
    db: Session = Depends(get_db),
) -> UserOut:
    return create_user(db, payload)
