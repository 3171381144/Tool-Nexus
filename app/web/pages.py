PORTAL_PAGE_HTML = """
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Tool Nexus Portal</title>
  <style>
    :root { --navy:#062443; --navy2:#0e3762; --bg:#f6f8fc; --side:#f0f3f8; --card:#ffffff; --line:#e6ebf2; --text:#0b223d; --muted:#748296; --blue:#2563eb; --green:#16a34a; --red:#dc2626; --shadow:0 18px 48px rgba(6,36,67,.08); }
    * { box-sizing:border-box; }
    body { margin:0; min-height:100vh; background:var(--bg); color:var(--text); font-family:"Microsoft YaHei","PingFang SC","Noto Sans SC","Segoe UI",sans-serif; }
    button,input,select { font:inherit; } a { color:inherit; text-decoration:none; }
    .topbar { height:72px; background:var(--navy); color:#fff; display:flex; align-items:center; justify-content:space-between; padding:0 30px; box-shadow:0 10px 30px rgba(6,36,67,.18); position:sticky; top:0; z-index:20; }
    .brand { display:flex; align-items:center; gap:12px; font-weight:900; font-size:20px; letter-spacing:.02em; }
    .brand-mark { width:34px; height:34px; border-radius:10px; background:#dbeafe; color:var(--navy); display:grid; place-items:center; font-weight:900; }
    .top-actions { display:flex; align-items:center; gap:12px; }
    .top-link { font-weight:800; padding:10px 8px; border-bottom:2px solid transparent; }
    .top-link.active { border-color:#fff; }
    .btn { border:0; border-radius:14px; padding:12px 18px; font-weight:900; cursor:pointer; }
    .btn-primary { background:var(--navy); color:#fff; box-shadow:0 14px 28px rgba(6,36,67,.18); }
    .btn-soft { background:#f1f5f9; color:var(--navy); }
    .btn-line { background:#fff; color:var(--navy); border:1px solid var(--line); }
    .user-chip { display:flex; align-items:center; gap:10px; padding:9px 14px; border-radius:14px; background:rgba(255,255,255,.1); font-weight:800; }
    .avatar { width:36px; height:36px; border-radius:999px; background:#bfdbfe; color:var(--navy); display:grid; place-items:center; font-weight:900; }
    .layout { display:grid; grid-template-columns:320px 1fr; min-height:calc(100vh - 72px); }
    .sidebar { background:var(--side); border-right:1px solid var(--line); padding:28px 16px; display:flex; flex-direction:column; justify-content:space-between; }
    .profile { display:flex; align-items:center; gap:14px; padding:4px 12px 24px; }
    .profile .avatar { width:58px; height:58px; box-shadow:var(--shadow); }
    .profile h3 { margin:0 0 4px; font-size:18px; }
    .profile p { margin:0; color:var(--muted); font-size:13px; }
    .menu { display:grid; gap:10px; }
    .menu button { width:100%; display:flex; align-items:center; gap:12px; border:0; border-radius:12px; padding:15px 18px; background:transparent; color:#334b63; font-weight:900; text-align:left; cursor:pointer; }
    .menu button.active { background:var(--navy2); color:#fff; box-shadow:0 12px 26px rgba(6,36,67,.18); }
    .menu .num { width:24px; color:inherit; opacity:.75; }
    .hint-card { margin:20px 10px 0; border:1px solid #d9e1ec; border-radius:18px; padding:16px; color:#526174; background:#eef2f7; font-size:13px; line-height:1.7; }
    .content { padding:42px min(56px,4vw); }
    .hero { display:flex; align-items:flex-start; justify-content:space-between; gap:24px; margin-bottom:30px; }
    .eyebrow { color:#8392a7; font-weight:900; letter-spacing:.22em; font-size:12px; margin-bottom:8px; }
    h1 { margin:0; color:var(--navy); font-size:clamp(34px,4vw,56px); line-height:1; letter-spacing:-.05em; font-family:Georgia,"Microsoft YaHei",serif; }
    .subtitle { margin:12px 0 0; color:#526174; font-weight:700; }
    .stats { display:flex; gap:16px; flex-wrap:wrap; }
    .stat { min-width:160px; background:#fff; border-radius:26px; padding:18px 22px; box-shadow:var(--shadow); display:flex; align-items:center; gap:14px; }
    .stat-icon { width:52px; height:52px; border-radius:18px; background:#f1f5f9; display:grid; place-items:center; color:var(--navy); font-weight:900; }
    .stat small { color:#8794a8; font-weight:900; }
    .stat strong { display:block; margin-top:4px; color:var(--navy); font-size:28px; }
    .section { display:none; }
    .section.active { display:block; }
    .grid { display:grid; grid-template-columns:minmax(0,1.1fr) minmax(420px,.9fr); gap:24px; align-items:start; }
    .panel { background:#fff; border:1px solid var(--line); border-radius:28px; box-shadow:var(--shadow); padding:28px; }
    .panel-head { display:flex; align-items:center; justify-content:space-between; gap:16px; margin-bottom:22px; }
    .panel-title { display:flex; align-items:flex-start; gap:12px; }
    .bar { width:6px; height:30px; border-radius:99px; background:var(--navy); margin-top:3px; }
    h2 { margin:0; color:var(--navy); font-size:24px; font-family:Georgia,"Microsoft YaHei",serif; }
    .muted { color:var(--muted); font-size:13px; line-height:1.65; }
    .project-list,.user-list { display:grid; gap:14px; }
    .project { display:grid; grid-template-columns:1fr auto; gap:18px; align-items:center; padding:18px 20px; border:1px solid var(--line); border-radius:22px; background:#fff; box-shadow:0 8px 22px rgba(6,36,67,.04); }
    .project h3 { margin:0 0 6px; color:var(--navy); font-size:18px; }
    .host { color:#8492a6; font-size:13px; }
    .tags { display:flex; flex-wrap:wrap; gap:8px; margin-top:12px; }
    .tag { border-radius:999px; padding:6px 10px; background:#eef2f7; color:#526174; font-size:12px; font-weight:900; }
    .tag.green { background:#dcfce7; color:#166534; } .tag.blue { background:#dbeafe; color:#1e40af; } .tag.red { background:#fee2e2; color:#991b1b; }
    form { display:grid; gap:14px; }
    label { display:grid; gap:8px; color:#7b89a0; font-weight:900; font-size:12px; letter-spacing:.04em; }
    input,select { width:100%; border:0; border-bottom:2px solid #c8d1de; background:transparent; padding:13px 4px; color:#172033; outline:none; }
    input:focus,select:focus { border-color:var(--navy); }
    .row { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
    .whitelist { border:1px solid var(--line); background:#fbfcfe; border-radius:18px; padding:16px; }
    .check-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(140px,1fr)); gap:10px; margin-top:12px; }
    .check { display:flex; align-items:center; gap:9px; background:#fff; border:1px solid var(--line); border-radius:12px; padding:10px; color:#223955; font-weight:800; }
    .check input { width:auto; }
    .notice { min-height:20px; color:var(--muted); font-size:13px; }
    .notice.error { color:var(--red); } .notice.success { color:#15803d; }
    .config { background:var(--navy); color:#dbeafe; border-radius:18px; padding:18px; overflow:auto; font:12px/1.65 Consolas,"Cascadia Mono",monospace; }
    .user { display:flex; align-items:center; justify-content:space-between; gap:12px; padding:14px 16px; border:1px solid var(--line); border-radius:16px; background:#f8fafc; }
    .empty { border:1px dashed #c8d1de; border-radius:20px; padding:24px; color:var(--muted); background:#fbfcfe; }
    .hidden { display:none!important; }
    @media(max-width:1120px){ .layout{grid-template-columns:1fr}.sidebar{display:none}.hero{flex-direction:column}.grid{grid-template-columns:1fr} }
    @media(max-width:680px){ .topbar{padding:0 16px}.content{padding:26px 16px}.row,.project{grid-template-columns:1fr}.top-link{display:none} }
  </style>
</head>
<body>
<header class="topbar">
  <div class="brand"><span class="brand-mark">TN</span><span>Tool Nexus 内部工具网关</span></div>
  <nav class="top-actions">
    <a class="top-link active" href="/">首页</a>
    <button id="refreshButton" class="btn btn-soft">刷新</button>
    <button id="logoutButton" class="btn btn-soft hidden">退出</button>
    <a id="loginLink" href="/login"><button class="btn btn-soft" type="button">登录</button></a>
    <div class="user-chip"><span class="avatar" id="avatarText">TN</span><span id="topUser">未登录</span></div>
  </nav>
</header>
<div class="layout">
  <aside class="sidebar">
    <div>
      <div class="profile"><div class="avatar" id="sideAvatar">TN</div><div><h3 id="sideUser">未登录</h3><p id="sideRole">Tool Nexus 用户</p></div></div>
      <div class="menu">
        <button class="active" data-section="projects"><span class="num">01</span>项目中心</button>
        <button data-section="create"><span class="num">02</span>新增工具</button>
        <button data-section="profile"><span class="num">03</span>个人资料</button>
        <button data-section="users" data-admin-only="1"><span class="num">04</span>用户管理</button>
        <button data-section="config"><span class="num">05</span>接入配置</button>
      </div>
    </div>
    <div class="hint-card"><strong>系统提示</strong><br>普通用户可以登记自己的工具；只有管理员可以创建用户和配置项目白名单。</div>
  </aside>
  <main class="content">
    <section class="hero">
      <div><div class="eyebrow">INTERNAL TOOL PORTAL</div><h1>统一入口与权限管理</h1><p class="subtitle">管理团队工具子域名、登录用户、白名单授权和 FRP 接入。</p></div>
      <div class="stats"><div class="stat"><div class="stat-icon">P</div><div><small>项目数</small><strong id="projectCount">0</strong></div></div><div class="stat"><div class="stat-icon">U</div><div><small>用户数</small><strong id="userCount">0</strong></div></div></div>
    </section>

    <section id="section-projects" class="section active">
      <div class="panel"><div class="panel-head"><div class="panel-title"><span class="bar"></span><div><h2>项目列表</h2><p class="muted">拥有项目、公开项目和白名单授权项目会显示在这里。</p></div></div></div><div id="projectList" class="project-list"></div><div id="projectEmpty" class="empty hidden">暂无可见项目。</div></div>
    </section>

    <section id="section-create" class="section">
      <div class="grid"><div class="panel"><div class="panel-head"><div class="panel-title"><span class="bar"></span><div><h2>新增网页工具</h2><p class="muted">创建后把生成的 customDomains 写入团队成员的 frpc.toml。</p></div></div></div>
        <form id="projectForm"><label>工具名称<input id="projectName" placeholder="image converter" required></label><div class="row"><label>子域名前缀<input id="projectSubdomain" placeholder="image-tool" required pattern="[a-z0-9-]+"></label><label>访问范围<select id="projectVisibility"><option value="true">私有：owner + 白名单</option><option value="false">公开：所有登录用户</option></select></label></div><div id="whitelistBox" class="whitelist"><strong>白名单用户</strong><p class="muted">owner 默认有权限，不需要勾选自己。只有管理员可以设置白名单。</p><div id="whitelistUsers" class="check-grid"></div></div><button class="btn btn-primary" type="submit">创建项目</button><div id="formNotice" class="notice"></div></form>
      </div><div class="panel"><div class="panel-head"><div class="panel-title"><span class="bar"></span><div><h2>接入片段</h2><p class="muted">创建项目后这里会显示客户端配置片段。</p></div></div></div><pre id="configPreview" class="config">customDomains will appear here after creating a project.</pre></div></div>
    </section>

    <section id="section-profile" class="section">
      <div class="panel"><div class="panel-head"><div class="panel-title"><span class="bar"></span><div><h2>个人资料</h2><p class="muted">用户可以修改自己的用户名和密码。</p></div></div></div><form id="profileForm"><div class="row"><label>用户名<input id="profileUsername" required></label><label>新密码<input id="profilePassword" type="password" minlength="6" placeholder="不修改则留空"></label></div><button class="btn btn-primary" type="submit">保存修改</button><div id="profileNotice" class="notice"></div></form></div>
    </section>

    <section id="section-users" class="section">
      <div class="panel"><div class="panel-head"><div class="panel-title"><span class="bar"></span><div><h2>用户管理</h2><p class="muted">只有管理员可以创建用户。管理员也可以创建其他管理员。</p></div></div></div><form id="userForm"><div class="row"><label>用户名<input id="newUsername" placeholder="lisi" required></label><label>初始密码<input id="newPassword" type="password" minlength="6" required></label></div><label class="check"><input id="newIsAdmin" type="checkbox">设为管理员</label><button class="btn btn-primary" type="submit">新增用户</button><div id="userNotice" class="notice"></div></form><div id="userList" class="user-list" style="margin-top:18px"></div></div>
    </section>

    <section id="section-config" class="section">
      <div class="panel"><div class="panel-head"><div class="panel-title"><span class="bar"></span><div><h2>接入配置</h2><p class="muted">发给团队成员的固定信息。每个工具只需要在 frpc.toml 中增加一个 proxies 配置块。</p></div></div></div><pre class="config">serverAddr = "frp.aim888888.xyz"
serverPort = 7000
auth.token = "请向管理员索取"
transport.tls.enable = true

[[proxies]]
name = "your-tool"
type = "http"
localIP = "127.0.0.1"
localPort = 3000
customDomains = ["your-tool.aim888888.xyz"]</pre></div>
    </section>
  </main>
</div>
<script>
const state = { authenticated:false, user:null, projects:[], users:[] };
const $ = (id) => document.getElementById(id);
function escapeHtml(value){ return String(value).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }
function initials(name){ return (name || 'TN').slice(0,2).toUpperCase(); }
function setNotice(el,msg,kind=''){ el.textContent = msg || ''; el.className = 'notice' + (kind ? ' ' + kind : ''); }
async function fetchJson(url,opt={}){ const headers = opt.body ? {'Content-Type':'application/json', ...(opt.headers||{})} : (opt.headers||{}); const r = await fetch(url,{credentials:'include',...opt,headers}); const t = await r.text(); let p=null; try{p=t?JSON.parse(t):null}catch{p={message:t}} if(!r.ok) throw new Error(p?.detail || p?.message || 'Request failed'); return p; }
function switchSection(name){ document.querySelectorAll('.section').forEach(s=>s.classList.remove('active')); document.getElementById('section-'+name)?.classList.add('active'); document.querySelectorAll('.menu button').forEach(b=>b.classList.toggle('active', b.dataset.section===name)); }
document.querySelectorAll('.menu button').forEach(btn => btn.onclick = () => switchSection(btn.dataset.section));
function renderSession(){ const logged = state.authenticated && state.user; $('loginLink').classList.toggle('hidden', logged); $('logoutButton').classList.toggle('hidden', !logged); const name = logged ? state.user.username : '未登录'; $('topUser').textContent=name; $('sideUser').textContent=name; $('avatarText').textContent=initials(name); $('sideAvatar').textContent=initials(name); $('sideRole').textContent = logged && state.user.is_admin ? '管理员' : 'Tool Nexus 用户'; $('profileUsername').value = logged ? state.user.username : ''; document.querySelectorAll('[data-admin-only="1"]').forEach(el=>el.classList.toggle('hidden', !(logged && state.user.is_admin))); $('whitelistBox').classList.toggle('hidden', !(logged && state.user.is_admin) || $('projectVisibility').value !== 'true'); }
function accessLabel(v){ return v === 'owner' ? 'Owner' : v === 'shared' ? 'Whitelist' : v === 'public' ? 'Public' : v === 'admin' ? 'Admin' : v; }
function renderProjects(){ $('projectCount').textContent = state.projects.length; $('projectList').innerHTML=''; $('projectEmpty').classList.toggle('hidden', state.projects.length > 0); for(const p of state.projects){ const host = p.subdomain + '.aim888888.xyz'; const granted = (p.granted_users||[]).map(u=>escapeHtml(u.username)).join(', ') || 'None'; const card = document.createElement('article'); card.className='project'; card.innerHTML = `<div><h3>${escapeHtml(p.name)}</h3><div class="host">${host}</div><div class="tags"><span class="tag blue">${accessLabel(p.access_type)}</span><span class="tag ${p.is_private?'red':'green'}">${p.is_private?'Private':'Public'}</span><span class="tag">Owner: ${escapeHtml(p.owner_username)}</span><span class="tag">Whitelist: ${granted}</span></div></div><a class="btn btn-soft" href="https://${host}" target="_blank">打开</a>`; $('projectList').appendChild(card); } }
function renderUsers(){ $('userCount').textContent = state.users.length || (state.user ? 1 : 0); $('userList').innerHTML=''; $('whitelistUsers').innerHTML=''; for(const u of state.users){ const row=document.createElement('div'); row.className='user'; row.innerHTML = `<strong>${escapeHtml(u.username)}</strong><span class="muted">ID ${u.id}${u.is_admin?' ADMIN':''}</span>`; $('userList').appendChild(row); if(state.user && u.id !== state.user.id){ const lab=document.createElement('label'); lab.className='check'; lab.innerHTML=`<input type="checkbox" value="${u.id}"><span>${escapeHtml(u.username)}</span>`; $('whitelistUsers').appendChild(lab); } } if(!$('whitelistUsers').children.length) $('whitelistUsers').innerHTML='<p class="muted">暂无其他用户。</p>'; }
function renderVisibility(){ $('whitelistBox').classList.toggle('hidden', !(state.user && state.user.is_admin) || $('projectVisibility').value !== 'true'); }
async function loadSession(){ const s=await fetchJson('/api/me'); state.authenticated=s.authenticated; state.user=s.user; renderSession(); }
async function loadUsers(){ if(!(state.authenticated && state.user && state.user.is_admin)){ state.users=[]; renderUsers(); return; } state.users=await fetchJson('/api/users'); renderUsers(); }
async function loadProjects(){ if(!state.authenticated) return; state.projects=await fetchJson('/api/my-projects'); renderProjects(); }
async function reloadAll(){ await loadSession(); if(!state.authenticated){ location.href='/login'; return; } await loadUsers(); await loadProjects(); }
$('refreshButton').onclick = () => reloadAll().catch(e=>setNotice($('formNotice'), e.message, 'error'));
$('logoutButton').onclick = async () => { await fetchJson('/api/logout',{method:'POST'}); location.href='/login'; };
$('projectVisibility').onchange = renderVisibility;
$('projectForm').onsubmit = async (e) => { e.preventDefault(); const sub=$('projectSubdomain').value.trim().toLowerCase(); const isPrivate=$('projectVisibility').value==='true'; const ids=(state.user && state.user.is_admin && isPrivate) ? [...$('whitelistUsers').querySelectorAll('input:checked')].map(i=>Number(i.value)) : []; try{ await fetchJson('/api/projects',{method:'POST',body:JSON.stringify({name:$('projectName').value.trim(), subdomain:sub, is_private:isPrivate, whitelist_user_ids:ids})}); setNotice($('formNotice'),'项目已创建。','success'); $('configPreview').textContent = `serverAddr = "frp.aim888888.xyz"\nserverPort = 7000\nauth.token = "请向管理员索取"\ntransport.tls.enable = true\n\n[[proxies]]\nname = "${sub}"\ntype = "http"\nlocalIP = "127.0.0.1"\nlocalPort = 3000\ncustomDomains = ["${sub}.aim888888.xyz"]`; e.target.reset(); renderVisibility(); await loadProjects(); } catch(err){ setNotice($('formNotice'),err.message,'error'); } };
$('userForm').onsubmit = async (e) => { e.preventDefault(); try{ await fetchJson('/api/users',{method:'POST',body:JSON.stringify({username:$('newUsername').value.trim(), password:$('newPassword').value, is_admin:$('newIsAdmin').checked})}); setNotice($('userNotice'),'用户已创建。','success'); e.target.reset(); await loadUsers(); } catch(err){ setNotice($('userNotice'),err.message,'error'); } };
$('profileForm').onsubmit = async (e) => { e.preventDefault(); const body={username:$('profileUsername').value.trim()}; if($('profilePassword').value) body.password=$('profilePassword').value; try{ const u=await fetchJson('/api/users/me',{method:'PATCH',body:JSON.stringify(body)}); state.user=u; $('profilePassword').value=''; renderSession(); setNotice($('profileNotice'),'资料已更新。','success'); await loadProjects(); } catch(err){ setNotice($('profileNotice'),err.message,'error'); } };
renderVisibility(); reloadAll().catch(e=>setNotice($('formNotice'), e.message, 'error'));
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
  <title>Tool Nexus Login</title>
  <style>
    :root { --navy:#062443; --bg:#f7f9fd; --muted:#637083; --line:#e6ebf2; --shadow:0 24px 70px rgba(6,36,67,.1); }
    * { box-sizing:border-box; }
    body { margin:0; min-height:100vh; font-family:"Microsoft YaHei","PingFang SC","Noto Sans SC","Segoe UI",sans-serif; color:var(--navy); background:linear-gradient(90deg,#f8fafc 0%,#f8fafc 58%,#eef2f8 58%,#eef2f8 100%); }
    a { color:inherit; text-decoration:none; }
    .top { height:72px; display:flex; align-items:center; justify-content:space-between; padding:0 42px; background:#fff; border-bottom:1px solid var(--line); }
    .brand { font-size:20px; font-weight:900; }
    .links { display:flex; gap:34px; font-weight:900; }
    .wrap { min-height:calc(100vh - 72px); display:grid; grid-template-columns:1.15fr .85fr; align-items:center; gap:40px; width:min(1360px,calc(100% - 64px)); margin:0 auto; }
    .hero small { display:inline-flex; letter-spacing:.28em; color:#91a4bd; font-weight:900; background:#edf2f8; border-radius:999px; padding:8px 18px; }
    .hero h1 { font-family:Georgia,"Microsoft YaHei",serif; font-size:clamp(58px,7vw,92px); line-height:.95; margin:30px 0 18px; letter-spacing:-.06em; }
    .hero p { font-size:20px; line-height:1.7; color:#516071; max-width:720px; }
    .stats { display:flex; gap:24px; margin-top:50px; }
    .stat { min-width:220px; background:#fff; border-radius:24px; padding:28px 32px; box-shadow:0 18px 45px rgba(6,36,67,.08); }
    .stat strong { display:block; font-size:38px; margin-top:10px; }
    .stat.dark { background:var(--navy); color:#fff; }
    .card { background:#fff; border-radius:34px; padding:44px 48px; box-shadow:var(--shadow); }
    h2 { font-size:28px; margin:0 0 8px; font-family:Georgia,"Microsoft YaHei",serif; }
    .muted { color:var(--muted); }
    .roles { display:grid; grid-template-columns:repeat(2,1fr); gap:14px; margin:24px 0 34px; }
    .role { border:2px solid var(--line); border-radius:18px; padding:22px 10px; text-align:center; font-weight:900; cursor:pointer; background:#fff; }
    .role.active { border-color:var(--navy); background:#f4f7fb; }
    label { display:grid; gap:8px; margin:18px 0; color:#9aabc0; font-size:12px; font-weight:900; letter-spacing:.08em; }
    input { border:0; border-bottom:2px solid #c8d1de; padding:14px 2px; font-size:17px; outline:none; }
    input:focus { border-color:var(--navy); }
    button.login { width:100%; border:0; border-radius:18px; background:var(--navy); color:#fff; padding:17px; font-size:16px; font-weight:900; margin-top:22px; cursor:pointer; box-shadow:0 16px 26px rgba(6,36,67,.18); }
    .notice { min-height:22px; margin-top:14px; color:var(--muted); }
    .notice.error { color:#b91c1c; } .notice.success { color:#15803d; }
    .back { display:inline-block; margin-top:18px; font-weight:900; }
    @media(max-width:980px){ .wrap{grid-template-columns:1fr;padding:30px 0}.stats{flex-direction:column}.top{padding:0 18px}.links{display:none} }
  </style>
</head>
<body>
<header class="top"><div class="brand">TN Tool Nexus 内部工具网关</div><nav class="links"><a href="/">首页</a><a>指南</a><a>公告</a><a>关于</a></nav></header>
<main class="wrap">
  <section class="hero"><small>INTERNAL TOOL GATEWAY</small><h1>统一接入<br>权限可控</h1><p>通过 Portal 管理团队网页工具、用户白名单和 FRP 子域名接入。</p><div class="stats"><div class="stat">FRP<strong>7000</strong></div><div class="stat dark">SSO<strong>ON</strong></div></div></section>
  <section class="card"><h2>身份登录</h2><p class="muted">登录后可访问已授权的工具。</p><div class="roles"><button type="button" class="role active" data-role="user">用户</button><button type="button" class="role" data-role="admin">管理员</button></div><form id="loginForm"><label>ACCOUNT / 账号<input id="username" value="zhangsan" required></label><label>PASSWORD / 密码<input id="password" type="password" value="zhangsan123" required></label><button class="login" type="submit">立即登录</button><div id="notice" class="notice"></div></form><a class="back" href="/">返回门户首页</a></section>
</main>
<script>
let selectedRole = 'user';
const params = new URLSearchParams(location.search);
const nextUrl = params.get('next') || '/';
const notice = document.getElementById('notice');
function setNotice(msg, kind=''){ notice.textContent = msg || ''; notice.className = 'notice' + (kind ? ' ' + kind : ''); }
async function fetchJson(url,opt={}){ const r=await fetch(url,{credentials:'include',headers:{'Content-Type':'application/json'},...opt}); const t=await r.text(); let p=null; try{p=t?JSON.parse(t):null}catch{p={message:t}} if(!r.ok) throw new Error(p?.detail || p?.message || 'Request failed'); return p; }
document.querySelectorAll('.role').forEach(btn => btn.onclick = () => { selectedRole = btn.dataset.role; document.querySelectorAll('.role').forEach(x=>x.classList.toggle('active', x===btn)); });
document.getElementById('loginForm').onsubmit = async (e) => { e.preventDefault(); try{ setNotice('登录中...'); const data = await fetchJson('/api/login',{method:'POST',body:JSON.stringify({username:document.getElementById('username').value.trim(), password:document.getElementById('password').value})}); if(selectedRole === 'admin' && !data.user.is_admin){ await fetchJson('/api/logout',{method:'POST'}); setNotice('该账号不是管理员。','error'); return; } setNotice('登录成功。','success'); location.href = nextUrl; } catch(err){ setNotice(err.message,'error'); } };
</script>
</body>
</html>
"""
