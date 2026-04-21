from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import User
from app.schemas import UserCreateRequest, UserOut
from app.services.auth import hash_password


def serialize_user(user: User) -> UserOut:
    return UserOut(id=user.id, username=user.username)


def list_users(db: Session) -> list[UserOut]:
    users = db.scalars(select(User).order_by(User.username)).all()
    return [serialize_user(user) for user in users]


def create_user(db: Session, payload: UserCreateRequest) -> UserOut:
    username = payload.username.strip()
    if not username:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="username ????")

    user = User(username=username, password_hash=hash_password(payload.password))
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="??????")

    db.refresh(user)
    return serialize_user(user)
