from sqlalchemy import inspect, select, text
from sqlalchemy.orm import Session

from app.db import SessionLocal, engine
from app.models import Base, User
from app.services.auth import hash_password
from app.services.repositories import ensure_repository_storage


def ensure_schema() -> None:
    Base.metadata.create_all(bind=engine)
    ensure_repository_storage()
    with engine.begin() as connection:
        columns = {column["name"] for column in inspect(connection).get_columns("users")}
        if "is_admin" not in columns:
            connection.execute(text("ALTER TABLE users ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT 0"))
        if "nickname" not in columns:
            connection.execute(text("ALTER TABLE users ADD COLUMN nickname VARCHAR(64) NOT NULL DEFAULT ''"))
        connection.execute(text("UPDATE users SET nickname = username WHERE nickname IS NULL OR nickname = ''"))

        project_columns = {column["name"] for column in inspect(connection).get_columns("projects")}
        if "description" not in project_columns:
            connection.execute(text("ALTER TABLE projects ADD COLUMN description TEXT NOT NULL DEFAULT ''"))
        if "usage_guide" not in project_columns:
            connection.execute(text("ALTER TABLE projects ADD COLUMN usage_guide TEXT NOT NULL DEFAULT ''"))
        if "entry_path" not in project_columns:
            connection.execute(text("ALTER TABLE projects ADD COLUMN entry_path VARCHAR(512) NOT NULL DEFAULT ''"))


def ensure_user(db: Session, username: str, password: str, *, nickname: str = "", is_admin: bool = False) -> User:
    user = db.scalar(select(User).where(User.username == username))
    if user is None:
        user = User(
            username=username,
            nickname=nickname or username,
            password_hash=hash_password(password),
            is_admin=is_admin,
        )
        db.add(user)
        return user
    if not user.nickname:
        user.nickname = nickname or username
    if is_admin and not user.is_admin:
        user.is_admin = True
    return user


def bootstrap_database() -> None:
    ensure_schema()

    with SessionLocal() as db:
        ensure_user(db, "zhangsan", "zhangsan123", nickname="Zhangsan", is_admin=True)
        ensure_user(db, "lisi", "lisi123", nickname="Lisi")
        ensure_user(db, "wangwu", "wangwu123", nickname="Wangwu")
        db.commit()
