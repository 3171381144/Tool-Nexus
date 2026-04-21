from sqlalchemy import select

from app.db import SessionLocal, engine
from app.models import Base, User
from app.services.auth import hash_password


def bootstrap_database() -> None:
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        if db.scalar(select(User.id).limit(1)) is not None:
            return

        zhangsan = User(username="??", password_hash=hash_password("zhangsan123"))
        lisi = User(username="??", password_hash=hash_password("lisi123"))
        wangwu = User(username="??", password_hash=hash_password("wangwu123"))
        db.add_all([zhangsan, lisi, wangwu])
        db.commit()
