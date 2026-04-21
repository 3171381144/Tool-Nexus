from typing import Optional

from fastapi import APIRouter, Cookie, Depends, Header, HTTPException, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db import get_db
from app.schemas import ForwardAuthResult, LoginRequest, LoginResponse, SessionResponse, SimpleMessageResponse, UserOut
from app.services.auth import authenticate_user, build_forward_auth_result, build_login_response, build_logout_response, get_current_user


router = APIRouter(tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)) -> LoginResponse:
    user = authenticate_user(db, payload.username, payload.password)
    return build_login_response(user, response)


@router.post("/logout", response_model=SimpleMessageResponse)
def logout(response: Response) -> SimpleMessageResponse:
    return build_logout_response(response)


@router.get("/me", response_model=SessionResponse)
def me(
    db: Session = Depends(get_db),
    session_token: Optional[str] = Cookie(default=None, alias=settings.cookie_name),
) -> SessionResponse:
    user = get_current_user(db, session_token)
    if not user:
        return SessionResponse(authenticated=False, user=None)
    return SessionResponse(authenticated=True, user=UserOut(id=user.id, username=user.username))


def _build_login_redirect(forwarded_host: Optional[str], forwarded_uri: Optional[str]) -> str:
    portal_host = f"portal.{settings.root_domain}" if settings.root_domain else "portal.localhost"
    next_host = (forwarded_host or "").split(":", maxsplit=1)[0].strip()
    next_uri = forwarded_uri or "/"
    if not next_uri.startswith("/"):
        next_uri = "/" + next_uri

    next_url = f"https://{next_host}{next_uri}" if next_host else "https://" + portal_host
    return f"https://{portal_host}/login?next={next_url}"


@router.get("/auth", response_model=ForwardAuthResult)
def forward_auth(
    response: Response,
    x_forwarded_host: Optional[str] = Header(default=None),
    x_forwarded_uri: Optional[str] = Header(default=None),
    x_portal_auth_redirect: Optional[str] = Header(default=None),
    db: Session = Depends(get_db),
    session_token: Optional[str] = Cookie(default=None, alias=settings.cookie_name),
) -> ForwardAuthResult | RedirectResponse:
    try:
        return build_forward_auth_result(db, session_token, x_forwarded_host, response)
    except HTTPException as exc:
        if x_portal_auth_redirect == "1" and exc.status_code in {401, 403}:
            return RedirectResponse(url=_build_login_redirect(x_forwarded_host, x_forwarded_uri), status_code=302)
        raise
