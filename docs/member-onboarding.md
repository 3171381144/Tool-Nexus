# 团队成员接入教程

这份文档给团队成员使用。

目标是把你自己电脑上的一个网页工具接入 Tool-Nexus，并通过统一子域名访问。

示例目标：

- 你的本地工具：`http://127.0.0.1:3000`
- 对外访问地址：`https://zhangsan-tool.aim888888.xyz`

## 你需要做什么

你只需要完成 4 步：

1. 确认你的本地网站能打开
2. 在 Portal 里登记一个项目
3. 配置你电脑上的 `frpc`
4. 启动 `frpc`

## 原理

你的网页并不会直接暴露到公网。

真正的路径是：

```text
浏览器
  -> Cloudflare
  -> 中心机 Caddy
  -> Portal 判断权限
  -> 中心机 frps
  -> 你电脑上的 frpc
  -> 你的本地网页端口
```

所以你电脑上必须运行 `frpc`。

## 第 1 步：确认本地网站已经启动

先在你自己的电脑上确认工具真的能打开。

例如：

```text
http://127.0.0.1:3000
```

如果这里都打不开，就不要继续往下了，先把项目本身跑起来。

## 第 2 步：登录 Portal 并登记项目

打开：

```text
https://portal.aim888888.xyz
```

登录后，在门户里创建项目，填写：

- 工具名称：例如 `张三工具`
- 子域名前缀：例如 `zhangsan-tool`
- 可见性：先选公开，联通后再改私有

创建成功后，你的项目地址就是：

```text
https://zhangsan-tool.aim888888.xyz
```

注意：

- 这里填的子域名，必须和 `frpc.toml` 里的 `customDomains` 完全一致
- 如果 Portal 里没有这条项目，网关不会放行

## 第 3 步：准备 frpc

向管理员拿到：

- `frpc.exe`
- 一份模板配置
- 中心机地址
- `frps` 的 token

frp 官方资料：

- 官方文档：[https://gofrp.org/en/docs/setup/](https://gofrp.org/en/docs/setup/)
- 官方下载页：[https://github.com/fatedier/frp/releases](https://github.com/fatedier/frp/releases)

## 第 4 步：填写 frpc.toml

示例配置：

```toml
serverAddr = "127.0.0.1"
serverPort = 7000
auth.token = "please-change-this-frp-token"
transport.tls.enable = true

[[proxies]]
name = "zhangsan-tool"
type = "http"
localIP = "127.0.0.1"
localPort = 3000
customDomains = ["zhangsan-tool.aim888888.xyz"]
```

上面这份模板已经填入了当前中心机本机自测时使用的值：

- `serverAddr = "127.0.0.1"`
- `auth.token = "please-change-this-frp-token"`

但要注意：

- 如果你不是在中心机本机上跑 `frpc`，不要直接照抄 `127.0.0.1`
- 你应该把 `serverAddr` 改成中心机对你可达的实际地址，例如内网 IP、DDNS 域名、IPv6 地址或组网地址
- `auth.token` 也应该以管理员实际下发的值为准

你只需要重点改这几个值：

- `serverAddr`
- `auth.token`
- `name`
- `localPort`
- `customDomains`

字段解释：

- `serverAddr`：中心机的可达地址
- `serverPort`：固定是 `7000`
- `localPort`：你本地项目实际监听的端口
- `customDomains`：你在 Portal 里登记的完整域名

## 第 5 步：启动 frpc

进入 `frpc.exe` 所在目录后执行：

```powershell
.\frpc.exe -c .\frpc.toml
```

如果启动成功，你会看到类似：

```text
login to server success
start proxy success
```

这个窗口不要关闭。

## 第 6 步：访问你的公网地址

打开：

```text
https://zhangsan-tool.aim888888.xyz
```

如果你已经登录 Portal，并且项目登记无误，就应该能看到你的工具页面。

## 如果你有多个项目

一台电脑通常只需要一个 `frpc.toml`。

多个项目写成多个 `[[proxies]]` 即可。

例如：

```toml
serverAddr = "127.0.0.1"
serverPort = 7000
auth.token = "please-change-this-frp-token"
transport.tls.enable = true

[[proxies]]
name = "tool-a"
type = "http"
localIP = "127.0.0.1"
localPort = 3000
customDomains = ["tool-a.aim888888.xyz"]

[[proxies]]
name = "tool-b"
type = "http"
localIP = "127.0.0.1"
localPort = 5173
customDomains = ["tool-b.aim888888.xyz"]
```

## 常见问题

### 1. 打开域名后跳回登录页

说明网关正常，但当前登录态或权限没通过。

检查：

- 是否已登录 Portal
- 项目是否已登记
- 子域名是否一致
- 项目是否公开，或你是否被授权

### 2. 打开域名后看到 frp 的 404 页面

说明请求已经到了中心机 `frps`，但没有成功匹配到你的代理。

检查：

- `frpc` 是否真的启动了
- `customDomains` 是否正确
- Portal 里登记的子域名和 `frpc.toml` 是否一致

### 3. 打开域名后什么都没有

先直接访问你自己电脑上的本地地址，例如：

```text
http://127.0.0.1:3000
```

如果本地都打不开，就不是 Tool-Nexus 的问题，而是你的项目本身没跑起来。

### 4. 关闭终端后为什么外网就访问不了了？

因为 `frpc` 进程被你关掉了。

要保持外网可访问，你的 `frpc` 必须一直运行。

## 给管理员的信息

如果你接不通，把下面这些信息发给管理员最快：

- 你的项目本地端口
- 你登记的子域名前缀
- 你的 `frpc.toml`
- `frpc` 启动日志截图
- 访问公网地址时的报错截图
