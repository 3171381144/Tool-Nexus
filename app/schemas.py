from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=1, max_length=128)


class RegisterRequest(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    nickname: str | None = Field(default=None, max_length=64)
    password: str = Field(min_length=6, max_length=128)
    invite_code: str = Field(min_length=1, max_length=128)


class UserCreateRequest(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    nickname: str | None = Field(default=None, max_length=64)
    password: str = Field(min_length=6, max_length=128)
    is_admin: bool = False


class UserUpdateRequest(BaseModel):
    username: str | None = Field(default=None, min_length=1, max_length=64)
    nickname: str | None = Field(default=None, max_length=64)
    password: str | None = Field(default=None, min_length=6, max_length=128)


class UserOut(BaseModel):
    id: int
    username: str
    nickname: str
    is_admin: bool


class LoginResponse(BaseModel):
    message: str
    user: UserOut


class SessionResponse(BaseModel):
    authenticated: bool
    user: UserOut | None = None


class SimpleMessageResponse(BaseModel):
    message: str


class ForwardAuthResult(BaseModel):
    message: str
    project: str
    access_type: str


class ProjectCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    subdomain: str = Field(min_length=3, max_length=63)
    entry_path: str | None = Field(default="", max_length=512)
    is_private: bool = True
    whitelist_user_ids: list[int] = Field(default_factory=list)


class ProjectAccessUpdateRequest(BaseModel):
    is_private: bool | None = None
    whitelist_user_ids: list[int] = Field(default_factory=list)


class ProjectDocsUpdateRequest(BaseModel):
    description: str | None = Field(default=None, max_length=4000)
    usage_guide: str | None = Field(default=None, max_length=8000)
    entry_path: str | None = Field(default=None, max_length=512)


class ProjectHealthOut(BaseModel):
    project_id: int
    subdomain: str
    online: bool
    reason: str


class ProjectOut(BaseModel):
    id: int
    name: str
    subdomain: str
    is_private: bool
    owner_id: int
    owner_username: str
    owner_nickname: str
    description: str = ""
    usage_guide: str = ""
    entry_path: str = ""
    access_type: str
    granted_users: list[UserOut] = Field(default_factory=list)


class RepositoryUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=128)
    description: str | None = Field(default=None, max_length=4000)


class RepositoryAccessUpdateRequest(BaseModel):
    is_private: bool | None = None
    whitelist_user_ids: list[int] = Field(default_factory=list)


class RepositoryFileEntryOut(BaseModel):
    path: str
    entry_type: str
    size: int


class RepositoryReadmeOut(BaseModel):
    repository_id: int
    name: str
    description: str = ""
    access_type: str
    archive_name: str = ""
    readme_path: str = ""
    readme_html: str = ""
    tree: list[RepositoryFileEntryOut] = Field(default_factory=list)


class RepositoryOut(BaseModel):
    id: int
    name: str
    description: str = ""
    is_private: bool
    owner_id: int
    owner_username: str
    owner_nickname: str
    access_type: str
    archive_name: str = ""
    readme_path: str = ""
    granted_users: list[UserOut] = Field(default_factory=list)
