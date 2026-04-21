param(
    [string]$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\.." )).Path,
    [string]$CondaCmd = "conda",
    [string]$CondaEnvName = "tool-nexus"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$portalScript = Join-Path $PSScriptRoot "run-portal.ps1"
$caddyExe = Join-Path $PSScriptRoot "bin\caddy.exe"
$caddyConfig = Join-Path $PSScriptRoot "Caddyfile"
$frpsExe = Join-Path $PSScriptRoot "bin\frps.exe"
$frpsConfig = Join-Path $PSScriptRoot "frps.toml"

foreach ($path in @($portalScript, $caddyExe, $caddyConfig, $frpsExe, $frpsConfig)) {
    if (-not (Test-Path $path)) {
        throw "缺少文件: $path"
    }
}

function Get-ListeningProcessId {
    param([int]$Port)
    $line = netstat -ano -p tcp | Select-String -Pattern (":{0}\s+.*LISTENING\s+(\d+)" -f $Port) | Select-Object -First 1
    if (-not $line) {
        return $null
    }
    $parts = ($line.ToString() -replace '^\s+', '') -split '\s+'
    return [int]$parts[-1]
}

function Wait-ForPort {
    param(
        [int]$Port,
        [int]$TimeoutSeconds = 15
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    do {
        $processId = Get-ListeningProcessId -Port $Port
        if ($processId) {
            return $processId
        }
        Start-Sleep -Milliseconds 500
    } while ((Get-Date) -lt $deadline)

    return $null
}

function Ensure-Started {
    param(
        [string]$Name,
        [int]$Port,
        [string]$FilePath,
        [string[]]$ArgumentList,
        [string]$WorkingDirectory
    )

    $existingPid = Get-ListeningProcessId -Port $Port
    if ($existingPid) {
        Write-Host "[skip] $Name 已在端口 $Port 上运行，PID=$existingPid"
        return
    }

    Write-Host "[start] 启动 $Name"
    Start-Process -FilePath $FilePath -ArgumentList $ArgumentList -WorkingDirectory $WorkingDirectory | Out-Null

    $startedPid = Wait-ForPort -Port $Port -TimeoutSeconds 15
    if (-not $startedPid) {
        throw "$Name 启动失败，端口 $Port 未监听"
    }

    Write-Host "[ok] $Name 已启动，PID=$startedPid，监听端口 $Port"
}

Ensure-Started `
    -Name "Portal" `
    -Port 8000 `
    -FilePath "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" `
    -ArgumentList @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", $portalScript, "-ProjectRoot", $ProjectRoot, "-CondaCmd", $CondaCmd, "-CondaEnvName", $CondaEnvName) `
    -WorkingDirectory $ProjectRoot

Ensure-Started `
    -Name "Caddy" `
    -Port 80 `
    -FilePath $caddyExe `
    -ArgumentList @("run", "--config", $caddyConfig, "--adapter", "caddyfile") `
    -WorkingDirectory $PSScriptRoot

Ensure-Started `
    -Name "FRPS" `
    -Port 7000 `
    -FilePath $frpsExe `
    -ArgumentList @("-c", $frpsConfig) `
    -WorkingDirectory $PSScriptRoot

Write-Host "[done] Portal/Caddy/FRPS 已全部启动。"
