Tool-Nexus client package

Put these files in one folder:

- frpc.exe
- frpc.toml
- start.bat

How to use:

1. Start your local web project first.
2. Confirm it works locally, for example:
   http://127.0.0.1:3000
3. Copy frpc.toml.template to frpc.toml.
4. Ask the admin for:
   - FRP token
   - subdomain
   - public URL
5. Edit frpc.toml:
   - auth.token
   - name
   - localPort
   - customDomains
6. Double click start.bat.
7. Keep the window open.
8. Open your public URL, for example:
   https://zhangsan-tool.aim888888.xyz

Example frpc.toml:

serverAddr = "frp.aim888888.xyz"
serverPort = 7000
auth.token = "your-real-token"
transport.tls.enable = true

[[proxies]]
name = "zhangsan-tool"
type = "http"
localIP = "127.0.0.1"
localPort = 3000
customDomains = ["zhangsan-tool.aim888888.xyz"]

Do not close the frpc window while you want the public URL to stay available.
