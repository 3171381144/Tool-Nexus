@echo off
cd /d %~dp0

if not exist frpc.exe (
  echo [ERROR] frpc.exe not found in this folder.
  echo Please put frpc.exe and frpc.toml in the same folder.
  pause
  exit /b 1
)

if not exist frpc.toml (
  echo [ERROR] frpc.toml not found in this folder.
  echo Please copy frpc.toml.template to frpc.toml and fill in your project info.
  pause
  exit /b 1
)

frpc.exe -c frpc.toml
pause
