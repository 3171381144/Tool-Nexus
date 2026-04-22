Tool-Nexus client package

Files needed:
- frpc.exe
- start.bat
- configure-frpc.ps1
- frpc.toml, optional but recommended if admin prefilled auth.token

How to use:
1. Start your local web projects.
2. Confirm each local page works, for example:
   http://127.0.0.1:8077/management.html#/
   http://127.0.0.1:8019/
3. Double click start.bat.
4. First run: enter how many projects you want to expose, then fill each project.
5. Later runs with existing frpc.toml:
   Press Enter / S = start directly
   A = add more projects
   R = rebuild all config
6. Keep the frpc window open.
7. Open the printed public URLs, for example:
   https://webxkk.aim888888.xyz/management.html#/

One member only needs one frpc.exe and one frpc.toml. Multiple projects are written as multiple [[proxies]] blocks.

If auth.token is still change-this-frp-token, ask admin for the real FRP token.

Common errors:
- powered by frp 404: frpc did not register the domain. Check token, domain, and logs.
- Vite host blocked: add .aim888888.xyz to server.allowedHosts in vite.config.

frp docs: https://gofrp.org/en/docs/setup/
frp download: https://github.com/fatedier/frp/releases
