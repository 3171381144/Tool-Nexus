# Tool-Nexus

Tool-Nexus 是一个面向小团队的内部工具聚合门户。

它解决 3 件事：

1. 把团队成员本机上的网页工具挂到统一域名下
2. 用 Portal 统一登录和子域名权限控制
3. 用 Cloudflare Tunnel 把本地中心机安全暴露到公网

当前仓库已经收敛到一套可运行的 Windows 原生方案：

- `Cloudflare Tunnel`：公网入口
- `Caddy`：本地网关，负责门户路由和 Forward Auth
- `FastAPI Portal`：登录、项目登记、权限校验、门户前端
- `frps`：中心机穿透服务端
- `frpc`：成员电脑穿透客户端

## 当前架构

```text
浏览器
  -> Cloudflare
  -> cloudflared
  -> Caddy (:80)
     -> portal.aim888888.xyz -> FastAPI Portal (:8000)
     -> *.aim888888.xyz -> /api/auth -> frps (:8080) -> frpc -> 成员本地工具
```

通俗理解：

- `Cloudflare Tunnel` 负责把公网请求带到你的中心机
- `Caddy` 负责看当前访问的是门户还是某个工具子域名
- `Portal` 负责判断“谁可以访问哪个工具”
- `frps/frpc` 负责把请求真正送到某台成员电脑上的本地端口

## 目录说明

```text
app/
  api/
  core/
  services/
  web/
  app.py
  db.py
  main.py
  models.py
  schemas.py
  seed.py

deploy/
  windows-native/
    bin/
      caddy.exe
      frps.exe
      frpc.exe
    Caddyfile
    frps.toml
    frpc.toml
    frpc.toml.example
    setup-portal.ps1
    run-portal.ps1
    start-all.ps1
    stop-all.ps1
    install-services.ps1

portal.db
requirements.txt
```

核心文件：

- `app/`：Portal 后端和门户前端
- `portal.db`：SQLite 数据库
- `deploy/windows-native/Caddyfile`：网关配置
- `deploy/windows-native/frps.toml`：中心机 frps 配置
- `deploy/windows-native/frpc.toml`：当前这台机器本地工具接入配置
- `deploy/windows-native/start-all.ps1`：一键启动 Portal、Caddy、FRPS
- `deploy/windows-native/stop-all.ps1`：一键停止 Portal、Caddy、FRPS

## 当前功能

- 用户登录，签发 Cookie Session
- 门户首页 `/`
- 登录页 `/login`
- `GET /api/auth` Forward Auth 鉴权
- `GET /api/my-projects` 查询当前用户可见项目
- `POST /api/projects` 创建项目
- Caddy 前置鉴权后再转发到 frps
- 支持本机项目和远端成员项目接入

## 环境准备

中心机当前假设为 Windows。

需要准备：

- Anaconda 或 Miniconda
- `caddy.exe`
- `frps.exe`
- `frpc.exe`
- `cloudflared.exe`
- 可选：`nssm.exe`，后续切 Windows 服务时使用

建议二进制目录：

```text
E:\Group-projects\Tool-Nexus\deploy\windows-native\bin\
```

## 首次初始化

先准备 Python 环境和数据库：

```powershell
cd E:\Group-projects\Tool-Nexus\deploy\windows-native
powershell -ExecutionPolicy Bypass -File .\setup-portal.ps1 -CondaCmd conda -CondaEnvName tool-nexus
```

这个脚本会：

- 创建 Conda 环境 `tool-nexus`
- 安装 `requirements.txt`
- 初始化 `portal.db`

## 日常启动

开发和联调阶段，直接一键启动：

```powershell
cd E:\Group-projects\Tool-Nexus\deploy\windows-native
powershell -ExecutionPolicy Bypass -File .\start-all.ps1 -CondaCmd conda -CondaEnvName tool-nexus
```

停止整套：

```powershell
powershell -ExecutionPolicy Bypass -File .\stop-all.ps1
```

这两个脚本当前管理：

- Portal
- Caddy
- FRPS

注意：

- `frpc` 不包含在 `start-all.ps1` 里
- 如果你当前中心机还挂了本机工具，需要单独启动 `frpc.exe -c .\frpc.toml`

## Cloudflare 配置

域名当前是：

- `portal.aim888888.xyz`
- `*.aim888888.xyz`

Tunnel 需要发布两条路由：

- `portal.aim888888.xyz -> http://localhost:80`
- `*.aim888888.xyz -> http://localhost:80`

DNS 里需要有：

- `portal` 指向 Tunnel
- `*` 指向 Tunnel

不要把工具子域名直接指到 `localhost:8080`。

正确入口必须是：

```text
Cloudflare -> Caddy(:80)
```

不是：

```text
Cloudflare -> frps(:8080)
```

## 本机接入一个项目

假设你的项目跑在：

```text
http://127.0.0.1:8765
```

接入步骤：

1. 确认本机端口能打开
2. 登录 Portal，在页面里创建一个项目
3. 子域名例如填 `tosvg`
4. 在 `deploy/windows-native/frpc.toml` 里增加一个 `[[proxies]]`
5. 启动：

```powershell
cd E:\Group-projects\Tool-Nexus\deploy\windows-native
.\bin\frpc.exe -c .\frpc.toml
```

之后访问：

```text
https://tosvg.aim888888.xyz
```

## 团队成员怎么接入

团队成员接入的标准流程是：

1. 先在 Portal 里登记项目
2. 再在成员自己的电脑上配置并启动 `frpc`
3. 由中心机 `frps` 把子域名流量转到成员电脑本地端口

详细步骤见：

[团队成员接入教程](E:/Group-projects/Tool-Nexus/docs/member-onboarding.md)

## 当前默认账号

默认测试账号仍然存在，但默认测试项目已经移除：

- `张三 / zhangsan123`
- `李四 / lisi123`
- `王五 / wangwu123`

## 常见问题

### 1. 为什么 Portal 能打开，但工具子域名打不开？

先按这个顺序排查：

1. `cloudflared` 是否在线
2. Caddy 是否在监听 `80`
3. Portal 是否在监听 `8000`
4. `frps` 是否在监听 `7000 / 8080`
5. 成员电脑上的 `frpc` 是否已经启动
6. Portal 里是否真的创建了对应 `subdomain`

### 2. 为什么访问工具时会被跳回登录页？

说明网关和 Forward Auth 是正常的，只是当前请求没有通过权限校验。

检查：

- 是否已登录
- 项目是否存在
- 当前用户是否是 owner
- 项目是否公开
- 私有项目是否已经授权

### 3. 为什么会出现 frp 的 “The page you requested was not found.”？

这通常表示：

- 请求已经到了 `frps`
- 但 `frpc` 里没有对应 `customDomains`
- 或者 `frpc` 根本没启动

### 4. 为什么其他成员还需要装 `frpc`？

因为工具运行在成员自己的电脑上，中心机看不到对方机器的 `localhost:3000`。

所以必须由成员电脑自己运行 `frpc`，主动连回中心机的 `frps`，把本地端口挂出来。

## 下一步建议

当前系统已经能用，接下来更适合继续补：

- 项目授权管理页面
- 一键生成 `frpc.toml` 配置片段
- Windows 服务化部署
- 操作日志和审计
