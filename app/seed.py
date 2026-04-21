from sqlalchemy import select

from app.db import SessionLocal, engine
from app.models import Base, User
from app.services.auth import hash_password


def ensure_user(db: SessionLocal, username: str, password: str) -> None:
    if db.scalar(select(User.id).where(User.username == username)) is not None:
        return
    db.add(User(username=username, password_hash=hash_password(password)))


def bootstrap_database() -> None:
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        ensure_user(db, "zhangsan", "zhangsan123")
        ensure_user(db, "lisi", "lisi123")
        ensure_user(db, "wangwu", "wangwu123")
        db.commit()
