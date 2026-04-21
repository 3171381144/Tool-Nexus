from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.web.pages import LOGIN_PAGE_HTML, PORTAL_PAGE_HTML


router = APIRouter(tags=["web"])


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def portal_page() -> HTMLResponse:
    return HTMLResponse(PORTAL_PAGE_HTML)


@router.get("/login", response_class=HTMLResponse, include_in_schema=False)
def login_page() -> HTMLResponse:
    return HTMLResponse(LOGIN_PAGE_HTML)
