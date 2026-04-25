# Tool-Nexus 成员端发布包说明

这个目录是给团队成员使用的 FRP 客户端包，用来把你本机已经跑起来的网页临时映射到公网，方便他人访问和联调。

## 先准备好这些文件

把下面几个文件放在同一个文件夹中：

- `frpc.exe`
- `start.bat`
- `configure-frpc.ps1`
- `frpc.toml`

说明：

- 如果已有 `frpc.toml`，并且里面已经填好了真实的 `auth.token`，脚本会继续沿用。

## 快速上手

### 第 1 步：先启动你的本地项目

先确保你自己的前端或本地网页已经能正常访问，例如：

```text
http://127.0.0.1:8077/management.html#/
http://127.0.0.1:8019/
```

建议先在本机浏览器里打开一次，确认页面确实是正常的，再做公网映射。

### 第 2 步：双击启动

直接双击 `start.bat`。

脚本会先检查必要文件，然后调用 `configure-frpc.ps1` 生成或更新 `frpc.toml`，最后自动启动 `frpc.exe`。

### 第 3 步：首次使用时填写项目信息

**重要！！！
先输入管理员给的密钥：
<mark>`change-this-frp-token**`</mark>

然后运行时，脚本会先问你要暴露几个项目：

```text
How many projects do you want to expose? [1]
```

直接回车表示默认 1 个，也可以输入 `2`、`3` 等数量。

然后依次填写每个项目的信息：

```text
Local web URL: http://127.0.0.1:8077/management.html#/
Project name: cpa-proxy
Subdomain or full domain: webxkk
```

字段说明：

- `Local web URL`：你本机真正能访问的页面地址
- `Project name`：项目标识名，只用于配置区分，建议填简短英文名
- `Subdomain or full domain`：可填二级域名前缀，也可直接填完整域名

### 第 4 步：保持窗口不要关闭

配置完成后，脚本会自动启动 `frpc.exe`。

只要你还希望公网地址可访问，就不要关闭这个命令行窗口。

## 再次运行时怎么选

如果目录里已经存在可用的 `frpc.toml`，脚本会给你 3 个选项：

```text
Press Enter / 
S = start directly with existing config
A = add more project(s)
R = rebuild all config
```

含义如下：

- 直接回车或输入 `S`：沿用现有配置，直接启动
- 输入 `A`：在现有配置基础上继续新增项目
- 输入 `R`：清空原有项目配置并重新生成

## 一个成员如何配置多个项目

一个成员只需要：

- 一个 `frpc.exe`
- 一个 `frpc.toml`

如果你要同时暴露多个本地项目，脚本会把它们都写进同一个 `frpc.toml`，每个项目对应一个 `[[proxies]]` 配置块。

示例：

```toml
[[proxies]]
name = "personal-web"
type = "http"
localIP = "127.0.0.1"
localPort = 8019
customDomains = ["web.aim888888.xyz"]

[[proxies]]
name = "cpa-proxy"
type = "http"
localIP = "127.0.0.1"
localPort = 8077
customDomains = ["webxkk.aim888888.xyz"]
```

## 域名填写规则

你可以输入：

```text
webxkk
```

也可以直接输入：

```text
webxkk.aim888888.xyz
```

这两种写法最终都会映射成：

```text
https://webxkk.aim888888.xyz
```

例如，你本地真实页面是：

```text
http://127.0.0.1:8077/management.html#/
```

那么外部访问地址通常就是：

```text
https://webxkk.aim888888.xyz/management.html#/
```

也就是说，脚本会保留你原始本地 URL 的路径和锚点部分。

## Token 说明

如果 `frpc.toml` 里已经有真实的 `auth.token`，脚本会直接保留。

如果还是默认占位值：

```text
change-this-frp-token
```

说明你还没有拿到正式 FRP 凭证，需要联系管理员获取 token。

## 常见问题

### 1. 打开公网地址后显示：

```text
The page you requested was not found. powered by frp
```

通常表示 `frpc` 没有成功注册这个域名。请重点检查：

- `auth.token` 是否正确
- 域名拼写是否正确
- 启动日志里是否出现 `start proxy success`

### 2. 页面提示：

```text
Blocked request. This host is not allowed
```

这通常不是 FRP 问题，而是你的前端开发服务器拦截了公网域名。

如果你使用的是 Vite，请在 `vite.config.ts` 或 `vite.config.js` 中给 `server.allowedHosts` 增加：

```text
.aim888888.xyz
```

### 3. 公网页面能打开，但内容不对

通常是本地 URL 填错了端口，或者本地服务本身访问的就不是目标页面。

请重新检查你填写的 `Local web URL`，尤其是端口号是否正确。

## 官方参考

- frp 文档：[https://gofrp.org/en/docs/setup/](https://gofrp.org/en/docs/setup/)
- frp 发布页：[https://github.com/fatedier/frp/releases](https://github.com/fatedier/frp/releases)
