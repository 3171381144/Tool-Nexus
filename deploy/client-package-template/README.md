# Team member client package

Put these files in one folder:

- frpc.exe
- start.bat
- configure-frpc.ps1
- frpc.toml, optional. If it already contains the real auth.token, the script will keep it.

## How to use

1. Start your local web project first.
2. Confirm every local page works in your browser, for example:

```text
http://127.0.0.1:8077/management.html#/
http://127.0.0.1:8019/
```

3. Double click `start.bat`.
4. First run: enter how many projects you want to expose, then fill each project.
5. Later runs with existing `frpc.toml`:

```text
Press Enter / S = start directly with existing config
A = add more project(s)
R = rebuild all config
```

For each new project, enter:

```text
Local web URL: http://127.0.0.1:8077/management.html#/
Project name: cpa-proxy
Subdomain or full domain: webxkk
```

The script writes one `frpc.toml` with one or more `[[proxies]]` entries and starts `frpc.exe`.
Keep the command window open while you want the public URLs to stay available.

## Multi-project rule

One member only needs one `frpc.exe` and one `frpc.toml`.
Multiple tools are written into the same `frpc.toml` as multiple `[[proxies]]` blocks.

Example result:

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

## Domain rule

You can enter either:

```text
webxkk
```

or:

```text
webxkk.aim888888.xyz
```

Both become:

```text
https://webxkk.aim888888.xyz
```

If your real local page is:

```text
http://127.0.0.1:8077/management.html#/
```

then open:

```text
https://webxkk.aim888888.xyz/management.html#/
```

## Token

If `frpc.toml` already has the real `auth.token`, the script keeps it.
If it is still `change-this-frp-token`, ask the administrator for the FRP token.

## Common errors

- `The page you requested was not found. powered by frp`: `frpc` did not register this domain. Check token, domain spelling, and `start proxy success` in logs.
- `Blocked request. This host is not allowed`: Vite blocked the public host. Add `.aim888888.xyz` to `server.allowedHosts` in `vite.config.ts/js`.
- Public page opens but content is wrong: check the local port in the local URL you entered.

## Official frp links

- Docs: https://gofrp.org/en/docs/setup/
- Releases: https://github.com/fatedier/frp/releases
