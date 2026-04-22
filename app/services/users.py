from fastapi import HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import Project, ProjectAccess, User
from app.schemas import RegisterRequest, SimpleMessageResponse, UserCreateRequest, UserOut, UserUpdateRequest
from app.services.auth import hash_password


def _clean_optional_text(value: str | None) -> str:
    return value.strip() if value else ""


def serialize_user(user: User) -> UserOut:
    nickname = user.nickname or user.username
    return UserOut(id=user.id, username=user.username, nickname=nickname, is_admin=user.is_admin)


def list_users(db: Session) -> list[UserOut]:
    users = db.scalars(select(User).order_by(User.username)).all()
    return [serialize_user(user) for user in users]


def _create_user_record(db: Session, *, username: str, password: str, nickname: str = "", is_admin: bool = False) -> UserOut:
    username = username.strip()
    if not username:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Username cannot be empty")

    user = User(
        username=username,
        nickname=nickname.strip() or username,
        password_hash=hash_password(password),
        is_admin=is_admin,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    db.refresh(user)
    return serialize_user(user)


def create_user(db: Session, payload: UserCreateRequest) -> UserOut:
    return _create_user_record(
        db,
        username=payload.username,
        nickname=_clean_optional_text(payload.nickname),
        password=payload.password,
        is_admin=payload.is_admin,
    )


def register_user(db: Session, payload: RegisterRequest) -> UserOut:
    if payload.invite_code != settings.registration_invite_code:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid invite code")
    return _create_user_record(
        db,
        username=payload.username,
        nickname=_clean_optional_text(payload.nickname),
        password=payload.password,
        is_admin=False,
    )


def update_current_user(db: Session, user: User, payload: UserUpdateRequest) -> UserOut:
    username = payload.username.strip() if payload.username is not None else None
    if username is not None:
        if not username:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Username cannot be empty")
        user.username = username

    if payload.nickname is not None:
        user.nickname = payload.nickname.strip() or (username or user.username)

    if payload.password is not None:
        user.password_hash = hash_password(payload.password)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

    db.refresh(user)
    return serialize_user(user)


def delete_user(db: Session, admin_user: User, user_id: int) -> SimpleMessageResponse:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if admin_user.id == user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Admin cannot delete current account")

    if user.is_admin:
        admin_count = len(db.scalars(select(User).where(User.is_admin.is_(True))).all())
        if admin_count <= 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete the last admin")

    owned_projects = db.scalars(select(Project).where(Project.owner_id == user.id)).all()
    owned_project_ids = [project.id for project in owned_projects]

    db.execute(delete(ProjectAccess).where(ProjectAccess.user_id == user.id))
    if owned_project_ids:
        db.execute(delete(ProjectAccess).where(ProjectAccess.project_id.in_(owned_project_ids)))
        for project in owned_projects:
            db.delete(project)

    username = user.username
    db.delete(user)
    db.commit()
    return SimpleMessageResponse(message=f"User deleted: {username}")
