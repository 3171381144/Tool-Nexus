# Tool-Nexus

Tool-Nexus 是一个面向小团队的内部资源门户，当前支持两类资源：

1. 网页工具：通过统一子域名、Portal 登录态和白名单控制访问。
2. 代码仓库：拥有者上传 zip 归档后，成员可按权限在线查看 README 或下载归档。

当前部署方案：

- `Cloudflare Tunnel`：公网入口
- `Caddy`：Portal 与子域名网关
- `FastAPI Portal`：登录、授权、门户前端、仓库上传/阅读
- `frps/frpc`：网页工具的穿透与转发

## 当前功能

- Cookie Session 登录
- 门户首页 `/` 与登录页 `/login`
- `GET /api/auth` Forward Auth
- `GET /api/my-projects` / `POST /api/projects` 管理网页工具
- `GET /api/my-repositories` / `POST /api/repositories` 管理代码仓库
- 代码仓库支持白名单、zip 上传、README 在线阅读和归档下载

## 服务器部署

代码推送到服务器后，按以下命令更新：

```bash
cd /opt/Tool-Nexus
git pull
cd deploy/server
docker compose up -d --build
```

`portal` 容器会把数据库和仓库文件都持久化到 Docker volume：

- `/data/portal.db`
- `/data/repositories`

## 开发提示

- 网页工具仍然依赖 `frpc` 把本地服务挂到 `*.aim888888.xyz`
- 代码仓库当前采用 zip 上传，不直接拉取 Git 远程仓库
- README 预览器目前是简易版，重点覆盖标题、段落、列表、引用和代码块
