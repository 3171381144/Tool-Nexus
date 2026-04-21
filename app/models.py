from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))

    owned_projects: Mapped[list["Project"]] = relationship(back_populates="owner")
    project_accesses: Mapped[list["ProjectAccess"]] = relationship(back_populates="user")


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    subdomain: Mapped[str] = mapped_column(String(63), unique=True, index=True)
    is_private: Mapped[bool] = mapped_column(Boolean, default=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    owner: Mapped[User] = relationship(back_populates="owned_projects")
    granted_users: Mapped[list["ProjectAccess"]] = relationship(back_populates="project")


class ProjectAccess(Base):
    __tablename__ = "project_access"
    __table_args__ = (UniqueConstraint("project_id", "user_id", name="uq_project_user_access"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    project: Mapped[Project] = relationship(back_populates="granted_users")
    user: Mapped[User] = relationship(back_populates="project_accesses")
