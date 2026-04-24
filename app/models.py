from sqlalchemy import Boolean, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    nickname: Mapped[str] = mapped_column(String(64), default="", server_default="")
    password_hash: Mapped[str] = mapped_column(String(255))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")

    owned_projects: Mapped[list["Project"]] = relationship(back_populates="owner")
    project_accesses: Mapped[list["ProjectAccess"]] = relationship(back_populates="user")
    owned_repositories: Mapped[list["CodeRepository"]] = relationship(back_populates="owner")
    repository_accesses: Mapped[list["RepositoryAccess"]] = relationship(back_populates="user")


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    subdomain: Mapped[str] = mapped_column(String(63), unique=True, index=True)
    is_private: Mapped[bool] = mapped_column(Boolean, default=True)
    description: Mapped[str] = mapped_column(Text, default="", server_default="")
    usage_guide: Mapped[str] = mapped_column(Text, default="", server_default="")
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


class CodeRepository(Base):
    __tablename__ = "code_repositories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(Text, default="", server_default="")
    is_private: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    storage_key: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    archive_name: Mapped[str] = mapped_column(String(255), default="", server_default="")
    readme_path: Mapped[str] = mapped_column(String(512), default="", server_default="")

    owner: Mapped[User] = relationship(back_populates="owned_repositories")
    granted_users: Mapped[list["RepositoryAccess"]] = relationship(back_populates="repository")


class RepositoryAccess(Base):
    __tablename__ = "repository_access"
    __table_args__ = (UniqueConstraint("repository_id", "user_id", name="uq_repository_user_access"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    repository_id: Mapped[int] = mapped_column(ForeignKey("code_repositories.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    repository: Mapped[CodeRepository] = relationship(back_populates="granted_users")
    user: Mapped[User] = relationship(back_populates="repository_accesses")
