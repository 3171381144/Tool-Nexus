Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-ListeningProcessId {
    param([int]$Port)
    $line = netstat -ano -p tcp | Select-String -Pattern (":{0}\s+.*LISTENING\s+(\d+)" -f $Port) | Select-Object -First 1
    if (-not $line) {
        return $null
    }
    $parts = ($line.ToString() -replace '^\s+', '') -split '\s+'
    return [int]$parts[-1]
}

function Stop-ByPort {
    param(
        [string]$Name,
        [int]$Port
    )

    $processId = Get-ListeningProcessId -Port $Port
    if (-not $processId) {
        Write-Host "[skip] $Name 未监听端口 $Port"
        return
    }

    try {
        $proc = Get-Process -Id $processId -ErrorAction Stop
        Write-Host "[stop] 结束 $Name，PID=$processId，进程名=$($proc.ProcessName)"
        Stop-Process -Id $processId -Force
    }
    catch {
        Write-Host "[warn] 无法结束 $Name，PID=$processId：$($_.Exception.Message)"
    }
}

Stop-ByPort -Name "FRPS" -Port 7000
Stop-ByPort -Name "Caddy" -Port 80
Stop-ByPort -Name "Portal" -Port 8000

Write-Host "[done] Portal/Caddy/FRPS 停止命令已执行。"
