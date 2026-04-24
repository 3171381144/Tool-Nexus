from app.core.config import settings


ROOT_DOMAIN = settings.root_domain or "aim888888.xyz"
WEB_PROTOCOL = "https" if settings.root_domain else "http"


def _fill(template: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        template = template.replace(f"__{key}__", value)
    return template


PORTAL_PAGE_HTML = _fill(r'''
<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tool Nexus Portal</title>
<style>
:root{--navy:#082544;--paper:#fffdf8;--bg:#f4f6f8;--line:#d8e1e8;--muted:#6d7d8b;--green:#15803d;--red:#b91c1c;--gold:#f6e4b8;--shadow:0 16px 40px rgba(8,37,68,.12)}*{box-sizing:border-box}body{margin:0;font-family:"Microsoft YaHei","PingFang SC",sans-serif;background:linear-gradient(135deg,#f7f4ec,#eef4f7);color:#17324d}button,input,select,textarea{font:inherit}a{text-decoration:none;color:inherit}button{cursor:pointer}header{position:sticky;top:0;z-index:10;background:rgba(8,37,68,.96);color:#fff;padding:16px 22px;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}.brand{font-weight:900;font-size:22px}.top-actions{display:flex;gap:10px;align-items:center;flex-wrap:wrap}.btn{border:0;border-radius:14px;padding:10px 14px;font-weight:900}.btn-primary{background:var(--navy);color:#fff}.btn-soft{background:#edf3f7;color:var(--navy)}.btn-gold{background:var(--gold);color:#754200}.btn-danger{background:#fee2e2;color:#991b1b}.chip{padding:10px 14px;border-radius:999px;background:rgba(255,255,255,.12);font-weight:800}.wrap{padding:28px min(32px,4vw) 40px}.hero{display:flex;justify-content:space-between;gap:18px;flex-wrap:wrap;align-items:flex-start;margin-bottom:24px}.hero h1{margin:0;font-size:clamp(34px,4vw,56px);line-height:1;letter-spacing:-.05em;font-family:Georgia,"Microsoft YaHei",serif;color:var(--navy)}.hero p{margin:12px 0 0;max-width:760px;color:#536678;line-height:1.8}.stats{display:flex;gap:12px;flex-wrap:wrap}.stat{min-width:150px;background:var(--paper);border-radius:22px;padding:18px;box-shadow:var(--shadow)}.stat small{display:block;color:#81909e;font-weight:900}.stat strong{display:block;margin-top:8px;font-size:28px;color:var(--navy)}.menu{display:flex;gap:10px;flex-wrap:wrap;margin:0 0 22px}.menu button{border:0;border-radius:999px;padding:11px 16px;font-weight:900;background:#e8eef3;color:#26455f}.menu button.active{background:#153b63;color:#fff}.section{display:none}.section.active{display:block}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}.panel{background:var(--paper);border:1px solid rgba(8,37,68,.08);border-radius:26px;padding:22px;box-shadow:var(--shadow)}.panel h2{margin:0 0 8px;font-size:24px;font-family:Georgia,"Microsoft YaHei",serif;color:var(--navy)}.muted{color:var(--muted);font-size:13px;line-height:1.7}.list{display:grid;gap:14px}.card{border:1px solid var(--line);border-radius:20px;background:#fff;padding:16px;display:grid;gap:12px}.card-head{display:flex;justify-content:space-between;gap:14px;align-items:flex-start;flex-wrap:wrap}.card h3{margin:0 0 6px;color:var(--navy);font-size:19px}.sub{color:#7d8c9a;font-size:13px}.tags{display:flex;gap:8px;flex-wrap:wrap}.tag{padding:5px 10px;border-radius:999px;background:#edf3f7;color:#4f677e;font-size:12px;font-weight:900}.tag.green{background:#dcfce7;color:#166534}.tag.red{background:#fee2e2;color:#991b1b}.tag.blue{background:#dbeafe;color:#1d4ed8}.tag.gold{background:#fef3c7;color:#92400e}.desc{padding:12px 14px;border-radius:14px;background:#f8fbfd;border:1px solid var(--line);white-space:pre-wrap;line-height:1.7}.actions{display:flex;gap:10px;flex-wrap:wrap}details{border:1px solid var(--line);border-radius:16px;background:#fbfdff}summary{cursor:pointer;padding:12px 14px;font-weight:900;color:var(--navy)}form{display:grid;gap:12px;padding:0 14px 14px}label{display:grid;gap:7px;color:#718497;font-size:12px;font-weight:900;letter-spacing:.05em}input,select,textarea{width:100%;border:1px solid #cfd8df;border-radius:13px;padding:11px 12px;background:#fff;outline:none}textarea{min-height:110px;resize:vertical}input:focus,select:focus,textarea:focus{border-color:#2e5b87;box-shadow:0 0 0 3px rgba(46,91,135,.12)}.row{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.checks{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}.check{display:flex;align-items:center;gap:8px;border:1px solid var(--line);border-radius:12px;padding:10px;background:#fff;font-weight:800;color:#26455f}.check input{width:auto}.notice{min-height:18px;color:var(--muted);font-size:13px}.notice.success{color:var(--green)}.notice.error{color:var(--red)}.empty{padding:24px;border:1px dashed #cad4dd;border-radius:18px;background:#fbfdff;color:#7b8b99}.tree{padding:12px;border-radius:14px;background:#0d223c;color:#d7e7f5;white-space:pre-wrap;overflow:auto;max-height:260px;font:12px/1.6 Consolas,"Cascadia Mono",monospace}.readme{padding:16px;border:1px solid var(--line);border-radius:16px;background:#fff;line-height:1.8}.readme h1,.readme h2,.readme h3,.readme h4,.readme h5,.readme h6{color:var(--navy)}.readme pre{padding:12px;border-radius:12px;background:#0d223c;color:#d7e7f5;overflow:auto}.readme code{background:#edf3f7;padding:.1em .35em;border-radius:8px}.readme pre code{background:transparent;padding:0}.modal-mask{position:fixed;inset:0;background:rgba(8,37,68,.56);display:grid;place-items:center;padding:18px}.modal{width:min(960px,100%);max-height:calc(100vh - 36px);overflow:auto;background:var(--paper);border-radius:28px;padding:22px;box-shadow:0 30px 80px rgba(8,37,68,.3)}.hidden{display:none!important}@media(max-width:900px){.grid,.row{grid-template-columns:1fr}}
</style>
</head>
<body>
<header>
  <div class="brand">Tool Nexus 资源门户</div>
  <div class="top-actions">
    <span class="chip" id="topUser">未登录</span>
    <button id="refreshButton" class="btn btn-soft" type="button">刷新</button>
    <button id="logoutButton" class="btn btn-soft hidden" type="button">退出</button>
    <a id="loginLink" href="/login"><button class="btn btn-gold" type="button">登录 / 注册</button></a>
  </div>
</header>
<main class="wrap">
  <section class="hero">
    <div>
      <div class="muted" style="font-weight:900;letter-spacing:.18em">INTERNAL RESOURCE HUB</div>
      <h1>统一入口<br>统一授权</h1>
      <p>网页工具继续走子域名和 FRP；代码仓库新增为独立资源类型，支持白名单访问、zip 归档上传、README 在线阅读和归档下载。</p>
    </div>
    <div class="stats">
      <div class="stat"><small>网页工具</small><strong id="projectCount">0</strong></div>
      <div class="stat"><small>代码仓库</small><strong id="repositoryCount">0</strong></div>
      <div class="stat"><small>用户数</small><strong id="userCount">0</strong></div>
    </div>
  </section>

  <div class="menu">
    <button class="active" data-section="dashboard">资源总览</button>
    <button data-section="create-project">新增网页工具</button>
    <button data-section="create-repository">新增代码仓库</button>
    <button data-section="profile">个人资料</button>
    <button data-section="users" data-admin-only="1">用户管理</button>
  </div>

  <section id="section-dashboard" class="section active">
    <div class="grid">
      <div class="panel">
        <h2>网页工具</h2>
        <p class="muted">可以直接打开工具；如果你是 owner 或管理员，还可以在卡片内调整说明、可见性和白名单。</p>
        <div id="projectList" class="list"></div>
        <div id="projectEmpty" class="empty hidden">当前没有可见的网页工具。</div>
      </div>
      <div class="panel">
        <h2>代码仓库</h2>
        <p class="muted">支持在线查看 README、下载归档；owner 或管理员还能替换 zip 版本和调整访问范围。</p>
        <div id="repositoryList" class="list"></div>
        <div id="repositoryEmpty" class="empty hidden">当前没有可见的代码仓库。</div>
      </div>
    </div>
  </section>

  <section id="section-create-project" class="section">
    <div class="grid">
      <div class="panel">
        <h2>新增网页工具</h2>
        <p class="muted">创建后会生成一段 `frpc.toml` 配置片段。</p>
        <form id="projectForm">
          <label>工具名称<input id="projectName" required></label>
          <div class="row">
            <label>子域名前缀<input id="projectSubdomain" pattern="[a-z0-9-]+" required></label>
            <label>访问范围<select id="projectVisibility"><option value="true">私有：owner + 白名单</option><option value="false">公开：所有已登录用户</option></select></label>
          </div>
          <div id="projectWhitelistBox">
            <label>白名单用户</label>
            <div id="projectWhitelistUsers" class="checks"></div>
          </div>
          <button class="btn btn-primary" type="submit">创建网页工具</button>
          <div id="projectFormNotice" class="notice"></div>
        </form>
      </div>
      <div class="panel">
        <h2>FRP 配置片段</h2>
        <p class="muted">创建完成后，按这个模板写入成员电脑上的 `frpc.toml`。</p>
        <pre id="configPreview" class="tree">创建网页工具后会在这里生成 customDomains 配置。</pre>
      </div>
    </div>
  </section>

  <section id="section-create-repository" class="section">
    <div class="grid">
      <div class="panel">
        <h2>新增代码仓库</h2>
        <p class="muted">当前版本采用 zip 上传，系统会保存归档并自动读取 README。</p>
        <form id="repositoryForm">
          <label>仓库名称<input id="repositoryName" required></label>
          <label>仓库说明<textarea id="repositoryDescription"></textarea></label>
          <div class="row">
            <label>访问范围<select id="repositoryVisibility"><option value="true">私有：owner + 白名单</option><option value="false">公开：所有已登录用户</option></select></label>
            <label>zip 归档<input id="repositoryArchive" type="file" accept=".zip" required></label>
          </div>
          <div id="repositoryWhitelistBox">
            <label>白名单用户</label>
            <div id="repositoryWhitelistUsers" class="checks"></div>
          </div>
          <button class="btn btn-primary" type="submit">上传代码仓库</button>
          <div id="repositoryFormNotice" class="notice"></div>
        </form>
      </div>
      <div class="panel">
        <h2>使用约定</h2>
        <div class="desc">1. 先把代码仓库打包成 zip。\n2. 上传后其他成员可按权限在线查看 README 或下载。\n3. 如果压缩包中有 README.md / README.txt / README.rst，系统会自动识别。</div>
      </div>
    </div>
  </section>

  <section id="section-profile" class="section">
    <div class="panel">
      <h2>个人资料</h2>
      <form id="profileForm">
        <div class="row">
          <label>用户名<input id="profileUsername" required></label>
          <label>昵称<input id="profileNickname" required></label>
        </div>
        <label>新密码<input id="profilePassword" type="password" minlength="6" placeholder="留空表示不修改"></label>
        <button class="btn btn-primary" type="submit">保存资料</button>
        <div id="profileNotice" class="notice"></div>
      </form>
    </div>
  </section>

  <section id="section-users" class="section">
    <div class="panel">
      <h2>用户管理</h2>
      <form id="userForm">
        <div class="row">
          <label>用户名<input id="newUsername" required></label>
          <label>昵称<input id="newNickname"></label>
        </div>
        <div class="row">
          <label>初始密码<input id="newPassword" type="password" minlength="6" required></label>
          <label>角色<div class="check"><input id="newIsAdmin" type="checkbox">设为管理员</div></label>
        </div>
        <button class="btn btn-primary" type="submit">新增用户</button>
        <div id="userNotice" class="notice"></div>
      </form>
      <div id="userList" class="list" style="margin-top:16px"></div>
    </div>
  </section>
</main>

<div id="readmeModal" class="modal-mask hidden">
  <div class="modal">
    <div class="card-head">
      <div><h2 id="readmeTitle" style="margin:0">仓库预览</h2><p id="readmeMeta" class="muted" style="margin:10px 0 0"></p></div>
      <div class="actions"><a id="readmeDownload" class="btn btn-gold" href="#">下载归档</a><button id="closeReadmeModal" class="btn btn-soft" type="button">关闭</button></div>
    </div>
    <div class="grid">
      <div class="panel"><h2 style="font-size:20px">文件树</h2><div id="readmeTree" class="tree"></div></div>
      <div class="panel"><h2 style="font-size:20px">README 阅读器</h2><div id="readmeContent" class="readme"></div></div>
    </div>
  </div>
</div>

<script>
const ROOT_DOMAIN='__ROOT_DOMAIN__';
const WEB_PROTOCOL='__WEB_PROTOCOL__';
const I18N={created:'网页工具已创建。',repoCreated:'代码仓库已上传。',saved:'保存成功。',uploaded:'新归档已上传。',profileSaved:'个人资料已更新。',userCreated:'用户已创建。',projectDeleted:'网页工具已删除。',repoDeleted:'代码仓库已删除。',userDeleted:'用户已删除。',checking:'检测中',online:'已启动',offline:'未启动',noUsers:'暂无其他用户。'};
const state={user:null,users:[],projects:[],repositories:[],health:{}};
const $=id=>document.getElementById(id);
const esc=v=>String(v??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
const nameOf=u=>u?.nickname||u?.username||'Unknown';
const setNotice=(id,msg='',kind='')=>{const el=$(id);if(!el)return;el.textContent=msg;el.className='notice'+(kind?' '+kind:'')};
async function fetchJson(url,opt={}){const headers={Accept:'application/json',...(opt.headers||{})};if(opt.body && !(opt.body instanceof FormData) && !headers['Content-Type'])headers['Content-Type']='application/json';const res=await fetch(url,{credentials:'include',...opt,headers});const text=await res.text();let payload=null;try{payload=text?JSON.parse(text):null}catch{payload={message:text}}if(!res.ok)throw new Error(payload?.detail||payload?.message||'请求失败');return payload}
function accessLabel(t){return({owner:'Owner',shared:'白名单',public:'公开',admin:'管理员'}[t]||t)}
function healthTag(p){const h=state.health[p.id];if(!h)return `<span class="tag">${I18N.checking}</span>`;return h.online?`<span class="tag green">${I18N.online}</span>`:`<span class="tag red">${I18N.offline}</span>`}
function host(p){return `${p.subdomain}.${ROOT_DOMAIN}`}
function projectUrl(p){return `${WEB_PROTOCOL}://${host(p)}`}
function userChecks(selected,ownerId){const ids=new Set(selected||[]);const items=state.users.filter(u=>u.id!==ownerId).map(u=>`<label class="check"><input type="checkbox" value="${u.id}" ${ids.has(u.id)?'checked':''}><span>${esc(nameOf(u))}</span></label>`);return items.join('')||`<div class="muted">${I18N.noUsers}</div>`}
function renderSession(){const u=state.user;const n=u?nameOf(u):'未登录';$('topUser').textContent=n;$('logoutButton').classList.toggle('hidden',!u);$('loginLink').classList.toggle('hidden',!!u);document.querySelectorAll('[data-admin-only="1"]').forEach(b=>b.classList.toggle('hidden',!(u&&u.is_admin)));if(u){$('profileUsername').value=u.username||'';$('profileNickname').value=u.nickname||''}}
function renderUsers(){const list=$('userList');list.innerHTML='';$('userCount').textContent=String(state.users.length||(state.user?1:0));$('projectWhitelistUsers').innerHTML='';$('repositoryWhitelistUsers').innerHTML='';for(const u of state.users){const row=document.createElement('div');row.className='card';row.innerHTML=`<div class="card-head"><div><strong>${esc(nameOf(u))}</strong><div class="sub">${esc(u.username)} · ID ${u.id}${u.is_admin?' · ADMIN':''}</div></div>${state.user&&state.user.is_admin&&state.user.id!==u.id?`<button class="btn btn-danger" type="button" data-delete-user="${u.id}">删除用户</button>`:''}</div>`;list.appendChild(row);if(state.user&&u.id!==state.user.id){const a=document.createElement('label');a.className='check';a.innerHTML=`<input type="checkbox" value="${u.id}"><span>${esc(nameOf(u))}</span>`;$('projectWhitelistUsers').appendChild(a);const b=document.createElement('label');b.className='check';b.innerHTML=`<input type="checkbox" value="${u.id}"><span>${esc(nameOf(u))}</span>`;$('repositoryWhitelistUsers').appendChild(b)}}if(!$('projectWhitelistUsers').children.length)$('projectWhitelistUsers').innerHTML=`<div class="muted">${I18N.noUsers}</div>`;if(!$('repositoryWhitelistUsers').children.length)$('repositoryWhitelistUsers').innerHTML=`<div class="muted">${I18N.noUsers}</div>`;toggleCreateBoxes()}
function renderProjects(){const list=$('projectList');list.innerHTML='';$('projectCount').textContent=String(state.projects.length);$('projectEmpty').classList.toggle('hidden',state.projects.length>0);for(const p of state.projects){const canManage=state.user&&(state.user.is_admin||p.owner_id===state.user.id);const users=(p.granted_users||[]).map(u=>u.id);const card=document.createElement('div');card.className='card';card.dataset.projectId=p.id;card.innerHTML=`<div class="card-head"><div><h3>${esc(p.name)}</h3><div class="sub">${esc(host(p))}</div><div class="tags">${healthTag(p)}<span class="tag blue">${accessLabel(p.access_type)}</span><span class="tag ${p.is_private?'red':'green'}">${p.is_private?'私有':'公开'}</span><span class="tag gold">Owner: ${esc(p.owner_nickname||p.owner_username)}</span></div></div><div class="actions"><a class="btn btn-soft" href="${projectUrl(p)}" target="_blank">打开工具</a></div></div><div class="desc"><strong>项目介绍</strong><br>${esc(p.description||'暂无项目介绍。')}</div><div class="desc"><strong>使用说明</strong><br>${esc(p.usage_guide||'暂无使用说明。')}</div>${canManage?`<details><summary>管理网页工具</summary><form data-project-form="${p.id}"><label>项目介绍<textarea data-description>${esc(p.description||'')}</textarea></label><label>使用说明<textarea data-usage>${esc(p.usage_guide||'')}</textarea></label><label>访问范围<select data-private><option value="true" ${p.is_private?'selected':''}>私有：owner + 白名单</option><option value="false" ${!p.is_private?'selected':''}>公开：所有已登录用户</option></select></label><div class="checks" data-users>${userChecks(users,p.owner_id)}</div><div class="actions"><button class="btn btn-danger" type="button" data-delete-project="${p.id}">删除</button><button class="btn btn-primary" type="submit">保存</button></div><div class="notice" data-notice></div></form></details>`:''}`;list.appendChild(card)}}
function renderRepositories(){const list=$('repositoryList');list.innerHTML='';$('repositoryCount').textContent=String(state.repositories.length);$('repositoryEmpty').classList.toggle('hidden',state.repositories.length>0);for(const r of state.repositories){const canManage=state.user&&(state.user.is_admin||r.owner_id===state.user.id);const users=(r.granted_users||[]).map(u=>u.id);const card=document.createElement('div');card.className='card';card.dataset.repositoryId=r.id;card.innerHTML=`<div class="card-head"><div><h3>${esc(r.name)}</h3><div class="sub">${esc(r.archive_name||'未命名归档')}</div><div class="tags"><span class="tag blue">${accessLabel(r.access_type)}</span><span class="tag ${r.is_private?'red':'green'}">${r.is_private?'私有':'公开'}</span><span class="tag gold">Owner: ${esc(r.owner_nickname||r.owner_username)}</span>${r.readme_path?`<span class="tag green">README: ${esc(r.readme_path)}</span>`:'<span class="tag">未发现 README</span>'}</div></div><div class="actions"><button class="btn btn-soft" type="button" data-view-repository="${r.id}">在线查看</button><a class="btn btn-gold" href="/api/repositories/${r.id}/download">下载归档</a></div></div><div class="desc">${esc(r.description||'暂无仓库说明。')}</div>${canManage?`<details><summary>管理代码仓库</summary><form data-repository-form="${r.id}"><label>仓库名称<input data-name value="${esc(r.name)}"></label><label>仓库说明<textarea data-description>${esc(r.description||'')}</textarea></label><label>访问范围<select data-private><option value="true" ${r.is_private?'selected':''}>私有：owner + 白名单</option><option value="false" ${!r.is_private?'selected':''}>公开：所有已登录用户</option></select></label><div class="checks" data-users>${userChecks(users,r.owner_id)}</div><label>上传新 zip 归档<input data-archive type="file" accept=".zip"></label><div class="actions"><button class="btn btn-danger" type="button" data-delete-repository="${r.id}">删除</button><button class="btn btn-gold" type="button" data-upload-repository="${r.id}">上传新版本</button><button class="btn btn-primary" type="submit">保存</button></div><div class="notice" data-notice></div></form></details>`:''}`;list.appendChild(card)}}
function toggleCreateBoxes(){$('projectWhitelistBox').classList.toggle('hidden',$('projectVisibility').value!=='true');$('repositoryWhitelistBox').classList.toggle('hidden',$('repositoryVisibility').value!=='true')}
async function openReadme(id){const data=await fetchJson(`/api/repositories/${id}/readme`);$('readmeTitle').textContent=data.name;$('readmeMeta').textContent=`${data.archive_name||'未命名归档'}${data.readme_path?` · README: ${data.readme_path}`:''}`;$('readmeDownload').href=`/api/repositories/${id}/download`;$('readmeTree').textContent=(data.tree||[]).map(x=>`${x.entry_type==='dir'?'[DIR] ':'      '}${x.path}${x.entry_type==='file'?` (${x.size} B)`:''}`).join('\n')||'暂无文件列表';$('readmeContent').innerHTML=data.readme_html||'<p>没有可展示的 README。</p>';$('readmeModal').classList.remove('hidden')}
async function loadAll(){const me=await fetchJson('/api/me');if(!me.authenticated){location.href='/login';return}state.user=me.user;renderSession();state.users=await fetchJson('/api/users');renderUsers();state.projects=await fetchJson('/api/my-projects');renderProjects();state.repositories=await fetchJson('/api/my-repositories');renderRepositories();state.health={};for(const h of await fetchJson('/api/projects/health'))state.health[h.project_id]=h;renderProjects()}
document.querySelectorAll('.menu button').forEach(b=>b.onclick=()=>{document.querySelectorAll('.menu button').forEach(x=>x.classList.toggle('active',x===b));document.querySelectorAll('.section').forEach(s=>s.classList.toggle('active',s.id===`section-${b.dataset.section}`))});$('projectVisibility').onchange=toggleCreateBoxes;$('repositoryVisibility').onchange=toggleCreateBoxes;$('refreshButton').onclick=()=>loadAll().catch(e=>setNotice('projectFormNotice',e.message,'error'));$('logoutButton').onclick=async()=>{await fetchJson('/api/logout',{method:'POST'});location.href='/login'};$('closeReadmeModal').onclick=()=>$('readmeModal').classList.add('hidden');$('readmeModal').onclick=e=>{if(e.target.id==='readmeModal')$('readmeModal').classList.add('hidden')};
$('projectForm').onsubmit=async e=>{e.preventDefault();const isPrivate=$('projectVisibility').value==='true';const whitelist=isPrivate?[...$('projectWhitelistUsers').querySelectorAll('input:checked')].map(i=>Number(i.value)):[];try{const p=await fetchJson('/api/projects',{method:'POST',body:JSON.stringify({name:$('projectName').value.trim(),subdomain:$('projectSubdomain').value.trim().toLowerCase(),is_private:isPrivate,whitelist_user_ids:whitelist})});setNotice('projectFormNotice',I18N.created,'success');$('configPreview').textContent=`serverAddr = "frp.__ROOT_DOMAIN__"\nserverPort = 7000\nauth.token = "请向管理员索取"\ntransport.tls.enable = true\n\n[[proxies]]\nname = "${p.subdomain}"\ntype = "http"\nlocalIP = "127.0.0.1"\nlocalPort = 3000\ncustomDomains = ["${p.subdomain}.__ROOT_DOMAIN__"]`;e.target.reset();toggleCreateBoxes();await loadAll()}catch(err){setNotice('projectFormNotice',err.message,'error')}};
$('repositoryForm').onsubmit=async e=>{e.preventDefault();const file=$('repositoryArchive').files[0];if(!file){setNotice('repositoryFormNotice','请先选择 zip 文件。','error');return}const isPrivate=$('repositoryVisibility').value==='true';const whitelist=isPrivate?[...$('repositoryWhitelistUsers').querySelectorAll('input:checked')].map(i=>Number(i.value)):[];const fd=new FormData();fd.append('name',$('repositoryName').value.trim());fd.append('description',$('repositoryDescription').value.trim());fd.append('is_private',String(isPrivate));fd.append('whitelist_user_ids',JSON.stringify(whitelist));fd.append('archive',file);try{await fetchJson('/api/repositories',{method:'POST',body:fd});setNotice('repositoryFormNotice',I18N.repoCreated,'success');e.target.reset();toggleCreateBoxes();await loadAll()}catch(err){setNotice('repositoryFormNotice',err.message,'error')}};
$('projectList').onclick=async e=>{const del=e.target.closest('[data-delete-project]');if(del&&confirm('确认删除这个网页工具吗？')){const notice=del.closest('form')?.querySelector('[data-notice]');try{await fetchJson(`/api/projects/${del.dataset.deleteProject}`,{method:'DELETE'});if(notice){notice.textContent=I18N.projectDeleted;notice.className='notice success'}await loadAll()}catch(err){if(notice){notice.textContent=err.message;notice.className='notice error'}}}};
$('projectList').onsubmit=async e=>{e.preventDefault();const form=e.target.closest('[data-project-form]');if(!form)return;const id=form.dataset.projectForm;const notice=form.querySelector('[data-notice]');const whitelist=[...form.querySelectorAll('[data-users] input:checked')].map(i=>Number(i.value));try{await fetchJson(`/api/projects/${id}/docs`,{method:'PATCH',body:JSON.stringify({description:form.querySelector('[data-description]').value,usage_guide:form.querySelector('[data-usage]').value})});await fetchJson(`/api/projects/${id}/access`,{method:'PUT',body:JSON.stringify({is_private:form.querySelector('[data-private]').value==='true',whitelist_user_ids:whitelist})});notice.textContent=I18N.saved;notice.className='notice success';await loadAll()}catch(err){notice.textContent=err.message;notice.className='notice error'}};
$('repositoryList').onclick=async e=>{const view=e.target.closest('[data-view-repository]');if(view){openReadme(Number(view.dataset.viewRepository)).catch(err=>alert(err.message));return}const del=e.target.closest('[data-delete-repository]');if(del&&confirm('确认删除这个代码仓库吗？')){const notice=del.closest('form')?.querySelector('[data-notice]');try{await fetchJson(`/api/repositories/${del.dataset.deleteRepository}`,{method:'DELETE'});if(notice){notice.textContent=I18N.repoDeleted;notice.className='notice success'}await loadAll()}catch(err){if(notice){notice.textContent=err.message;notice.className='notice error'}}return}const up=e.target.closest('[data-upload-repository]');if(up){const form=up.closest('form');const input=form?.querySelector('[data-archive]');const notice=form?.querySelector('[data-notice]');const file=input?.files?.[0];if(!file){if(notice){notice.textContent='请先选择 zip 文件。';notice.className='notice error'}return}const fd=new FormData();fd.append('archive',file);try{await fetchJson(`/api/repositories/${up.dataset.uploadRepository}/upload`,{method:'POST',body:fd});if(notice){notice.textContent=I18N.uploaded;notice.className='notice success'}await loadAll()}catch(err){if(notice){notice.textContent=err.message;notice.className='notice error'}}}};
$('repositoryList').onsubmit=async e=>{e.preventDefault();const form=e.target.closest('[data-repository-form]');if(!form)return;const id=form.dataset.repositoryForm;const notice=form.querySelector('[data-notice]');const whitelist=[...form.querySelectorAll('[data-users] input:checked')].map(i=>Number(i.value));try{await fetchJson(`/api/repositories/${id}`,{method:'PATCH',body:JSON.stringify({name:form.querySelector('[data-name]').value.trim(),description:form.querySelector('[data-description]').value})});await fetchJson(`/api/repositories/${id}/access`,{method:'PUT',body:JSON.stringify({is_private:form.querySelector('[data-private]').value==='true',whitelist_user_ids:whitelist})});notice.textContent=I18N.saved;notice.className='notice success';await loadAll()}catch(err){notice.textContent=err.message;notice.className='notice error'}};
$('profileForm').onsubmit=async e=>{e.preventDefault();const body={username:$('profileUsername').value.trim(),nickname:$('profileNickname').value.trim()};if($('profilePassword').value)body.password=$('profilePassword').value;try{const u=await fetchJson('/api/users/me',{method:'PATCH',body:JSON.stringify(body)});state.user=u;renderSession();$('profilePassword').value='';setNotice('profileNotice',I18N.profileSaved,'success');await loadAll()}catch(err){setNotice('profileNotice',err.message,'error')}};
$('userForm').onsubmit=async e=>{e.preventDefault();try{await fetchJson('/api/users',{method:'POST',body:JSON.stringify({username:$('newUsername').value.trim(),nickname:$('newNickname').value.trim(),password:$('newPassword').value,is_admin:$('newIsAdmin').checked})});setNotice('userNotice',I18N.userCreated,'success');e.target.reset();await loadAll()}catch(err){setNotice('userNotice',err.message,'error')}};
$('userList').onclick=async e=>{const del=e.target.closest('[data-delete-user]');if(!del||!confirm('确认删除这个用户吗？'))return;try{await fetchJson(`/api/users/${del.dataset.deleteUser}`,{method:'DELETE'});setNotice('userNotice',I18N.userDeleted,'success');await loadAll()}catch(err){setNotice('userNotice',err.message,'error')}};
toggleCreateBoxes();loadAll().catch(e=>setNotice('projectFormNotice',e.message,'error'));
</script>
</body>
</html>
''', {"ROOT_DOMAIN": ROOT_DOMAIN, "WEB_PROTOCOL": WEB_PROTOCOL})


LOGIN_PAGE_HTML = r'''
<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tool Nexus Login</title>
<style>
:root{--navy:#082544;--line:#d9e2e8;--muted:#687a8c;--shadow:0 24px 70px rgba(8,37,68,.12)}*{box-sizing:border-box}body{margin:0;font-family:"Microsoft YaHei","PingFang SC",sans-serif;background:linear-gradient(120deg,#f8fafb 0%,#f8fafb 58%,#efe7d6 58%,#efe7d6 100%);color:#17324d}a{text-decoration:none;color:inherit}button,input{font:inherit}.top{display:flex;justify-content:space-between;align-items:center;padding:18px 24px;background:#fff;border-bottom:1px solid var(--line)}.wrap{width:min(1180px,calc(100% - 40px));margin:0 auto;min-height:calc(100vh - 74px);display:grid;grid-template-columns:1.1fr .9fr;gap:34px;align-items:center}.hero h1{font-family:Georgia,"Microsoft YaHei",serif;font-size:clamp(46px,6vw,82px);line-height:.95;margin:0 0 16px;letter-spacing:-.05em}.hero p{font-size:18px;line-height:1.8;color:#536678;max-width:720px}.stats{display:flex;gap:16px;flex-wrap:wrap;margin-top:34px}.stat{background:#fff;border-radius:22px;padding:20px 22px;box-shadow:var(--shadow)}.stat strong{display:block;font-size:30px;margin-top:8px}.card{background:#fffdf8;border-radius:28px;padding:32px;box-shadow:var(--shadow)}.card h2{margin:0 0 8px;font-size:28px;font-family:Georgia,"Microsoft YaHei",serif}.muted{color:var(--muted)}.roles{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin:20px 0}.role{border:2px solid var(--line);border-radius:14px;padding:13px 10px;background:#fff;font-weight:900;cursor:pointer}.role.active{border-color:#153b63;background:#eef4f9}label{display:grid;gap:8px;margin:14px 0;font-size:12px;font-weight:900;color:#7a8da0;letter-spacing:.08em}input{border:1px solid #ccd7df;border-radius:13px;padding:12px 13px;outline:none}.submit{width:100%;border:0;border-radius:15px;background:var(--navy);color:#fff;padding:15px 16px;font-weight:900;margin-top:18px}.notice{min-height:20px;margin-top:14px;color:var(--muted)}.notice.error{color:#b91c1c}.notice.success{color:#15803d}.toggle{margin-top:14px;border:0;background:transparent;color:#4f6478;font-weight:900;cursor:pointer;padding:0}.hidden{display:none!important}@media(max-width:960px){.wrap{grid-template-columns:1fr;padding:28px 0}}
</style>
</head>
<body>
<header class="top"><div style="font-weight:900;font-size:21px">Tool Nexus 资源门户</div><a href="/">返回首页</a></header>
<main class="wrap">
  <section class="hero"><h1>统一接入<br>统一授权</h1><p>登录后可以访问团队网页工具、查看已授权代码仓库的 README，并下载仓库归档。</p><div class="stats"><div class="stat">SSO<strong>ON</strong></div><div class="stat">README<strong>VIEW</strong></div><div class="stat">FRP<strong>READY</strong></div></div></section>
  <section class="card"><h2 id="title">账号登录</h2><p id="help" class="muted">登录后可访问已授权资源。</p><form id="authForm"><div id="roleBlock" class="roles"><button type="button" class="role active" data-role="user">普通用户</button><button type="button" class="role" data-role="admin">管理员</button></div><label>用户名<input id="username" value="zhangsan" required></label><label>密码<input id="password" type="password" value="zhangsan123" required></label><div id="registerFields" class="hidden"><label>昵称<input id="nickname"></label><label>邀请码<input id="inviteCode"></label></div><button class="submit" id="submitButton" type="submit">立即登录</button><div id="notice" class="notice"></div></form><button id="toggle" class="toggle" type="button">没有账号？使用邀请码注册</button></section>
</main>
<script>
let role='user',mode='login';const params=new URLSearchParams(location.search);const nextUrl=params.get('next')||'/';const notice=document.getElementById('notice');const setNotice=(m='',k='')=>{notice.textContent=m;notice.className='notice'+(k?' '+k:'')};async function fetchJson(url,opt={}){const headers={Accept:'application/json',...(opt.headers||{})};if(opt.body && !(opt.body instanceof FormData) && !headers['Content-Type'])headers['Content-Type']='application/json';const res=await fetch(url,{credentials:'include',...opt,headers});const text=await res.text();let payload=null;try{payload=text?JSON.parse(text):null}catch{payload={message:text}}if(!res.ok)throw new Error(payload?.detail||payload?.message||'请求失败');return payload}function setMode(next){mode=next;const reg=mode==='register';document.getElementById('title').textContent=reg?'邀请码注册':'账号登录';document.getElementById('help').textContent=reg?'使用管理员发放的邀请码创建普通用户账号。':'登录后可访问已授权资源。';document.getElementById('registerFields').classList.toggle('hidden',!reg);document.getElementById('roleBlock').classList.toggle('hidden',reg);document.getElementById('submitButton').textContent=reg?'立即注册':'立即登录';document.getElementById('toggle').textContent=reg?'返回登录':'没有账号？使用邀请码注册';setNotice('')}document.querySelectorAll('[data-role]').forEach(b=>b.onclick=()=>{role=b.dataset.role;document.querySelectorAll('[data-role]').forEach(x=>x.classList.toggle('active',x===b))});document.getElementById('toggle').onclick=()=>setMode(mode==='login'?'register':'login');document.getElementById('authForm').onsubmit=async e=>{e.preventDefault();try{const username=document.getElementById('username').value.trim();const password=document.getElementById('password').value;if(mode==='register'){setNotice('注册中...');await fetchJson('/api/register',{method:'POST',body:JSON.stringify({username,nickname:document.getElementById('nickname').value.trim(),password,invite_code:document.getElementById('inviteCode').value.trim()})});setNotice('注册成功，正在跳转...','success');location.href=nextUrl;return}setNotice('登录中...');const data=await fetchJson('/api/login',{method:'POST',body:JSON.stringify({username,password})});if(role==='admin'&&!data.user.is_admin){await fetchJson('/api/logout',{method:'POST'});setNotice('该账号不是管理员。','error');return}setNotice('登录成功，正在跳转...','success');location.href=nextUrl}catch(err){setNotice(err.message,'error')}};
</script>
</body>
</html>
'''
