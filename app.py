from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import sqlite3
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "talentflow.db"
HOST = "0.0.0.0"


HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>TalentFlow AI | Talent workspace</title>
<style>
:root {
  --ink:#17243a; --muted:#738098; --line:#e7ebf2; --paper:#f6f8fc;
  --white:#fff; --navy:#192d4d; --blue:#4b69e8; --blue-soft:#edf1ff;
  --teal:#17a89b; --orange:#f3a34b; --shadow:0 8px 28px rgba(24,45,77,.06);
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:14px/1.5 Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}
button,input,textarea,select{font:inherit}
button{cursor:pointer}
.shell{min-height:100vh;display:grid;grid-template-columns:246px minmax(0,1fr)}
.sidebar{background:var(--navy);color:#d7e0f0;padding:24px 16px;display:flex;flex-direction:column;gap:30px}
.brand{display:flex;align-items:center;gap:11px;padding:0 10px;color:#fff;font-size:18px;font-weight:750;letter-spacing:-.4px}
.brand-mark{width:35px;height:35px;display:grid;place-items:center;border-radius:11px;background:linear-gradient(135deg,#6d85ff,#28c6bd);font-weight:900;color:#fff}
.brand small{display:block;font-size:10px;font-weight:500;color:#a9bad5;letter-spacing:1.5px;text-transform:uppercase}
.nav-label{font-size:10px;letter-spacing:1.5px;color:#8ea1bf;font-weight:700;padding:0 12px;margin-bottom:8px}
.nav{display:grid;gap:6px}
.nav button{border:0;background:transparent;color:#c5d1e4;text-align:left;padding:11px 12px;border-radius:10px;display:flex;align-items:center;gap:12px;font-weight:550}
.nav button .ico{width:20px;text-align:center;font-size:16px}
.nav button:hover,.nav button.active{background:rgba(255,255,255,.12);color:white}
.sidebar-bottom{margin-top:auto;background:rgba(255,255,255,.07);padding:15px;border-radius:13px;color:#d7e0f0;font-size:12px}
.sidebar-bottom strong{display:block;color:#fff;font-size:13px;margin-bottom:4px}
.sidebar-bottom p{margin:0;color:#afbed4}
.main{min-width:0}
.topbar{height:78px;background:#fff;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;padding:0 clamp(18px,3vw,38px);gap:18px}
.crumb{font-size:12px;color:var(--muted)}.crumb strong{color:var(--ink);font-size:14px;margin-left:8px}
.top-right{display:flex;align-items:center;gap:16px}
.searchbox{background:#f7f8fc;border:1px solid var(--line);border-radius:10px;padding:9px 12px;display:flex;align-items:center;gap:8px;width:min(260px,30vw)}
.searchbox input{border:0;outline:0;background:transparent;width:100%;min-width:0}
.avatar{width:37px;height:37px;display:grid;place-items:center;background:#e9edff;color:#4c60c9;border-radius:50%;font-weight:800}
.content{padding:30px clamp(18px,3vw,38px) 42px;max-width:1500px;margin:auto}
.hello{display:flex;align-items:flex-start;justify-content:space-between;gap:18px;margin-bottom:25px}
h1{font-size:27px;line-height:1.2;letter-spacing:-.8px;margin:0 0 7px}
.sub{color:var(--muted);margin:0}
.btn{border:0;border-radius:9px;padding:11px 15px;font-weight:700;display:inline-flex;align-items:center;justify-content:center;gap:8px}
.btn-primary{background:var(--blue);color:#fff;box-shadow:0 5px 12px #4b69e82b}
.btn-primary:hover{background:#3e59d0}.btn-light{background:#fff;border:1px solid var(--line);color:var(--ink)}
.stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin-bottom:22px}
.stat,.panel{background:#fff;border:1px solid var(--line);border-radius:15px;box-shadow:var(--shadow)}
.stat{padding:19px 20px}
.stat-head{display:flex;align-items:center;justify-content:space-between;color:var(--muted);font-size:12px;font-weight:650}
.stat-icon{width:35px;height:35px;border-radius:10px;display:grid;place-items:center;font-size:17px}
.si-blue{background:#edf1ff;color:#4b69e8}.si-teal{background:#e5f8f5;color:#159b8e}.si-orange{background:#fff3e3;color:#db8c2c}.si-purple{background:#f2eaff;color:#9360d5}
.stat-num{font-size:29px;font-weight:800;letter-spacing:-1px;margin:13px 0 1px}
.stat-note{font-size:11px;color:var(--muted)}
.stat-note span{color:#159b8e;font-weight:750}
.columns{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(280px,.9fr);gap:18px}
.panel{padding:21px;min-width:0}
.panel-head{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:17px}
.panel h2{font-size:16px;margin:0;letter-spacing:-.25px}
.panel-desc{font-size:12px;color:var(--muted);margin:4px 0 0}
.link-btn{border:0;background:transparent;color:var(--blue);font-weight:700;padding:5px}
.table-wrap{overflow:auto}
table{border-collapse:collapse;width:100%;min-width:470px}
th{text-align:left;font-size:10px;letter-spacing:1px;text-transform:uppercase;color:#8b96aa;font-weight:750;padding:12px 9px;border-bottom:1px solid var(--line)}
td{padding:14px 9px;border-bottom:1px solid #f0f2f7;color:#48566e;font-size:12px}
tbody tr:last-child td{border-bottom:0}
.person{display:flex;align-items:center;gap:10px;min-width:140px}
.person-avatar{width:32px;height:32px;border-radius:10px;background:#eaf0ff;color:#4c64cb;display:grid;place-items:center;font-size:11px;font-weight:800;flex-shrink:0}
.person strong{display:block;color:var(--ink);font-size:12px}.person small{display:block;color:var(--muted);font-size:11px}
.pill{display:inline-block;padding:5px 8px;border-radius:20px;font-size:10px;font-weight:750;background:#e7f8f3;color:#168b7c}
.empty{padding:28px 12px;text-align:center;color:var(--muted);font-size:12px}
.quick-list{display:grid;gap:12px}
.quick{border:1px solid var(--line);border-radius:12px;padding:14px;display:flex;align-items:center;gap:12px}
.quick-icon{width:38px;height:38px;border-radius:11px;background:var(--blue-soft);display:grid;place-items:center;color:var(--blue);font-size:17px;flex-shrink:0}
.quick strong{display:block;font-size:12px}.quick small{color:var(--muted);font-size:11px}
.quick .arrow{margin-left:auto;color:#a1aabd}
.activity{margin-top:18px}
.activity-row{display:flex;gap:12px;align-items:flex-start;padding:12px 0;border-bottom:1px solid #f0f2f7}
.activity-row:last-child{border:0}.dot{width:9px;height:9px;background:var(--teal);border-radius:50%;margin-top:5px;flex-shrink:0}
.activity-row strong{font-size:12px;display:block}.activity-row small{font-size:11px;color:var(--muted)}
.page-view{display:none}.page-view.active{display:block}
.page-title{margin-bottom:22px}
.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.field{display:grid;gap:6px}.field.full{grid-column:1/-1}.field label{font-size:12px;font-weight:700;color:#46536a}
.field input,.field textarea,.field select{width:100%;border:1px solid #dfe4ee;border-radius:9px;padding:11px 12px;outline:none;background:#fff}
.field input:focus,.field textarea:focus,.field select:focus{border-color:#8b9df8;box-shadow:0 0 0 3px #4b69e815}
.field textarea{min-height:105px;resize:vertical}
.form-actions{display:flex;gap:10px;justify-content:flex-end;margin-top:16px}
.notice{font-size:12px;color:var(--muted);margin-top:12px;min-height:18px}
.filter-row{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:16px}.filter-row input{flex:1;min-width:190px;border:1px solid var(--line);padding:10px 12px;border-radius:9px}
.info-banner{padding:15px;border-radius:12px;background:#f0f4ff;border:1px solid #dfe6ff;color:#42578d;font-size:12px;margin-bottom:16px}
.job-list{display:grid;gap:12px;margin-top:16px}
.job-card{border:1px solid var(--line);border-radius:12px;padding:16px;display:grid;gap:10px}
.job-card-head{display:flex;justify-content:space-between;align-items:flex-start;gap:12px}
.job-card h3{margin:0;font-size:15px;color:var(--ink)}
.job-card p{margin:0;color:var(--muted);font-size:12px;white-space:pre-wrap;overflow-wrap:anywhere}
.job-meta{display:flex;gap:8px;flex-wrap:wrap;color:var(--muted);font-size:11px}
.job-actions{display:flex;gap:8px;flex-wrap:wrap}
.btn-small{padding:7px 10px;font-size:11px;border-radius:7px}
footer{font-size:11px;color:#9aa4b5;text-align:center;padding:24px 0 0}
@media(max-width:1100px){.stats{grid-template-columns:repeat(2,minmax(0,1fr))}.columns{grid-template-columns:1fr}}
@media(max-width:720px){.shell{grid-template-columns:1fr}.sidebar{padding:13px;gap:12px}.brand{padding:0 5px}.nav-label,.sidebar-bottom{display:none}.nav{grid-template-columns:repeat(5,minmax(0,1fr));gap:4px}.nav button{padding:9px 5px;justify-content:center;flex-direction:column;gap:3px;font-size:10px}.nav button .ico{font-size:15px}.topbar{height:64px}.searchbox{width:45vw}.content{padding-top:22px}.hello{flex-direction:column}.hello .btn{width:100%}.stats{gap:10px}.stat{padding:14px}.stat-num{font-size:25px}.panel{padding:15px}.form-grid{grid-template-columns:1fr}.field.full{grid-column:auto}h1{font-size:24px}}
</style>
</head>
<body>
<div class="shell">
  <aside class="sidebar">
    <div class="brand"><div class="brand-mark">T</div><div>TalentFlow <small>AI talent workspace</small></div></div>
    <div>
      <div class="nav-label">WORKSPACE</div>
      <nav class="nav" aria-label="Main navigation">
        <button class="active" data-page="dashboard"><span class="ico">▦</span>Dashboard</button>
        <button data-page="candidates"><span class="ico">♙</span>Candidates</button>
        <button data-page="applications"><span class="ico">▤</span>Applications</button>
        <button data-page="jobs"><span class="ico">▣</span>Jobs</button>
        <button data-page="matching"><span class="ico">✦</span>AI Matching</button>
      </nav>
    </div>
    <div class="sidebar-bottom"><strong>TalentFlow workspace</strong><p>Recruitment overview and candidate application tracking.</p></div>
  </aside>
  <main class="main">
    <header class="topbar">
      <div class="crumb">Workspace / <strong id="crumb-title">Dashboard</strong></div>
      <div class="top-right">
        <label class="searchbox" aria-label="Search applications"><span>⌕</span><input id="global-search" placeholder="Search applications..." /></label>
        <div class="avatar" title="Workspace profile">TF</div>
      </div>
    </header>
    <div class="content">
      <section class="page-view active" id="page-dashboard">
        <div class="hello">
          <div><h1>Good to see you 👋</h1><p class="sub">Here’s what’s happening in your talent workspace today.</p></div>
          <button class="btn btn-primary" id="new-candidate">＋ Add candidate</button>
        </div>
        <div class="stats">
          <article class="stat"><div class="stat-head">Total applications <span class="stat-icon si-blue">▤</span></div><div class="stat-num" id="stat-total">—</div><div class="stat-note">Applications saved in this demo</div></article>
          <article class="stat"><div class="stat-head">Candidate profiles <span class="stat-icon si-teal">♙</span></div><div class="stat-num" id="stat-candidates">—</div><div class="stat-note">Based on submitted applications</div></article>
          <article class="stat"><div class="stat-head">Job categories <span class="stat-icon si-orange">▣</span></div><div class="stat-num" id="stat-jobs">—</div><div class="stat-note">Distinct job titles submitted</div></article>
          <article class="stat"><div class="stat-head">New today <span class="stat-icon si-purple">✦</span></div><div class="stat-num" id="stat-today">—</div><div class="stat-note">Applications created today</div></article>
        </div>
        <div class="columns">
          <section class="panel">
            <div class="panel-head"><div><h2>Recent applications</h2><p class="panel-desc">Latest candidates submitted to the workspace</p></div><button class="link-btn" data-goto="applications">View all →</button></div>
            <div class="table-wrap"><table><thead><tr><th>Candidate</th><th>Job title</th><th>Submitted</th><th>Status</th></tr></thead><tbody id="recent-rows"><tr><td colspan="4" class="empty">Loading applications…</td></tr></tbody></table></div>
          </section>
          <section class="panel">
            <div class="panel-head"><div><h2>Quick actions</h2><p class="panel-desc">Common workspace tasks</p></div></div>
            <div class="quick-list">
              <button class="quick" data-goto="candidates" style="text-align:left;background:#fff;width:100%"><span class="quick-icon">♙</span><span><strong>Add a candidate</strong><small>Submit candidate details and skills</small></span><span class="arrow">›</span></button>
              <button class="quick" data-goto="applications" style="text-align:left;background:#fff;width:100%"><span class="quick-icon">▤</span><span><strong>Review applications</strong><small>Browse submitted candidate records</small></span><span class="arrow">›</span></button>
              <button class="quick" data-goto="jobs" style="text-align:left;background:#fff;width:100%"><span class="quick-icon">▣</span><span><strong>Job workspace</strong><small>See current implementation status</small></span><span class="arrow">›</span></button>
            </div>
            <div class="activity"><div class="panel-head"><h2>Workspace activity</h2></div><div class="activity-row"><span class="dot"></span><div><strong>Candidate records are stored locally</strong><small>SQLite database · this application instance</small></div></div><div class="activity-row"><span class="dot" style="background:#f3a34b"></span><div><strong>Skills-based matching is available</strong><small>Compare candidate skills with saved job requirements</small></div></div></div>
          </section>
        </div>
        <footer>TalentFlow AI · Internship demo workspace</footer>
      </section>

      <section class="page-view" id="page-candidates">
        <div class="page-title"><h1>Candidate management</h1><p class="sub">Capture candidate details and submit an application to the local database.</p></div>
        <div class="columns">
          <section class="panel">
            <div class="panel-head"><div><h2>Candidate details</h2><p class="panel-desc">Fields marked required must be completed.</p></div></div>
            <form id="application-form">
              <div class="form-grid">
                <div class="field"><label for="name">Full name *</label><input id="name" name="name" placeholder="e.g. Alex Morgan" maxlength="100" required></div>
                <div class="field"><label for="email">Email address *</label><input id="email" name="email" type="email" placeholder="alex@example.com" maxlength="254" required></div>
                <div class="field full"><label for="job">Applying for *</label><input id="job" name="job" placeholder="e.g. Junior Cloud Engineer" maxlength="150" required></div>
                <div class="field full"><label for="skills">Skills and experience *</label><textarea id="skills" name="skills" placeholder="Add relevant skills, tools, and experience…" maxlength="3000" required></textarea></div>
              </div>
              <div class="form-actions"><button type="reset" class="btn btn-light">Clear form</button><button type="submit" class="btn btn-primary">Submit application →</button></div>
              <p class="notice" id="form-result" role="status"></p>
            </form>
          </section>
          <section class="panel"><div class="panel-head"><div><h2>Submission checklist</h2><p class="panel-desc">Before saving a candidate</p></div></div><div class="quick-list"><div class="quick"><span class="quick-icon">✓</span><span><strong>Contact details</strong><small>Enter a valid email address</small></span></div><div class="quick"><span class="quick-icon">✓</span><span><strong>Target role</strong><small>Specify the job title</small></span></div><div class="quick"><span class="quick-icon">✓</span><span><strong>Skills summary</strong><small>Include relevant skills and tools</small></span></div></div><p class="notice">Demo note: use fictional candidate data when testing. Applications are saved to the local SQLite database.</p></section>
        </div>
        <footer>TalentFlow AI · Candidate management</footer>
      </section>

      <section class="page-view" id="page-applications">
        <div class="page-title"><h1>Applications</h1><p class="sub">Browse the applications stored in this project’s SQLite database.</p></div>
        <section class="panel">
          <div class="panel-head"><div><h2>All applications</h2><p class="panel-desc" id="application-count">Loading records…</p></div><button class="btn btn-primary" data-goto="candidates">＋ Add candidate</button></div>
          <div class="filter-row"><input id="table-search" placeholder="Search by name, email, role, or skills…" aria-label="Filter applications"></div>
          <div class="table-wrap"><table><thead><tr><th>Candidate</th><th>Job title</th><th>Skills</th><th>Submitted</th><th>Status</th></tr></thead><tbody id="all-rows"><tr><td colspan="5" class="empty">Loading applications…</td></tr></tbody></table></div>
        </section>
        <footer>TalentFlow AI · Application tracking</footer>
      </section>

      <section class="page-view" id="page-jobs">
        <div class="page-title"><h1>Job management</h1><p class="sub">Create and maintain job postings stored in your local SQLite database.</p></div>
        <div class="columns">
          <section class="panel">
            <div class="panel-head"><div><h2 id="job-form-heading">Create a job posting</h2><p class="panel-desc">Add the role details below. Required fields are marked.</p></div></div>
            <form id="job-form">
              <input type="hidden" id="job-id" value="">
              <div class="form-grid">
                <div class="field"><label for="job-title">Job title *</label><input id="job-title" maxlength="150" required placeholder="e.g. Junior Cloud Engineer"></div>
                <div class="field"><label for="job-company">Company *</label><input id="job-company" maxlength="150" required placeholder="e.g. TalentFlow Demo"></div>
                <div class="field"><label for="job-experience">Experience level *</label><select id="job-experience" required><option value="">Select level</option><option>Fresher</option><option>0–1 years</option><option>1–3 years</option><option>3–5 years</option><option>5+ years</option></select></div>
                <div class="field"><label for="job-skills">Required skills *</label><input id="job-skills" maxlength="1000" required placeholder="AWS, Linux, Python"></div>
                <div class="field full"><label for="job-description">Job description *</label><textarea id="job-description" maxlength="5000" required placeholder="Responsibilities and role details…"></textarea></div>
              </div>
              <div class="form-actions"><button type="button" id="job-cancel-edit" class="btn btn-light" style="display:none">Cancel edit</button><button type="reset" class="btn btn-light">Clear form</button><button type="submit" id="job-submit" class="btn btn-primary">Save job posting →</button></div>
              <p class="notice" id="job-form-result" role="status"></p>
            </form>
          </section>
          <section class="panel"><div class="panel-head"><div><h2>Job postings</h2><p class="panel-desc" id="jobs-count">Loading jobs…</p></div><button class="btn btn-light btn-small" id="refresh-jobs" type="button">Refresh</button></div><div id="jobs-list" class="job-list"><div class="empty">Loading jobs…</div></div></section>
        </div>
        <footer>TalentFlow AI · Job management</footer>
      </section>

      <section class="page-view" id="page-matching">
        <div class="page-title"><h1>AI candidate matching</h1><p class="sub">Compare candidate skills with a selected job and review matched and missing skills.</p></div>
        <section class="panel">
          <div class="info-banner">This first version uses transparent, skills-based matching—not a trained AI model. Scores show the percentage of required job skills found in each candidate’s saved skills summary.</div>
          <div class="form-grid">
            <div class="field"><label for="match-job-select">Select job posting *</label><select id="match-job-select"><option value="">Choose a saved job…</option></select></div>
            <div class="field" style="align-content:end"><button type="button" class="btn btn-primary" id="run-matching">Find candidate matches →</button></div>
          </div>
          <p class="notice" id="match-status" role="status"></p>
          <div id="match-results" class="job-list"><div class="empty">Choose a job and run matching to see candidate results.</div></div>
        </section>
        <footer>TalentFlow AI · Skills-based candidate matching</footer>
      </section>
    </div>
  </main>
</div>
<script>
const $ = (selector) => document.querySelector(selector);
let applications = [];

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, char => ({
    "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;"
  })[char]);
}
function initials(name) {
  return String(name || "?").trim().split(/\s+/).slice(0,2).map(part => part[0] || "").join("").toUpperCase();
}
function formatDate(value) {
  if (!value) return "—";
  const parsed = new Date(value.replace(" ", "T") + (value.includes("Z") ? "" : "Z"));
  return Number.isNaN(parsed.getTime()) ? value : parsed.toLocaleDateString(undefined,{month:"short",day:"numeric",year:"numeric"});
}
function renderRows(rows, target, columns) {
  const body = $(target);
  if (!rows.length) {
    body.innerHTML = `<tr><td colspan="${columns}" class="empty">No applications yet. Add a candidate to see records here.</td></tr>`;
    return;
  }
  body.innerHTML = rows.map(item => {
    const name = escapeHtml(item.name);
    const email = escapeHtml(item.email);
    const job = escapeHtml(item.job);
    const skills = escapeHtml(item.skills);
    const date = escapeHtml(formatDate(item.created_at));
    const person = `<div class="person"><span class="person-avatar">${escapeHtml(initials(item.name))}</span><span><strong>${name}</strong><small>${email}</small></span></div>`;
    if (columns === 4) return `<tr><td>${person}</td><td>${job}</td><td>${date}</td><td><span class="pill">Submitted</span></td></tr>`;
    return `<tr><td>${person}</td><td>${job}</td><td>${skills}</td><td>${date}</td><td><span class="pill">Submitted</span></td></tr>`;
  }).join("");
}
function applySearch() {
  const query = (($("#table-search")?.value || "") + " " + ($("#global-search")?.value || "")).trim().toLowerCase();
  const filtered = applications.filter(item => [item.name,item.email,item.job,item.skills].some(v => String(v || "").toLowerCase().includes(query)));
  renderRows(filtered, "#all-rows", 5);
  $("#application-count").textContent = `${filtered.length} of ${applications.length} application${applications.length === 1 ? "" : "s"}`;
  renderRows(applications.slice(0,5), "#recent-rows", 4);
}
async function loadApplications() {
  try {
    const response = await fetch("/api/applications", {cache:"no-store"});
    if (!response.ok) throw new Error("Could not load application records.");
    const data = await response.json();
    applications = data.applications || [];
    $("#stat-total").textContent = data.stats.total;
    $("#stat-candidates").textContent = data.stats.candidates;
    $("#stat-jobs").textContent = data.stats.job_titles;
    $("#stat-today").textContent = data.stats.today;
    applySearch();
  } catch (error) {
    $("#recent-rows").innerHTML = `<tr><td colspan="4" class="empty">Unable to load records. ${escapeHtml(error.message)}</td></tr>`;
    $("#all-rows").innerHTML = `<tr><td colspan="5" class="empty">Unable to load records.</td></tr>`;
  }
}
let jobs = [];
function resetJobForm() {
  $("#job-form").reset(); $("#job-id").value = "";
  $("#job-form-heading").textContent = "Create a job posting";
  $("#job-submit").textContent = "Save job posting →";
  $("#job-cancel-edit").style.display = "none";
  $("#job-form-result").textContent = "";
}
function renderJobs() {
  $("#jobs-count").textContent = `${jobs.length} job posting${jobs.length === 1 ? "" : "s"}`;
  if (!jobs.length) { $("#jobs-list").innerHTML = '<div class="empty">No job postings yet. Create the first one using the form.</div>'; return; }
  $("#jobs-list").innerHTML = jobs.map(job => `<article class="job-card"><div class="job-card-head"><div><h3>${escapeHtml(job.title)}</h3><div class="job-meta">${escapeHtml(job.company)} · ${escapeHtml(job.experience)}</div></div><span class="pill">Saved</span></div><p><strong>Required skills:</strong> ${escapeHtml(job.skills)}</p><p>${escapeHtml(job.description)}</p><div class="job-meta">Created ${escapeHtml(formatDate(job.created_at))}</div><div class="job-actions"><button class="btn btn-light btn-small" type="button" data-job-edit="${job.id}">Edit</button><button class="btn btn-light btn-small" type="button" data-job-delete="${job.id}">Delete</button></div></article>`).join("");
}
async function loadJobs() {
  try { const response = await fetch("/api/jobs", {cache:"no-store"}); const data = await response.json(); if (!response.ok) throw new Error(data.error || "Could not load jobs."); jobs = data.jobs || []; renderJobs(); }
  catch (error) { $("#jobs-list").innerHTML = `<div class="empty">Unable to load jobs. ${escapeHtml(error.message)}</div>`; }
}
$("#job-form").addEventListener("submit", async event => {
  event.preventDefault(); const result = $("#job-form-result"); const id = $("#job-id").value;
  const payload = {title:$("#job-title").value.trim(), company:$("#job-company").value.trim(), experience:$("#job-experience").value, skills:$("#job-skills").value.trim(), description:$("#job-description").value.trim()};
  const submit = $("#job-submit"); submit.disabled = true; result.textContent = "Saving job…";
  try { const response = await fetch(id ? `/api/jobs/${id}` : "/api/jobs", {method:id ? "PUT" : "POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(payload)}); const data = await response.json(); if (!response.ok) throw new Error(data.error || "Could not save job."); result.textContent = id ? "Job updated successfully." : "Job posting created successfully."; result.style.color = "#168b7c"; resetJobForm(); await loadJobs(); }
  catch (error) { result.textContent = `Error: ${error.message}`; result.style.color = "#bd3b46"; }
  finally { submit.disabled = false; }
});
$("#job-cancel-edit").addEventListener("click", resetJobForm);
$("#job-form").addEventListener("reset", () => { const result = $("#job-form-result"); if (result) result.textContent = ""; });
$("#refresh-jobs").addEventListener("click", loadJobs);
$("#jobs-list").addEventListener("click", async event => {
  const editButton = event.target.closest("[data-job-edit]"); const deleteButton = event.target.closest("[data-job-delete]");
  if (editButton) { const job = jobs.find(item => item.id === Number(editButton.dataset.jobEdit)); if (!job) return; $("#job-id").value = job.id; $("#job-title").value = job.title; $("#job-company").value = job.company; $("#job-experience").value = job.experience; $("#job-skills").value = job.skills; $("#job-description").value = job.description; $("#job-form-heading").textContent = "Edit job posting"; $("#job-submit").textContent = "Update job posting →"; $("#job-cancel-edit").style.display = "inline-flex"; $("#job-form-result").textContent = "Editing selected job."; $("#job-form").scrollIntoView({behavior:"smooth",block:"start"}); }
  if (deleteButton) { const id = Number(deleteButton.dataset.jobDelete); const job = jobs.find(item => item.id === id); if (!job || !window.confirm(`Delete job posting “${job.title}”?`)) return; try { const response = await fetch(`/api/jobs/${id}`, {method:"DELETE"}); const data = await response.json(); if (!response.ok) throw new Error(data.error || "Could not delete job."); await loadJobs(); } catch (error) { window.alert(error.message); } }
});

function populateMatchJobs() {
  const select = $("#match-job-select");
  const previous = select.value;
  select.innerHTML = '<option value="">Choose a saved job…</option>' + jobs.map(job => `<option value="${job.id}">${escapeHtml(job.title)} — ${escapeHtml(job.company)}</option>`).join("");
  if (jobs.some(job => String(job.id) === previous)) select.value = previous;
}
function renderMatches(matches) {
  const target = $("#match-results");
  if (!matches.length) { target.innerHTML = '<div class="empty">No candidate applications found yet. Add candidate applications first, then run matching again.</div>'; return; }
  target.innerHTML = matches.map(item => {
    const score = Number(item.score) || 0;
    const matched = item.matched_skills.length ? item.matched_skills.map(escapeHtml).join(", ") : "None identified";
    const missing = item.missing_skills.length ? item.missing_skills.map(escapeHtml).join(", ") : "None";
    const matchedCount = Number(item.matched_count ?? item.matched_skills.length);
    const requiredCount = Number(item.required_count ?? (item.matched_skills.length + item.missing_skills.length));
    const scoreExplanation = requiredCount > 0
      ? `${matchedCount} of ${requiredCount} required skills matched (${matchedCount} ÷ ${requiredCount} × 100 = ${score}%).`
      : "No required skills were available to calculate a score.";
    return `<article class="job-card"><div class="job-card-head"><div><h3>${escapeHtml(item.name)}</h3><div class="job-meta">${escapeHtml(item.email)} · Applied for: ${escapeHtml(item.job)}</div></div><span class="pill">${score}% skill match</span></div><div style="height:8px;background:#edf0f7;border-radius:99px;overflow:hidden"><div style="height:100%;width:${score}%;background:#4b69e8;border-radius:99px"></div></div><p><strong>How the score is calculated:</strong> ${escapeHtml(scoreExplanation)}</p><p><strong>Matched skills:</strong> ${matched}</p><p><strong>Missing required skills:</strong> ${missing}</p><p><strong>Candidate skills summary:</strong> ${escapeHtml(item.skills)}</p><div class="job-meta">Submitted ${escapeHtml(formatDate(item.created_at))}</div></article>`;
  }).join("");
}
async function runMatching() {
  const jobId = $("#match-job-select").value;
  const status = $("#match-status");
  if (!jobId) { status.textContent = "Please select a job posting first."; status.style.color = "#bd3b46"; return; }
  status.textContent = "Comparing saved candidate skills…"; status.style.color = "var(--muted)";
  try {
    const response = await fetch(`/api/matches?job_id=${encodeURIComponent(jobId)}`, {cache:"no-store"});
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Could not calculate matches.");
    renderMatches(data.matches || []);
    status.textContent = `Compared ${data.matches.length} candidate application${data.matches.length === 1 ? "" : "s"} with ${data.job.title}. Scores are based on required-skill overlap.`;
    status.style.color = "#168b7c";
  } catch (error) { status.textContent = `Error: ${error.message}`; status.style.color = "#bd3b46"; }
}
$("#run-matching").addEventListener("click", runMatching);
function navigate(page) {
  document.querySelectorAll(".page-view").forEach(el => el.classList.toggle("active", el.id === `page-${page}`));
  document.querySelectorAll(".nav button[data-page]").forEach(el => el.classList.toggle("active", el.dataset.page === page));
  const label = ({dashboard:"Dashboard",candidates:"Candidates",applications:"Applications",jobs:"Jobs",matching:"AI Matching"})[page] || "Dashboard";
  $("#crumb-title").textContent = label;
  if (page === "applications") applySearch();
  if (page === "jobs" || page === "matching") loadJobs().then(populateMatchJobs);
  window.scrollTo({top:0,behavior:"smooth"});
}
document.querySelectorAll("[data-page]").forEach(button => button.addEventListener("click", () => navigate(button.dataset.page)));
document.querySelectorAll("[data-goto]").forEach(button => button.addEventListener("click", () => navigate(button.dataset.goto)));
$("#new-candidate").addEventListener("click", () => navigate("candidates"));
$("#global-search").addEventListener("input", applySearch);
$("#table-search").addEventListener("input", applySearch);
$("#application-form").addEventListener("submit", async event => {
  event.preventDefault();
  const form = event.currentTarget;
  const result = $("#form-result");
  const submit = form.querySelector('button[type="submit"]');
  submit.disabled = true;
  submit.textContent = "Saving…";
  result.textContent = "Saving application…";
  const data = Object.fromEntries(new FormData(form).entries());
  try {
    const response = await fetch("/apply", {
      method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(data)
    });
    const answer = await response.json();
    if (!response.ok) throw new Error(answer.error || "Submission failed.");
    result.textContent = `Application saved successfully. Record ID: ${answer.id}`;
    result.style.color = "#168b7c";
    form.reset();
    await loadApplications();
  } catch (error) {
    result.textContent = `Error: ${error.message}`;
    result.style.color = "#bd3b46";
  } finally {
    submit.disabled = false;
    submit.textContent = "Submit application →";
  }
});
$("#application-form").addEventListener("reset", () => {
  const result = $("#form-result");
  result.textContent = "";
});
loadApplications();
loadJobs().then(populateMatchJobs);
</script>
</body>
</html>
"""


def initialize_database():
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                job TEXT NOT NULL,
                skills TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                description TEXT NOT NULL,
                skills TEXT NOT NULL,
                experience TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            body = HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return
        if path == "/api/applications":
            try:
                with sqlite3.connect(DB_PATH) as connection:
                    connection.row_factory = sqlite3.Row
                    rows = connection.execute("""
                        SELECT id, name, email, job, skills, created_at
                        FROM applications ORDER BY id DESC
                    """).fetchall()
                    today = connection.execute("""
                        SELECT COUNT(*) FROM applications
                        WHERE date(created_at) = date('now','localtime')
                    """).fetchone()[0]
                records = [dict(row) for row in rows]
                stats = {
                    "total": len(records),
                    "candidates": len({(item["name"].strip().lower(), item["email"].strip().lower()) for item in records}),
                    "job_titles": len({item["job"].strip().lower() for item in records if item["job"].strip()}),
                    "today": today,
                }
                self.send_json(200, {"applications": records, "stats": stats})
            except sqlite3.Error:
                self.send_json(500, {"error": "Could not read application database"})
            return
        if path == "/api/jobs":
            try:
                with sqlite3.connect(DB_PATH) as connection:
                    connection.row_factory = sqlite3.Row
                    rows = connection.execute("SELECT id, title, company, description, skills, experience, created_at FROM jobs ORDER BY id DESC").fetchall()
                self.send_json(200, {"jobs": [dict(row) for row in rows]})
            except sqlite3.Error:
                self.send_json(500, {"error": "Could not read jobs database"})
            return
        if path == "/api/matches":
            try:
                query = urlparse(self.path).query
                from urllib.parse import parse_qs
                raw_id = parse_qs(query).get("job_id", [""])[0]
                job_id = int(raw_id)
                with sqlite3.connect(DB_PATH) as connection:
                    connection.row_factory = sqlite3.Row
                    job_row = connection.execute("SELECT id, title, skills FROM jobs WHERE id=?", (job_id,)).fetchone()
                    application_rows = connection.execute("SELECT id, name, email, job, skills, created_at FROM applications ORDER BY id DESC").fetchall()
                if job_row is None:
                    self.send_json(404, {"error": "Job posting not found"}); return
                def split_skills(value):
                    import re
                    parts = re.split(r"[,;\n|]+", str(value or ""))
                    cleaned = []
                    for part in parts:
                        skill = " ".join(part.lower().strip().split())
                        if skill and skill not in cleaned:
                            cleaned.append(skill)
                    return cleaned
                required = split_skills(job_row["skills"])
                matches = []
                for row in application_rows:
                    candidate = dict(row)
                    candidate_skills = split_skills(candidate["skills"])
                    matched = [skill for skill in required if any(skill == cs or skill in cs or cs in skill for cs in candidate_skills)]
                    missing = [skill for skill in required if skill not in matched]
                    score = round((len(matched) / len(required)) * 100) if required else 0
                    candidate.update({"score": score, "matched_skills": matched, "missing_skills": missing,
                                      "matched_count": len(matched), "required_count": len(required)})
                    matches.append(candidate)
                matches.sort(key=lambda item: (-item["score"], item["name"].lower()))
                self.send_json(200, {"job": {"id": job_row["id"], "title": job_row["title"]}, "matches": matches})
            except (ValueError, TypeError):
                self.send_json(400, {"error": "Please select a valid job posting"})
            except sqlite3.Error:
                self.send_json(500, {"error": "Could not calculate candidate matches"})
            return
        self.send_json(404, {"error": "Page not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/api/jobs":
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length <= 0 or length > 12000:
                    self.send_json(400, {"error": "Invalid request size"}); return
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
                if not isinstance(payload, dict): raise ValueError("Invalid job data")
                values = [str(payload.get(key, "")).strip() for key in ("title", "company", "description", "skills", "experience")]
                if not all(values): self.send_json(400, {"error": "Please complete all job fields"}); return
                if len(values[0]) > 150 or len(values[1]) > 150 or len(values[2]) > 5000 or len(values[3]) > 1000 or len(values[4]) > 50:
                    self.send_json(400, {"error": "One or more job fields are too long"}); return
                with sqlite3.connect(DB_PATH) as connection:
                    cursor = connection.execute("INSERT INTO jobs (title, company, description, skills, experience) VALUES (?, ?, ?, ?, ?)", tuple(values))
                    job_id = cursor.lastrowid
                self.send_json(201, {"message": "Job created", "id": job_id})
            except (json.JSONDecodeError, UnicodeDecodeError, ValueError): self.send_json(400, {"error": "Invalid job data"})
            except sqlite3.Error: self.send_json(500, {"error": "Database error; job not saved"})
            return
        if path != "/apply":
            self.send_json(404, {"error": "Endpoint not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 16000:
                self.send_json(400, {"error": "Invalid request size"})
                return
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            if not isinstance(payload, dict):
                raise ValueError("Invalid application data")
            name = str(payload.get("name", "")).strip()
            email = str(payload.get("email", "")).strip()
            job = str(payload.get("job", "")).strip()
            skills = str(payload.get("skills", "")).strip()
            if not all([name, email, job, skills]):
                self.send_json(400, {"error": "Please complete all fields"})
                return
            if (len(name) > 100 or len(email) > 254 or len(job) > 150 or
                    len(skills) > 3000 or "@" not in email):
                self.send_json(400, {"error": "Please check your input"})
                return
            with sqlite3.connect(DB_PATH) as connection:
                cursor = connection.execute(
                    """INSERT INTO applications (name, email, job, skills)
                       VALUES (?, ?, ?, ?)""", (name, email, job, skills)
                )
                application_id = cursor.lastrowid
            self.send_json(201, {"message": "Application saved", "id": application_id})
        except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
            self.send_json(400, {"error": "Invalid application data"})
        except sqlite3.Error:
            self.send_json(500, {"error": "Database error; application not saved"})
        except Exception:
            self.send_json(500, {"error": "Unexpected server error"})

    def do_PUT(self):
        path = urlparse(self.path).path
        parts = path.strip("/").split("/")
        if len(parts) != 3 or parts[:2] != ["api", "jobs"]:
            self.send_json(404, {"error": "Endpoint not found"}); return
        try:
            job_id = int(parts[2])
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 12000: self.send_json(400, {"error": "Invalid request size"}); return
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            values = [str(payload.get(key, "")).strip() for key in ("title", "company", "description", "skills", "experience")]
            if not all(values): self.send_json(400, {"error": "Please complete all job fields"}); return
            if len(values[0]) > 150 or len(values[1]) > 150 or len(values[2]) > 5000 or len(values[3]) > 1000 or len(values[4]) > 50:
                self.send_json(400, {"error": "One or more job fields are too long"}); return
            with sqlite3.connect(DB_PATH) as connection:
                cursor = connection.execute("UPDATE jobs SET title=?, company=?, description=?, skills=?, experience=? WHERE id=?", (*values, job_id))
                if cursor.rowcount == 0: self.send_json(404, {"error": "Job not found"}); return
            self.send_json(200, {"message": "Job updated", "id": job_id})
        except (ValueError, json.JSONDecodeError, UnicodeDecodeError): self.send_json(400, {"error": "Invalid job data"})
        except sqlite3.Error: self.send_json(500, {"error": "Database error; job not updated"})

    def do_DELETE(self):
        path = urlparse(self.path).path
        parts = path.strip("/").split("/")
        if len(parts) != 3 or parts[:2] != ["api", "jobs"]:
            self.send_json(404, {"error": "Endpoint not found"}); return
        try:
            job_id = int(parts[2])
            with sqlite3.connect(DB_PATH) as connection:
                cursor = connection.execute("DELETE FROM jobs WHERE id=?", (job_id,))
                if cursor.rowcount == 0: self.send_json(404, {"error": "Job not found"}); return
            self.send_json(200, {"message": "Job deleted", "id": job_id})
        except ValueError: self.send_json(400, {"error": "Invalid job ID"})
        except sqlite3.Error: self.send_json(500, {"error": "Database error; job not deleted"})

    def log_message(self, format, *args):
        print("%s - %s" % (self.address_string(), format % args))


if __name__ == "__main__":
    initialize_database()
    server = HTTPServer((HOST, 8000), Handler)
    print("TalentFlow AI running at http://127.0.0.1:8000")
    print(f"SQLite database: {DB_PATH}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\\nServer stopped.")
        server.server_close()
