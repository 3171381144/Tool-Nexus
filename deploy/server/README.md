# Tool-Nexus 服务器部署说明

这套部署用于公网服务器，例如当前 Ubuntu 24.04 VPS。

服务器公网 IPv4：`149.71.241.141`

## 1. Cloudflare DNS

在 `aim888888.xyz` 的 DNS 页面配置：

| 名称 | 类型 | 内容 | 代理状态 |
| --- | --- | --- | --- |
| `portal` | `A` | `149.71.241.141` | 已代理，橙云 |
| `*` | `A` | `149.71.241.141` | 已代理，橙云 |
| `frp` | `A` | `149.71.241.141` | 仅 DNS，灰云 |

重点：

- `portal` 和 `*` 是浏览器访问入口，可以橙云。
- `frp` 是 `frpc -> frps:7000` 的原生 TCP 入口，必须灰云。
- 不要给 `frp.aim888888.xyz` 配 Cloudflare Tunnel。

## 2. 服务器安全组/防火墙

需要放行：

- `22/tcp`：SSH
- `80/tcp`：Cloudflare 到 Caddy
- `7000/tcp`：成员 frpc 到 frps

如果你只允许 Cloudflare 访问 80，可以后续再收紧来源 IP。第一版先放行即可。

## 3. 安装 Docker

登录服务器：

```bash
ssh root@149.71.241.141
```

安装 Docker：

```bash
apt update
apt install -y ca-certificates curl gnupg git
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" > /etc/apt/sources.list.d/docker.list
apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## 4. 上传项目

推荐先用 Git：

```bash
cd /opt
git clone <你的仓库地址> Tool-Nexus
cd /opt/Tool-Nexus/deploy/server
```

如果暂时没有远程仓库，也可以从本机用 `scp` 上传整个项目目录。

## 5. 修改密钥

复制环境变量文件：

```bash
cp .env.example .env
```

编辑 `.env`：

```bash
nano .env
```

至少改：

```env
PORTAL_SECRET_KEY=一个足够长的随机字符串
FRP_TOKEN=一个足够长的随机字符串
```

然后把 `frps.toml` 里的 token 改成同一个值：

```toml
auth.token = "你的FRP_TOKEN"
```

## 6. 启动

```bash
docker compose up -d --build
```

查看状态：

```bash
docker compose ps
docker compose logs -f
```

## 7. 验证

浏览器访问：

```text
https://portal.aim888888.xyz
```

成员 frpc 连接配置：

```toml
serverAddr = "frp.aim888888.xyz"
serverPort = 7000
auth.token = "你的FRP_TOKEN"
transport.tls.enable = true

[[proxies]]
name = "zhangsan-tool"
type = "http"
localIP = "127.0.0.1"
localPort = 3000
customDomains = ["zhangsan-tool.aim888888.xyz"]
```

## 8. 迁移现有数据库

如果你要保留当前本机的 `portal.db`，先把服务器启动一次后停掉：

```bash
docker compose down
```

然后把本机的 `portal.db` 上传到服务器，并放进 Docker volume 对应位置。更简单的做法是先不用迁移，重新在服务器 Portal 里创建项目。


## 9. Update server code

After changing code locally and pushing it to GitHub, run this on the server:

```bash
cd /opt/Tool-Nexus
git pull
cd /opt/Tool-Nexus/deploy/server
docker compose up -d --build
```

Use the same command even if you only changed frontend HTML or Python code, because the Portal image must be rebuilt.

Check status and logs:

```bash
docker compose ps
docker compose logs -f portal
```
