@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"

if not exist "frpc.exe" (
  echo [ERROR] frpc.exe not found in this folder.
  echo Please put frpc.exe, start.bat and configure-frpc.ps1 in the same folder.
  pause
  exit /b 1
)

if not exist "configure-frpc.ps1" (
  echo [ERROR] configure-frpc.ps1 not found in this folder.
  pause
  exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0configure-frpc.ps1"
if errorlevel 1 (
  echo.
  echo [ERROR] Failed to generate frpc.toml.
  pause
  exit /b 1
)

echo.
echo Starting frpc. Keep this window open while the public URL is in use.
echo.
"%~dp0frpc.exe" -c "%~dp0frpc.toml"
pause
