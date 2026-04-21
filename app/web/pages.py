PORTAL_PAGE_HTML = """
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Tool Nexus Portal</title>
  <style>
    :root {
      --ink: #17201b;
      --muted: #6d756e;
      --paper: #fffaf0;
      --paper-2: rgba(255, 250, 240, 0.82);
      --line: rgba(23, 32, 27, 0.14);
      --green: #155f43;
      --green-2: #0b3d2b;
      --lime: #d8f15f;
      --orange: #d77a32;
      --red: #b83c3c;
      --blue: #305c80;
      --shadow: 0 24px 80px rgba(23, 32, 27, 0.14);
      --radius: 26px;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      font-family: "Aptos", "Segoe UI", "PingFang SC", sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at 8% 12%, rgba(216, 241, 95, 0.55), transparent 26%),
        radial-gradient(circle at 92% 8%, rgba(48, 92, 128, 0.22), transparent 28%),
        radial-gradient(circle at 72% 92%, rgba(215, 122, 50, 0.2), transparent 30%),
        linear-gradient(135deg, #edf0df 0%, #efe3cf 52%, #dce5d8 100%);
    }
    a { color: var(--green); font-weight: 700; text-decoration: none; }
    button { border: 0; border-radius: 16px; padding: 12px 16px; font-size: 14px; font-weight: 800; cursor: pointer; transition: transform .16s ease, box-shadow .16s ease; }
    button:hover { transform: translateY(-1px); }
    button:disabled { cursor: not-allowed; opacity: .55; transform: none; }
    input, select {
      width: 100%; border: 1px solid var(--line); border-radius: 16px; padding: 13px 14px;
      font: inherit; background: rgba(255,255,255,.78); color: var(--ink);
    }
    input:focus, select:focus { outline: 3px solid rgba(21,95,67,.16); border-color: rgba(21,95,67,.5); }
    label { display: grid; gap: 7px; color: var(--muted); font-size: 13px; font-weight: 700; }
    .shell { width: min(1360px, calc(100% - 34px)); margin: 0 auto; padding: 26px 0 64px; }
    .topbar { display: flex; justify-content: space-between; align-items: center; gap: 14px; margin-bottom: 20px; }
    .brand { display: flex; align-items: center; gap: 12px; font-weight: 900; letter-spacing: .02em; }
    .mark { width: 38px; height: 38px; border-radius: 13px; background: linear-gradient(135deg, var(--green), var(--lime)); box-shadow: inset -10px -10px 0 rgba(0,0,0,.08); }
    .actions { display: flex; gap: 10px; flex-wrap: wrap; justify-content: flex-end; }
    .primary { background: linear-gradient(135deg, var(--green), var(--green-2)); color: white; box-shadow: 0 14px 30px rgba(21,95,67,.22); }
    .secondary { background: rgba(255,255,255,.62); color: var(--ink); border: 1px solid var(--line); }
    .danger { background: rgba(184,60,60,.12); color: var(--red); border: 1px solid rgba(184,60,60,.18); }
    .layout { display: grid; grid-template-columns: 1.1fr .9fr; gap: 20px; align-items: start; }
    .hero { grid-column: 1 / -1; display: grid; grid-template-columns: 1.25fr .75fr; gap: 20px; }
    .card { background: var(--paper-2); border: 1px solid var(--line); border-radius: var(--radius); box-shadow: var(--shadow); backdrop-filter: blur(18px); }
    .hero-main { position: relative; overflow: hidden; padding: 34px; min-height: 260px; }
    .hero-main::after { content:""; position:absolute; width: 320px; height: 320px; border-radius: 999px; right: -80px; top: -100px; background: radial-gradient(circle, rgba(216,241,95,.72), transparent 62%); }
    .eyebrow { display:inline-flex; align-items:center; gap:8px; padding:8px 12px; border-radius:999px; color: var(--green-2); background: rgba(21,95,67,.08); font-size:12px; font-weight:900; letter-spacing:.12em; text-transform:uppercase; }
    h1 { position:relative; z-index:1; margin: 18px 0 12px; max-width: 10ch; font-size: clamp(42px, 6vw, 82px); line-height: .88; letter-spacing: -.06em; }
    .lead { position:relative; z-index:1; margin:0; color: var(--muted); font-size: 16px; line-height: 1.75; max-width: 60ch; }
    .session { padding: 24px; display:grid; gap:14px; }
    .metric { padding: 16px; border-radius: 20px; border:1px solid var(--line); background: rgba(255,255,255,.62); }
    .metric small { display:block; color: var(--green); font-weight:900; margin-bottom: 6px; }
    .metric span { color: var(--muted); }
    .panel { padding: 24px; }
    .panel-head { display:flex; justify-content:space-between; gap:14px; align-items:start; margin-bottom:18px; }
    .panel h2 { margin:0 0 6px; font-size: 22px; letter-spacing: -.02em; }
    .hint { margin:0; color: var(--muted); font-size: 14px; line-height:1.55; }
    .pill { display:inline-flex; align-items:center; padding:7px 12px; border-radius:999px; background: rgba(215,122,50,.13); color:#8b4c1d; font-size:12px; font-weight:900; white-space:nowrap; }
    .project-list { display:grid; gap: 14px; }
    .project { padding: 18px; border-radius: 22px; background: rgba(255,255,255,.68); border:1px solid var(--line); }
    .project-top { display:flex; justify-content:space-between; gap:14px; align-items:start; }
    .project h3 { margin:0 0 6px; font-size:19px; }
    .host { color: var(--muted); font-size: 13px; word-break: break-all; }
    .tags { display:flex; flex-wrap:wrap; gap:8px; margin-top:14px; }
    .tag { padding:6px 10px; border-radius:999px; font-size:12px; font-weight:800; color:var(--green-2); background:rgba(21,95,67,.1); }
    .tag.private { color: var(--red); background:rgba(184,60,60,.1); }
    .tag.blue { color: var(--blue); background: rgba(48,92,128,.1); }
    form { display:grid; gap:14px; }
    .row { display:grid; grid-template-columns: 1fr 1fr; gap:12px; }
    .notice { min-height:20px; font-size:14px; color:var(--muted); }
    .notice.error { color: var(--red); }
    .notice.success { color: var(--green); }
    .empty { padding: 22px; border-radius: 20px; border:1px dashed rgba(23,32,27,.22); color:var(--muted); background:rgba(255,255,255,.48); }
    .hidden { display:none !important; }
    .whitelist { display:grid; gap:10px; padding:14px; border-radius:20px; border:1px solid var(--line); background:rgba(255,255,255,.5); }
    .whitelist-grid { display:grid; grid-template-columns: repeat(auto-fill, minmax(145px, 1fr)); gap:9px; }
    .check-card { display:flex; align-items:center; gap:9px; padding:10px 11px; border-radius:14px; background:rgba(255,255,255,.76); border:1px solid var(--line); color: var(--ink); font-size: 13px; font-weight: 800; }
    .check-card input { width:auto; }
    .user-list { display:grid; gap:9px; }
    .user-row { display:flex; justify-content:space-between; gap:10px; padding:12px 14px; border-radius:16px; border:1px solid var(--line); background:rgba(255,255,255,.58); }
    .config-box { margin-top:16px; padding:14px; border-radius:18px; background:#17201b; color:#e9f3df; overflow:auto; font: 12px/1.65 "Cascadia Mono", Consolas, monospace; }
    @media (max-width: 980px) { .layout, .hero { grid-template-columns: 1fr; } .row { grid-template-columns:1fr; } h1 { max-width: 12ch; } }
  </style>
</head>
<body>
  <main class="shell">
    <nav class="topbar">
      <div class="brand"><span class="mark"></span><span>Tool Nexus</span></div>
      <div class="actions">
        <button id="refreshButton" class="secondary">??</button>
        <button id="logoutButton" class="secondary hidden">????</button>
        <a id="loginLink" href="/login"><button class="primary" type="button">??</button></a>
      </div>
    </nav>

    <section class="hero">
      <div class="card hero-main">
        <span class="eyebrow">Internal Tool Gateway</span>
        <h1>????????????????</h1>
        <p class="lead">???????????????????????????Portal ????????frp ?????????????????????</p>
      </div>
      <aside class="card session">
        <div class="metric"><small>????</small><span id="sessionStatus">???...</span></div>
        <div class="metric"><small>????</small><span id="sessionUser">???</span></div>
        <div class="metric"><small>FRP ??</small><span>frp.aim888888.xyz:7000</span></div>
      </aside>
    </section>

    <section class="layout">
      <div class="card panel">
        <div class="panel-head">
          <div><h2>????</h2><p class="hint">??????????????????????</p></div>
          <span class="pill" id="projectCount">0 ???</span>
        </div>
        <div id="projectList" class="project-list"></div>
        <div id="projectEmpty" class="empty hidden">??????????????????????????????</div>
      </div>

      <div style="display:grid; gap:20px;">
        <section class="card panel">
          <div class="panel-head">
            <div><h2>?????</h2><p class="hint">?????????????????????????????</p></div>
            <span class="pill">??</span>
          </div>
          <form id="projectForm">
            <label>????<input id="projectName" placeholder="??????????" required></label>
            <div class="row">
              <label>?????<input id="projectSubdomain" placeholder="???zhangsan-tool" required pattern="[a-z0-9-]+"></label>
              <label>???<select id="projectVisibility"><option value="true">???? owner + ???</option><option value="false">?????????</option></select></label>
            </div>
            <div id="whitelistBox" class="whitelist">
              <div><strong>?????</strong><p class="hint">owner ??????????????</p></div>
              <div id="whitelistUsers" class="whitelist-grid"></div>
            </div>
            <button class="primary" type="submit">????</button>
            <div id="formNotice" class="notice"></div>
          </form>
          <pre id="configPreview" class="config-box">????????????? frpc.toml ????? customDomains?</pre>
        </section>

        <section class="card panel">
          <div class="panel-head">
            <div><h2>????</h2><p class="hint">???????????????????</p></div>
            <span class="pill" id="userCount">0 ???</span>
          </div>
          <form id="userForm">
            <div class="row">
              <label>???<input id="newUsername" placeholder="???wangwu" required></label>
              <label>????<input id="newPassword" type="password" placeholder="?? 6 ?" required minlength="6"></label>
            </div>
            <button class="secondary" type="submit">????</button>
            <div id="userNotice" class="notice"></div>
          </form>
          <div id="userList" class="user-list" style="margin-top:14px;"></div>
        </section>
      </div>
    </section>
  </main>

  <script>
    const state = { authenticated: false, user: null, projects: [], users: [] };
    const $ = (id) => document.getElementById(id);
    const sessionStatus = $('sessionStatus');
    const sessionUser = $('sessionUser');
    const projectList = $('projectList');
    const projectEmpty = $('projectEmpty');
    const projectCount = $('projectCount');
    const userCount = $('userCount');
    const userList = $('userList');
    const whitelistUsers = $('whitelistUsers');
    const whitelistBox = $('whitelistBox');
    const projectVisibility = $('projectVisibility');
    const formNotice = $('formNotice');
    const userNotice = $('userNotice');
    const configPreview = $('configPreview');
    const loginLink = $('loginLink');
    const logoutButton = $('logoutButton');

    function setNotice(el, message, kind = '') { el.textContent = message || ''; el.className = 'notice' + (kind ? ' ' + kind : ''); }
    function escapeHtml(value) { return String(value).replace(/[&<>"]/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[ch])); }
    async function fetchJson(url, options = {}) {
      const headers = options.body ? { 'Content-Type': 'application/json', ...(options.headers || {}) } : (options.headers || {});
      const response = await fetch(url, { credentials: 'include', ...options, headers });
      const text = await response.text();
      let payload = null;
      try { payload = text ? JSON.parse(text) : null; } catch { payload = { message: text }; }
      if (!response.ok) throw new Error(payload?.detail || payload?.message || '????');
      return payload;
    }
    function renderSession() {
      if (state.authenticated && state.user) {
        sessionStatus.textContent = '???';
        sessionUser.textContent = `${state.user.username} (ID ${state.user.id})`;
        loginLink.classList.add('hidden');
        logoutButton.classList.remove('hidden');
      } else {
        sessionStatus.textContent = '???';
        sessionUser.textContent = '???? Portal';
        loginLink.classList.remove('hidden');
        logoutButton.classList.add('hidden');
      }
    }
    function accessLabel(value) { return value === 'owner' ? '???' : value === 'shared' ? '???' : value === 'public' ? '??' : value; }
    function renderProjects() {
      projectList.innerHTML = '';
      projectCount.textContent = `${state.projects.length} ???`;
      projectEmpty.classList.toggle('hidden', state.projects.length > 0);
      for (const project of state.projects) {
        const host = `${project.subdomain}.aim888888.xyz`;
        const granted = (project.granted_users || []).map(u => escapeHtml(u.username)).join('?') || '?';
        const article = document.createElement('article');
        article.className = 'project';
        article.innerHTML = `
          <div class="project-top">
            <div><h3>${escapeHtml(project.name)}</h3><div class="host">${host}</div></div>
            <a href="https://${host}" target="_blank" rel="noreferrer">????</a>
          </div>
          <div class="tags">
            <span class="tag">${accessLabel(project.access_type)}</span>
            <span class="tag ${project.is_private ? 'private' : ''}">${project.is_private ? '??' : '??'}</span>
            <span class="tag blue">Owner: ${escapeHtml(project.owner_username)}</span>
            <span class="tag blue">???: ${granted}</span>
          </div>`;
        projectList.appendChild(article);
      }
    }
    function renderUsers() {
      userCount.textContent = `${state.users.length} ???`;
      userList.innerHTML = '';
      whitelistUsers.innerHTML = '';
      for (const user of state.users) {
        const row = document.createElement('div');
        row.className = 'user-row';
        row.innerHTML = `<strong>${escapeHtml(user.username)}</strong><span class="hint">ID ${user.id}</span>`;
        userList.appendChild(row);
        if (!state.user || user.id === state.user.id) continue;
        const label = document.createElement('label');
        label.className = 'check-card';
        label.innerHTML = `<input type="checkbox" value="${user.id}"><span>${escapeHtml(user.username)}</span>`;
        whitelistUsers.appendChild(label);
      }
      if (!whitelistUsers.children.length) whitelistUsers.innerHTML = '<div class="hint">????????????????</div>';
    }
    function renderVisibility() { whitelistBox.classList.toggle('hidden', projectVisibility.value !== 'true'); }
    async function loadSession() { const data = await fetchJson('/api/me'); state.authenticated = data.authenticated; state.user = data.user; renderSession(); }
    async function loadUsers() { if (!state.authenticated) return; state.users = await fetchJson('/api/users'); renderUsers(); }
    async function loadProjects() { if (!state.authenticated) return; state.projects = await fetchJson('/api/my-projects'); renderProjects(); }
    async function reloadAll() { await loadSession(); if (state.authenticated) { await loadUsers(); await loadProjects(); } }

    $('refreshButton').addEventListener('click', async () => { try { await reloadAll(); } catch (e) { setNotice(formNotice, e.message, 'error'); } });
    logoutButton.addEventListener('click', async () => { await fetchJson('/api/logout', { method: 'POST' }); location.href = '/login'; });
    projectVisibility.addEventListener('change', renderVisibility);
    $('projectForm').addEventListener('submit', async (event) => {
      event.preventDefault();
      const subdomain = $('projectSubdomain').value.trim().toLowerCase();
      const isPrivate = projectVisibility.value === 'true';
      const whitelist_user_ids = isPrivate ? [...whitelistUsers.querySelectorAll('input:checked')].map(input => Number(input.value)) : [];
      const payload = { name: $('projectName').value.trim(), subdomain, is_private: isPrivate, whitelist_user_ids };
      try {
        setNotice(formNotice, '??????...');
        await fetchJson('/api/projects', { method: 'POST', body: JSON.stringify(payload) });
        setNotice(formNotice, '???????', 'success');
        configPreview.textContent = `customDomains = ["${subdomain}.aim888888.xyz"]\n\n?? frpc.toml ? localPort ?????????`;
        event.target.reset();
        renderVisibility();
        await loadProjects();
      } catch (e) { setNotice(formNotice, e.message, 'error'); }
    });
    $('userForm').addEventListener('submit', async (event) => {
      event.preventDefault();
      const payload = { username: $('newUsername').value.trim(), password: $('newPassword').value };
      try {
        setNotice(userNotice, '??????...');
        await fetchJson('/api/users', { method: 'POST', body: JSON.stringify(payload) });
        setNotice(userNotice, '???????', 'success');
        event.target.reset();
        await loadUsers();
      } catch (e) { setNotice(userNotice, e.message, 'error'); }
    });
    renderVisibility();
    reloadAll().catch(e => setNotice(formNotice, e.message, 'error'));
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
  <title>?? Tool Nexus Portal</title>
  <style>
    :root { --ink:#111916; --muted:#69726c; --green:#155f43; --green2:#0b3d2b; --lime:#d8f15f; --line:rgba(17,25,22,.14); --red:#b83c3c; }
    * { box-sizing:border-box; }
    body { margin:0; min-height:100vh; display:grid; place-items:center; padding:20px; font-family:"Aptos","Segoe UI","PingFang SC",sans-serif; color:var(--ink); background:radial-gradient(circle at 20% 10%, rgba(216,241,95,.55), transparent 28%), radial-gradient(circle at 82% 84%, rgba(21,95,67,.32), transparent 30%), linear-gradient(145deg,#121a18,#29352f); }
    .box { width:min(980px,100%); display:grid; grid-template-columns:1.05fr .95fr; border-radius:30px; overflow:hidden; box-shadow:0 28px 90px rgba(0,0,0,.32); background:#fff8ea; }
    .intro { padding:42px; background:linear-gradient(150deg, rgba(216,241,95,.28), rgba(255,255,255,.55)); }
    .form { padding:42px; background:rgba(255,255,255,.72); }
    .eyebrow { display:inline-flex; padding:8px 12px; border-radius:999px; background:rgba(21,95,67,.1); color:var(--green2); font-size:12px; font-weight:900; letter-spacing:.12em; text-transform:uppercase; }
    h1 { margin:18px 0 12px; font-size:clamp(36px,5vw,66px); line-height:.9; letter-spacing:-.06em; }
    p { color:var(--muted); line-height:1.7; }
    label { display:grid; gap:8px; margin-bottom:14px; color:var(--muted); font-size:14px; font-weight:800; }
    input { width:100%; border:1px solid var(--line); border-radius:16px; padding:14px; font:inherit; }
    button { width:100%; border:0; border-radius:16px; padding:14px 16px; font-weight:900; color:white; background:linear-gradient(135deg,var(--green),var(--green2)); cursor:pointer; }
    .notice { min-height:22px; margin-top:12px; color:var(--muted); }
    .notice.error { color:var(--red); }
    .notice.success { color:var(--green); }
    .accounts { margin-top:24px; padding:16px; border-radius:18px; border:1px solid var(--line); background:rgba(255,255,255,.58); color:var(--muted); line-height:1.8; }
    a { color:var(--green); font-weight:900; text-decoration:none; display:inline-block; margin-top:18px; }
    @media (max-width:820px){ .box{grid-template-columns:1fr;} .intro,.form{padding:28px;} }
  </style>
</head>
<body>
  <main class="box">
    <section class="intro">
      <span class="eyebrow">Tool Nexus Login</span>
      <h1>??????????????</h1>
      <p>??? Portal ?????? Cookie?????????????????? `/api/auth` ?????????</p>
      <div class="accounts"><strong>????</strong><br>zhangsan / zhangsan123<br>lisi / lisi123<br>wangwu / wangwu123</div>
    </section>
    <section class="form">
      <h2>?? Portal</h2>
      <p>??????????????????????????</p>
      <form id="loginForm">
        <label>???<input id="username" autocomplete="username" value="zhangsan" required></label>
        <label>??<input id="password" type="password" autocomplete="current-password" value="zhangsan123" required></label>
        <button type="submit">?????</button>
        <div id="notice" class="notice"></div>
      </form>
      <a href="/">??????</a>
    </section>
  </main>
  <script>
    const params = new URLSearchParams(location.search);
    const nextUrl = params.get('next') || '/';
    const notice = document.getElementById('notice');
    function setNotice(message, kind='') { notice.textContent = message || ''; notice.className = 'notice' + (kind ? ' ' + kind : ''); }
    async function fetchJson(url, options={}) {
      const response = await fetch(url, { credentials:'include', headers:{'Content-Type':'application/json'}, ...options });
      const text = await response.text();
      let payload = null;
      try { payload = text ? JSON.parse(text) : null; } catch { payload = { message:text }; }
      if (!response.ok) throw new Error(payload?.detail || payload?.message || '????');
      return payload;
    }
    document.getElementById('loginForm').addEventListener('submit', async (event) => {
      event.preventDefault();
      try {
        setNotice('????...');
        await fetchJson('/api/login', { method:'POST', body: JSON.stringify({ username: document.getElementById('username').value.trim(), password: document.getElementById('password').value }) });
        setNotice('?????????...', 'success');
        location.href = nextUrl;
      } catch (e) { setNotice(e.message, 'error'); }
    });
  </script>
</body>
</html>
"""
