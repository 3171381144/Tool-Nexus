PORTAL_PAGE_HTML = """
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Tool Nexus Portal</title>
  <style>
    :root {
      --bg: #f4efe5;
      --panel: rgba(255, 251, 244, 0.92);
      --ink: #1a1714;
      --muted: #6f665d;
      --line: rgba(44, 36, 28, 0.14);
      --brand: #0e6b50;
      --brand-strong: #084a38;
      --accent: #c96f2d;
      --danger: #9d2f2f;
      --shadow: 0 22px 60px rgba(26, 23, 20, 0.12);
      --radius: 24px;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Segoe UI", "PingFang SC", sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, rgba(201,111,45,0.22), transparent 28%),
        radial-gradient(circle at top right, rgba(14,107,80,0.22), transparent 24%),
        linear-gradient(160deg, #f7f2e9 0%, #efe6d6 100%);
      min-height: 100vh;
    }
    .shell { width: min(1180px, calc(100% - 32px)); margin: 0 auto; padding: 28px 0 56px; }
    .hero { display: grid; grid-template-columns: 1.25fr 0.95fr; gap: 20px; margin-bottom: 22px; }
    .card { background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius); box-shadow: var(--shadow); backdrop-filter: blur(12px); }
    .hero-main { padding: 28px; position: relative; overflow: hidden; }
    .hero-main::after { content: ""; position: absolute; width: 220px; height: 220px; border-radius: 999px; background: radial-gradient(circle, rgba(14,107,80,0.22), transparent 65%); right: -40px; top: -40px; }
    .eyebrow { display: inline-flex; align-items: center; gap: 8px; padding: 8px 12px; border-radius: 999px; background: rgba(14,107,80,0.08); color: var(--brand-strong); font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; }
    h1 { margin: 18px 0 12px; font-size: clamp(34px, 5vw, 58px); line-height: 0.96; max-width: 11ch; }
    .lead { margin: 0; color: var(--muted); font-size: 16px; line-height: 1.7; max-width: 56ch; }
    .hero-side { padding: 24px; display: flex; flex-direction: column; gap: 16px; justify-content: space-between; }
    .hero-side h2, .section h2 { margin: 0 0 8px; font-size: 18px; }
    .meta-list { display: grid; gap: 12px; margin-top: 8px; }
    .meta-item { padding: 14px 16px; border-radius: 18px; background: rgba(255,255,255,0.68); border: 1px solid var(--line); }
    .meta-item strong { display: block; margin-bottom: 6px; font-size: 13px; color: var(--brand-strong); }
    .meta-item span { color: var(--muted); font-size: 14px; }
    .grid { display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 20px; }
    .section { padding: 24px; }
    .section-head { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 18px; }
    .pill { padding: 7px 12px; border-radius: 999px; font-size: 12px; background: rgba(201,111,45,0.12); color: #8c4b19; }
    .state { color: var(--muted); font-size: 14px; }
    .project-list { display: grid; gap: 14px; }
    .project { padding: 18px; border-radius: 20px; border: 1px solid var(--line); background: rgba(255,255,255,0.7); display: grid; gap: 10px; }
    .project-top { display: flex; align-items: start; justify-content: space-between; gap: 10px; }
    .project h3 { margin: 0; font-size: 18px; }
    .project small { color: var(--muted); font-size: 13px; }
    .tags { display: flex; flex-wrap: wrap; gap: 8px; }
    .tag { padding: 6px 10px; border-radius: 999px; background: rgba(14,107,80,0.1); color: var(--brand-strong); font-size: 12px; }
    .tag.private { background: rgba(157,47,47,0.1); color: var(--danger); }
    form { display: grid; gap: 14px; }
    label { display: grid; gap: 8px; font-size: 14px; color: var(--muted); }
    input, select { width: 100%; border: 1px solid rgba(44,36,28,0.14); border-radius: 14px; padding: 13px 14px; font-size: 15px; background: rgba(255,255,255,0.88); color: var(--ink); }
    input:focus, select:focus { outline: 2px solid rgba(14,107,80,0.18); border-color: rgba(14,107,80,0.42); }
    .row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
    button { border: 0; border-radius: 14px; padding: 13px 16px; font-size: 15px; font-weight: 600; cursor: pointer; }
    .primary { background: linear-gradient(135deg, var(--brand), var(--brand-strong)); color: white; }
    .secondary { background: rgba(26,23,20,0.06); color: var(--ink); }
    .inline-actions { display: flex; gap: 10px; flex-wrap: wrap; }
    .notice { margin-top: 10px; min-height: 20px; font-size: 14px; color: var(--muted); }
    .notice.error { color: var(--danger); }
    .notice.success { color: var(--brand-strong); }
    .hidden { display: none !important; }
    .empty { padding: 22px; border: 1px dashed rgba(44,36,28,0.18); border-radius: 18px; color: var(--muted); background: rgba(255,255,255,0.45); }
    .topbar { display: flex; align-items: center; justify-content: space-between; gap: 10px; margin-bottom: 18px; }
    .brandline { display: flex; align-items: center; gap: 10px; font-size: 13px; color: var(--muted); }
    .dot { width: 10px; height: 10px; border-radius: 999px; background: var(--accent); box-shadow: 18px 0 0 var(--brand); margin-right: 18px; }
    @media (max-width: 900px) { .hero, .grid, .row { grid-template-columns: 1fr; } .shell { width: min(100% - 20px, 1180px); } }
  </style>
</head>
<body>
  <div class="shell">
    <div class="topbar">
      <div class="brandline"><span class="dot"></span><span>Tool Nexus Portal</span></div>
      <div class="inline-actions">
        <button id="refreshButton" class="secondary">刷新项目</button>
        <button id="logoutButton" class="secondary hidden">退出登录</button>
        <a id="loginLink" href="/login"><button class="primary" type="button">去登录</button></a>
      </div>
    </div>
    <div class="hero">
      <section class="card hero-main">
        <span class="eyebrow">Internal Tool Mesh</span>
        <h1>一个入口，聚合全团队工具</h1>
        <p class="lead">Portal 负责统一登录、项目可见性和子域名权限控制。你可以在这里查看自己拥有或被授权的工具，并直接登记新的 FRP 子域名。</p>
      </section>
      <aside class="card hero-side">
        <div>
          <h2>当前会话</h2>
          <div class="meta-list">
            <div class="meta-item"><strong>登录状态</strong><span id="sessionStatus">检查中...</span></div>
            <div class="meta-item"><strong>当前用户</strong><span id="sessionUser">未登录</span></div>
            <div class="meta-item"><strong>建议接入方式</strong><span>先在这里登记子域名，再启动对应的 frpc 代理。</span></div>
          </div>
        </div>
      </aside>
    </div>
    <div class="grid">
      <section class="card section">
        <div class="section-head">
          <div><h2>我的项目</h2><div class="state">拥有项目、公开项目和被分享项目会统一展示在这里。</div></div>
          <span class="pill" id="projectCount">0 个项目</span>
        </div>
        <div id="projectList" class="project-list"></div>
        <div id="projectEmpty" class="empty hidden">当前还没有可见项目。你可以先创建一个新项目，或者让项目所有者给你授权。</div>
      </section>
      <section class="card section">
        <div class="section-head">
          <div><h2>登记新工具</h2><div class="state">这里的 subdomain 会直接决定 *.aim888888.xyz 的访问路由。</div></div>
          <span class="pill">Portal API</span>
        </div>
        <form id="projectForm">
          <label>工具名称<input id="projectName" name="name" placeholder="例如：模型评测台" required></label>
          <div class="row">
            <label>子域名前缀<input id="projectSubdomain" name="subdomain" placeholder="例如：demo-tool" required pattern="[a-z0-9-]+"></label>
            <label>可见性<select id="projectVisibility" name="is_private"><option value="true">私有</option><option value="false">公开（任何已登录用户可访问）</option></select></label>
          </div>
          <button class="primary" type="submit">创建项目</button>
          <div id="formNotice" class="notice"></div>
        </form>
      </section>
    </div>
  </div>
  <script>
    const state = { authenticated: false, user: null, projects: [] };
    const sessionStatus = document.getElementById('sessionStatus');
    const sessionUser = document.getElementById('sessionUser');
    const projectList = document.getElementById('projectList');
    const projectEmpty = document.getElementById('projectEmpty');
    const projectCount = document.getElementById('projectCount');
    const formNotice = document.getElementById('formNotice');
    const projectForm = document.getElementById('projectForm');
    const logoutButton = document.getElementById('logoutButton');
    const loginLink = document.getElementById('loginLink');
    const refreshButton = document.getElementById('refreshButton');
    function setNotice(element, message, kind = '') { element.textContent = message || ''; element.className = 'notice' + (kind ? ' ' + kind : ''); }
    function renderSession() {
      if (state.authenticated && state.user) {
        sessionStatus.textContent = '已登录';
        sessionUser.textContent = state.user.username + ' (ID ' + state.user.id + ')';
        logoutButton.classList.remove('hidden');
        loginLink.classList.add('hidden');
        projectForm.classList.remove('hidden');
      } else {
        sessionStatus.textContent = '未登录';
        sessionUser.textContent = '请先登录 Portal';
        logoutButton.classList.add('hidden');
        loginLink.classList.remove('hidden');
        projectForm.classList.add('hidden');
        setNotice(formNotice, '登录后才能登记新项目。');
      }
    }
    function accessLabel(accessType) { return accessType === 'owner' ? '所有者' : accessType === 'shared' ? '授权访问' : accessType === 'public' ? '公开项目' : accessType; }
    function renderProjects() {
      projectList.innerHTML = '';
      projectCount.textContent = state.projects.length + ' 个项目';
      projectEmpty.classList.toggle('hidden', state.projects.length > 0);
      for (const project of state.projects) {
        const article = document.createElement('article');
        article.className = 'project';
        const host = project.subdomain + '.aim888888.xyz';
        article.innerHTML = '<div class="project-top"><div><h3>' + project.name + '</h3><small>' + host + '</small></div><a href="https://' + host + '" target="_blank" rel="noreferrer">打开工具</a></div><div class="tags"><span class="tag">' + accessLabel(project.access_type) + '</span><span class="tag ' + (project.is_private ? 'private' : '') + '">' + (project.is_private ? '私有' : '公开') + '</span><span class="tag">Owner: ' + project.owner_username + '</span></div>';
        projectList.appendChild(article);
      }
    }
    async function fetchJson(url, options = {}) {
      const response = await fetch(url, { credentials: 'include', headers: { 'Content-Type': 'application/json', ...(options.headers || {}) }, ...options });
      const text = await response.text();
      let payload = null;
      try { payload = text ? JSON.parse(text) : null; } catch { payload = { message: text }; }
      if (!response.ok) throw new Error(payload?.detail || payload?.message || '请求失败');
      return payload;
    }
    async function loadSession() {
      const session = await fetchJson('/api/me', { method: 'GET' });
      state.authenticated = session.authenticated;
      state.user = session.user;
      renderSession();
    }
    async function loadProjects() {
      if (!state.authenticated) { state.projects = []; renderProjects(); return; }
      state.projects = await fetchJson('/api/my-projects', { method: 'GET' });
      renderProjects();
    }
    refreshButton.addEventListener('click', async () => { try { await loadSession(); await loadProjects(); } catch (error) { setNotice(formNotice, error.message, 'error'); } });
    logoutButton.addEventListener('click', async () => { try { await fetchJson('/api/logout', { method: 'POST' }); state.authenticated = false; state.user = null; state.projects = []; renderSession(); renderProjects(); } catch (error) { setNotice(formNotice, error.message, 'error'); } });
    projectForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      setNotice(formNotice, '正在创建项目...');
      const payload = { name: document.getElementById('projectName').value.trim(), subdomain: document.getElementById('projectSubdomain').value.trim(), is_private: document.getElementById('projectVisibility').value === 'true' };
      try {
        await fetchJson('/api/projects', { method: 'POST', body: JSON.stringify(payload) });
        projectForm.reset();
        setNotice(formNotice, '项目创建成功。接下来把 frpc 的 customDomains 指向这个子域名。', 'success');
        await loadProjects();
      } catch (error) {
        setNotice(formNotice, error.message, 'error');
      }
    });
    (async () => { try { await loadSession(); await loadProjects(); } catch (error) { setNotice(formNotice, error.message, 'error'); } })();
  </script>
</body>
</html>
"""

