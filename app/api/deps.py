from typing import Optional

from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db import get_db
from app.models import User
from app.services.auth import get_current_user


def require_user(
    db: Session = Depends(get_db),
    session_token: Optional[str] = Cookie(default=None, alias=settings.cookie_name),
) -> User:
    user = get_current_user(db, session_token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="未登录或登录已失效")
    return user
