import os
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./portal.db")
    secret_key: str = os.getenv("PORTAL_SECRET_KEY", "change-this-in-production")
    cookie_name: str = os.getenv("COOKIE_NAME", "portal_session")
    cookie_domain: str | None = os.getenv("COOKIE_DOMAIN") or None
    cookie_secure: bool = os.getenv("COOKIE_SECURE", "false").lower() == "true"
    root_domain: str | None = os.getenv("PORTAL_ROOT_DOMAIN") or None
    session_ttl_seconds: int = int(os.getenv("SESSION_TTL_SECONDS", "43200"))
    pbkdf2_iterations: int = 120_000
    subdomain_re: re.Pattern[str] = re.compile(r"^[a-z0-9](?:[a-z0-9-]{1,61}[a-z0-9])?$")


settings = Settings()