LOGIN_PAGE_HTML = """
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>登录 Tool Nexus Portal</title>
  <style>
    :root { --panel: rgba(250, 244, 235, 0.92); --ink: #191611; --muted: #6b655d; --brand: #0d7b59; --brand-strong: #08563f; --danger: #ad3434; --line: rgba(28, 24, 19, 0.12); --shadow: 0 26px 80px rgba(0,0,0,0.28); }
    * { box-sizing: border-box; }
    body { margin: 0; min-height: 100vh; display: grid; place-items: center; padding: 20px; font-family: "Segoe UI", "PingFang SC", sans-serif; background: radial-gradient(circle at top left, rgba(214,122,50,0.3), transparent 30%), radial-gradient(circle at bottom right, rgba(13,123,89,0.34), transparent 30%), linear-gradient(145deg, #111518 0%, #1d2428 100%); }
    .login-shell { width: min(100%, 1040px); display: grid; grid-template-columns: 1.05fr 0.95fr; background: var(--panel); border-radius: 30px; overflow: hidden; box-shadow: var(--shadow); }
    .left { padding: 42px; background: linear-gradient(160deg, rgba(13,123,89,0.12), rgba(214,122,50,0.12)), #f7f0e5; }
    .right { padding: 42px; background: rgba(255,255,255,0.72); }
    .eyebrow { display: inline-block; padding: 8px 12px; border-radius: 999px; background: rgba(13,123,89,0.1); color: var(--brand-strong); font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; }
    h1 { margin: 18px 0 12px; font-size: clamp(32px, 5vw, 54px); line-height: 0.98; color: var(--ink); }
    p { color: var(--muted); line-height: 1.7; font-size: 15px; margin: 0 0 16px; }
    .info-grid { display: grid; gap: 12px; margin-top: 24px; }
    .info { padding: 16px; border-radius: 18px; background: rgba(255,255,255,0.66); border: 1px solid var(--line); }
    .info strong { display: block; margin-bottom: 6px; }
    form { display: grid; gap: 14px; margin-top: 18px; }
    label { display: grid; gap: 8px; font-size: 14px; color: var(--muted); }
    input { border: 1px solid var(--line); border-radius: 14px; padding: 14px; font-size: 15px; background: rgba(255,255,255,0.92); }
    button { border: 0; border-radius: 14px; padding: 14px 16px; font-size: 15px; font-weight: 700; cursor: pointer; color: white; background: linear-gradient(135deg, var(--brand), var(--brand-strong)); }
    .notice { min-height: 20px; font-size: 14px; color: var(--muted); }
    .notice.error { color: var(--danger); }
    .notice.success { color: var(--brand-strong); }
    .back { display: inline-flex; margin-top: 18px; color: var(--brand-strong); text-decoration: none; font-weight: 600; }
    @media (max-width: 900px) { .login-shell { grid-template-columns: 1fr; } .left, .right { padding: 28px; } }
  </style>
</head>
<body>
  <div class="login-shell">
    <section class="left">
      <span class="eyebrow">Portal Access</span>
      <h1>登录后再进入团队工具子域名</h1>
      <p>Tool Nexus Portal 负责单点登录、子域名路由授权和跨工具访问控制。完成登录后，你可以回到原始工具地址继续访问。</p>
      <div class="info-grid">
        <div class="info"><strong>测试账号</strong>张三 / zhangsan123<br>李四 / lisi123<br>王五 / wangwu123</div>
        <div class="info"><strong>登录后会发生什么</strong>Portal 会写入跨子域 HttpOnly Cookie，随后 `*.aim888888.xyz` 的访问会先经过 `/api/auth` 校验。</div>
      </div>
    </section>
    <section class="right">
      <h2>进入 Portal</h2>
      <p>如果你是从工具页跳转过来的，登录成功后会自动返回原地址。</p>
      <form id="loginForm">
        <label>用户名<input id="username" autocomplete="username" value="张三" required></label>
        <label>密码<input id="password" type="password" autocomplete="current-password" value="zhangsan123" required></label>
        <button type="submit">登录并继续</button>
        <div id="loginNotice" class="notice"></div>
      </form>
      <a class="back" href="/">返回门户首页</a>
    </section>
  </div>
  <script>
    const params = new URLSearchParams(window.location.search);
    const nextUrl = params.get('next') || '/';
    const notice = document.getElementById('loginNotice');
    function setNotice(message, kind = '') { notice.textContent = message || ''; notice.className = 'notice' + (kind ? ' ' + kind : ''); }
    async function fetchJson(url, options = {}) {
      const response = await fetch(url, { credentials: 'include', headers: { 'Content-Type': 'application/json', ...(options.headers || {}) }, ...options });
      const text = await response.text();
      let payload = null;
      try { payload = text ? JSON.parse(text) : null; } catch { payload = { message: text }; }
      if (!response.ok) throw new Error(payload?.detail || payload?.message || '请求失败');
      return payload;
    }
    async function checkSession() {
      try {
        const session = await fetchJson('/api/me', { method: 'GET' });
        if (session.authenticated) { window.location.href = nextUrl; }
      } catch {}
    }
    document.getElementById('loginForm').addEventListener('submit', async (event) => {
      event.preventDefault();
      setNotice('正在登录...');
      try {
        await fetchJson('/api/login', { method: 'POST', body: JSON.stringify({ username: document.getElementById('username').value.trim(), password: document.getElementById('password').value }) });
        setNotice('登录成功，正在跳转...', 'success');
        window.location.href = nextUrl;
      } catch (error) { setNotice(error.message, 'error'); }
    });
    checkSession();
  </script>
</body>
</html>
"""
