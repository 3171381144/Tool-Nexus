param(
    [string]$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\.." )).Path,
    [string]$CondaCmd = "conda",
    [string]$CondaEnvName = "tool-nexus"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# 这里用环境变量控制运行参数，避免把敏感信息硬编码到 app 代码里。
$env:PORTAL_SECRET_KEY = "please-change-this-secret-key"
$env:COOKIE_NAME = "portal_session"
$env:COOKIE_DOMAIN = ".aim888888.xyz"
$env:COOKIE_SECURE = "true"
$env:PORTAL_ROOT_DOMAIN = "aim888888.xyz"
$env:DATABASE_URL = "sqlite:///$($ProjectRoot.Replace('\','/'))/portal.db"
$env:SESSION_TTL_SECONDS = "43200"
$env:FRP_HTTP_PROBE_URL = "http://127.0.0.1:8080"

Push-Location $ProjectRoot
try {
    & $CondaCmd run -n $CondaEnvName --cwd $ProjectRoot python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
}
finally {
    Pop-Location
}
