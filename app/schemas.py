from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=1, max_length=128)


class UserCreateRequest(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=6, max_length=128)
    is_admin: bool = False


class UserUpdateRequest(BaseModel):
    username: str | None = Field(default=None, min_length=1, max_length=64)
    password: str | None = Field(default=None, min_length=6, max_length=128)


class UserOut(BaseModel):
    id: int
    username: str
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
    is_private: bool = True
    whitelist_user_ids: list[int] = Field(default_factory=list)


class ProjectAccessUpdateRequest(BaseModel):
    whitelist_user_ids: list[int] = Field(default_factory=list)


class ProjectOut(BaseModel):
    id: int
    name: str
    subdomain: str
    is_private: bool
    owner_id: int
    owner_username: str
    access_type: str
    granted_users: list[UserOut] = Field(default_factory=list)
