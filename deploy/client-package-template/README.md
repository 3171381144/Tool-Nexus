# 成员接入包模板

这个目录用于给团队成员制作接入包。

不要把真实 `auth.token` 提交到仓库。

## 文件说明

- `frpc.toml.template`：配置模板
- `start.bat`：Windows 双击启动脚本
- `README.txt`：发给成员的极简说明

## 制作成员专属接入包

例如给张三制作：

```text
tool-nexus-client-zhangsan/
  frpc.exe
  frpc.toml
  start.bat
  README.txt
```

步骤：

1. 从 frp 官方 release 下载 Windows 版 `frpc.exe`
2. 复制 `start.bat` 和 `README.txt`
3. 复制 `frpc.toml.template` 为 `frpc.toml`
4. 替换 `frpc.toml` 里的：
   - `CHANGE_ME_FRP_TOKEN`
   - `CHANGE_ME_SUBDOMAIN`
   - `localPort`
5. 在 Portal 里创建同名子域名项目
6. 把整个文件夹压缩后发给成员

## frp 官方地址

- 文档：https://gofrp.org/en/docs/setup/
- 下载：https://github.com/fatedier/frp/releases
