param(
    [string]$NssmPath,
    [string]$CloudflaredPath,
    [string]$TunnelToken,
    [string]$CondaCmd = "conda",
    [string]$CondaEnvName = "tool-nexus",
    [string]$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\.." )).Path,
    [string]$BinRoot = (Resolve-Path (Join-Path $PSScriptRoot "bin" )).Path
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not $NssmPath) {
    throw "请传入 -NssmPath，例如 C:\\tools\\nssm\\win64\\nssm.exe"
}
if (-not (Test-Path $NssmPath)) {
    throw "未找到 NSSM: $NssmPath"
}

$caddyExe = Join-Path $BinRoot "caddy.exe"
$frpsExe = Join-Path $BinRoot "frps.exe"
$portalRunner = Join-Path $PSScriptRoot "run-portal.ps1"
$caddyfile = Join-Path $PSScriptRoot "Caddyfile"
$frpsConfig = Join-Path $PSScriptRoot "frps.toml"

foreach ($path in @($caddyExe, $frpsExe, $portalRunner, $caddyfile, $frpsConfig)) {
    if (-not (Test-Path $path)) {
        throw "缺少文件: $path"
    }
}

function Install-Or-UpdateService {
    param(
        [string]$Name,
        [string]$Application,
        [string]$Arguments,
        [string]$AppDirectory
    )

    $existing = Get-Service -Name $Name -ErrorAction SilentlyContinue
    if (-not $existing) {
        & $NssmPath install $Name $Application $Arguments | Out-Null
    }

    & $NssmPath set $Name Application $Application | Out-Null
    & $NssmPath set $Name AppParameters $Arguments | Out-Null
    & $NssmPath set $Name AppDirectory $AppDirectory | Out-Null
    & $NssmPath set $Name Start SERVICE_AUTO_START | Out-Null
    & $NssmPath set $Name AppStopMethodSkip 6 | Out-Null
}

# Portal 服务：通过 PowerShell 启动 run-portal.ps1，便于集中管理环境变量。
Install-Or-UpdateService `
    -Name "ToolNexus-Portal" `
    -Application "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" `
    -Arguments "-NoProfile -ExecutionPolicy Bypass -File `"$portalRunner`" -ProjectRoot `"$ProjectRoot`" -CondaCmd `"$CondaCmd`" -CondaEnvName `"$CondaEnvName`"" `
    -AppDirectory $ProjectRoot

# Caddy 网关服务。
Install-Or-UpdateService `
    -Name "ToolNexus-Caddy" `
    -Application $caddyExe `
    -Arguments "run --config `"$caddyfile`" --adapter caddyfile" `
    -AppDirectory $PSScriptRoot

# FRPS 服务。
Install-Or-UpdateService `
    -Name "ToolNexus-FRPS" `
    -Application $frpsExe `
    -Arguments "-c `"$frpsConfig`"" `
    -AppDirectory $PSScriptRoot

# cloudflared 使用官方 Windows 服务安装方式。
if ($CloudflaredPath -and $TunnelToken) {
    if (-not (Test-Path $CloudflaredPath)) {
        throw "未找到 cloudflared.exe: $CloudflaredPath"
    }
    & $CloudflaredPath service install $TunnelToken
}

Write-Host "[done] 服务注册完成。你可以在 services.msc 中查看 ToolNexus-* 服务。"
Write-Host "[next] 首次启动前，请先手动执行 setup-portal.ps1 准备 Conda 环境。"
