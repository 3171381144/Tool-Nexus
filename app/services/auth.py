import base64
import hashlib
import hmac
import json
import secrets
import time
from typing import Optional
from urllib.parse import quote

from fastapi import HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import Project, ProjectAccess, User
from app.schemas import ForwardAuthResult, LoginResponse, SimpleMessageResponse, UserOut


def _b64url_encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def _b64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def _user_out(user: User) -> UserOut:
    return UserOut(id=user.id, username=user.username, nickname=user.nickname or user.username, is_admin=user.is_admin)


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, settings.pbkdf2_iterations)
    return f"pbkdf2_sha256${settings.pbkdf2_iterations}${_b64url_encode(salt)}${_b64url_encode(digest)}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        algorithm, iteration_text, salt_text, digest_text = stored_hash.split("$", maxsplit=3)
        if algorithm != "pbkdf2_sha256":
            return False
        iterations = int(iteration_text)
        salt = _b64url_decode(salt_text)
        expected = _b64url_decode(digest_text)
    except (ValueError, TypeError):
        return False

    actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return hmac.compare_digest(actual, expected)


def create_session_token(user_id: int) -> str:
    now = int(time.time())
    payload = {"sub": user_id, "iat": now, "exp": now + settings.session_ttl_seconds}
    payload_text = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    payload_part = _b64url_encode(payload_text)
    signature = hmac.new(settings.secret_key.encode("utf-8"), payload_part.encode("ascii"), hashlib.sha256).digest()
    return f"{payload_part}.{_b64url_encode(signature)}"


def decode_session_token(token: str) -> Optional[dict]:
    try:
        payload_part, signature_part = token.split(".", maxsplit=1)
        actual_signature = _b64url_decode(signature_part)
    except ValueError:
        return None

    expected_signature = hmac.new(
        settings.secret_key.encode("utf-8"),
        payload_part.encode("ascii"),
        hashlib.sha256,
    ).digest()
    if not hmac.compare_digest(actual_signature, expected_signature):
        return None

    try:
        payload = json.loads(_b64url_decode(payload_part))
    except (ValueError, json.JSONDecodeError):
        return None

    if payload.get("exp", 0) < int(time.time()):
        return None

    return payload


def get_current_user(db: Session, session_token: Optional[str]) -> Optional[User]:
    if not session_token:
        return None

    payload = decode_session_token(session_token)
    if not payload or "sub" not in payload:
        return None

    return db.get(User, payload["sub"])


def authenticate_user(db: Session, username: str, password: str) -> User:
    user = db.scalar(select(User).where(User.username == username))
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    return user


def build_login_response(user: User, response: Response) -> LoginResponse:
    response.set_cookie(
        key=settings.cookie_name,
        value=create_session_token(user.id),
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
        domain=settings.cookie_domain,
        max_age=settings.session_ttl_seconds,
        path="/",
    )
    return LoginResponse(message="Login successful", user=_user_out(user))


def build_logout_response(response: Response) -> SimpleMessageResponse:
    response.delete_cookie(
        key=settings.cookie_name,
        domain=settings.cookie_domain,
        path="/",
    )
    return SimpleMessageResponse(message="Logged out")


def extract_subdomain(forwarded_host: str) -> str:
    host = forwarded_host.split(":", maxsplit=1)[0].strip().lower()

    if settings.root_domain:
        root_domain = settings.root_domain.lower().lstrip(".")
        if host == root_domain or not host.endswith(f".{root_domain}"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="X-Forwarded-Host is outside root domain")
        subdomain = host[: -(len(root_domain) + 1)]
        if "." in subdomain:
            subdomain = subdomain.split(".", maxsplit=1)[0]
        return subdomain

    labels = [label for label in host.split(".") if label]
    if len(labels) < 3:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="X-Forwarded-Host missing subdomain")
    return labels[0]


def authorize_project_access(db: Session, user: User, project: Project) -> str:
    if project.owner_id == user.id:
        return "owner"

    if not project.is_private:
        return "public"

    access_row = db.scalar(
        select(ProjectAccess).where(
            ProjectAccess.project_id == project.id,
            ProjectAccess.user_id == user.id,
        )
    )
    if access_row:
        return "shared"

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission for this project")


def build_forward_auth_result(db: Session, session_token: Optional[str], forwarded_host: Optional[str], response: Response) -> ForwardAuthResult:
    user = get_current_user(db, session_token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not logged in")

    if not forwarded_host:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing X-Forwarded-Host")

    subdomain = extract_subdomain(forwarded_host)
    project = db.scalar(select(Project).where(Project.subdomain == subdomain))
    if not project:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Target subdomain is not registered")

    access_type = authorize_project_access(db, user, project)
    response.headers["X-Auth-User"] = quote(user.username, safe="")
    response.headers["X-Auth-Nickname"] = quote(user.nickname or user.username, safe="")
    response.headers["X-Auth-User-Id"] = str(user.id)
    response.headers["X-Auth-Project"] = project.subdomain
    response.headers["X-Auth-Access-Type"] = access_type
    return ForwardAuthResult(message="ok", project=project.subdomain, access_type=access_type)
