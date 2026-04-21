# Windows 原生部署说明

当前项目主说明已经放到根目录：

[项目 README](E:/Group-projects/Tool-Nexus/README.md)

团队成员接入教程在这里：

[团队成员接入教程](E:/Group-projects/Tool-Nexus/docs/member-onboarding.md)

这个目录只保留部署相关文件：

- `Caddyfile`
- `frps.toml`
- `frpc.toml`
- `frpc.toml.example`
- `setup-portal.ps1`
- `run-portal.ps1`
- `start-all.ps1`
- `stop-all.ps1`
- `install-services.ps1`
- `bin/`

常用命令：

```powershell
cd E:\Group-projects\Tool-Nexus\deploy\windows-native
powershell -ExecutionPolicy Bypass -File .\setup-portal.ps1 -CondaCmd conda -CondaEnvName tool-nexus
powershell -ExecutionPolicy Bypass -File .\start-all.ps1 -CondaCmd conda -CondaEnvName tool-nexus
powershell -ExecutionPolicy Bypass -File .\stop-all.ps1
```
