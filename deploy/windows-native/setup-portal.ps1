param(
    [string]$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\.." )).Path,
    [string]$CondaCmd = "conda",
    [string]$CondaEnvName = "tool-nexus",
    [string]$PythonVersion = "3.12"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$requirements = Join-Path $ProjectRoot "requirements.txt"
if (-not (Test-Path $requirements)) {
    throw "未找到 requirements.txt: $requirements"
}

Write-Host "[setup] 检查 Conda 环境: $CondaEnvName"
Push-Location $ProjectRoot
try {
    $envListJson = & $CondaCmd env list --json
    if ($LASTEXITCODE -ne 0) {
        throw "执行 conda env list 失败，请确认 Conda 已安装且 CondaCmd 可用: $CondaCmd"
    }

    $envList = ($envListJson | ConvertFrom-Json).envs
    $envExists = $false
    foreach ($envPath in $envList) {
        if ((Split-Path $envPath -Leaf) -eq $CondaEnvName) {
            $envExists = $true
            break
        }
    }

    if (-not $envExists) {
        Write-Host "[setup] 创建 Conda 环境: $CondaEnvName (python=$PythonVersion)"
        & $CondaCmd create -y -n $CondaEnvName "python=$PythonVersion"
        if ($LASTEXITCODE -ne 0) {
            throw "创建 Conda 环境失败"
        }
    }

    Write-Host "[setup] 安装 Python 依赖"
    & $CondaCmd run -n $CondaEnvName python -m pip install --upgrade pip
    if ($LASTEXITCODE -ne 0) {
        throw "升级 pip 失败"
    }

    & $CondaCmd run -n $CondaEnvName python -m pip install -r $requirements
    if ($LASTEXITCODE -ne 0) {
        throw "安装 requirements 失败"
    }

    Write-Host "[setup] 初始化 Portal 数据库"
    & $CondaCmd run -n $CondaEnvName --cwd $ProjectRoot python -m app.main --init-db
    if ($LASTEXITCODE -ne 0) {
        throw "初始化数据库失败"
    }
}
finally {
    Pop-Location
}

Write-Host "[done] Portal Conda 环境准备完成"
