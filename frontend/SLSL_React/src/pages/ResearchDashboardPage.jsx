import React from "react";
import { UserNav, ResearchSidebar } from "../components/Navigation";

export default function ResearchDashboardPage() {
  
  return (<>

<div className="research-shell">
<ResearchSidebar />
<main className="research-main">
<header className="research-topbar">
<div>
<h1>Research Dashboard</h1>
<p>Experimental workspace and evaluation protocol for the SLSL research project.</p>
</div>
<div className="research-account">
<span className="research-avatar">I</span>
<div>
<strong>Ishini</strong>
<small>Researcher</small>
</div>
</div>
</header>

<section className="section">
<div className="section-heading">
<div>
<h2>Research Modules</h2>
<p>Explore individual operational and evaluation components.</p>
</div>
</div>
<div className="module-grid">
<article className="module-card recognition">
<h3>SLSL Recognition</h3>
<p>Signer-independent recognition, similar-sign confusions, and environmental robustness.</p>
<a href="/recognition-analysis">Open Analysis →</a>
<span className="module-art" aria-hidden="true">📷</span>
</article>
<article className="module-card translation">
<h3>Context Translation</h3>
<p>Temporal SLSL gloss sequence to natural Sinhala and English sentence reconstruction.</p>
<a href="/translation">Open Prototype →</a>
<span className="module-art" aria-hidden="true">文</span>
</article>
<article className="module-card learning">
<h3>Error Detection</h3>
<p>Automated motion error analysis on hand shape, spatial position, and movement trajectory.</p>
<a href="/learn">Open Prototype →</a>
<span className="module-art" aria-hidden="true">🎓</span>
</article>
<article className="module-card communication">
<h3>Bidirectional System</h3>
<p>End-to-end Deaf ↔ hearing communication workflow with context-aware sign selection.</p>
<a href="/communication">Open Prototype →</a>
<span className="module-art" aria-hidden="true">💬</span>
</article>
</div>
</section>

<section className="section">
<div className="section-heading">
<div>
<h2>System &amp; Dataset Overview</h2>
<p>Current prototype counts and evaluation status.</p>
</div>
</div>
<div className="overview-grid">
<article className="card overview-card">
<span className="overview-icon">☝</span>
<div>
<span>Sign Vocabulary</span>
<strong>12</strong>
<small>Pilot sign IDs — unreviewed</small>
</div>
</article>
<article className="card overview-card">
<span className="overview-icon">▧</span>
<div>
<span>Gesture Samples</span>
<strong>22</strong>
<small>Pilot expert videos</small>
</div>
</article>
<article className="card overview-card">
<span className="overview-icon">👥</span>
<div>
<span>Pilot signers</span>
<strong>2</strong>
<small>Signer-disjoint protocol</small>
</div>
</article>
<article className="card overview-card">
<span className="overview-icon">▥</span>
<div>
<span>Overall Accuracy</span>
<strong style={{color: "var(--text-secondary)"}}>—</strong>
<small>Awaiting evaluation</small>
</div>
</article>
</div>
</section>

<section className="section lower-grid">
<article className="card workflow-card">
<h3>End-to-End System Workflow</h3>
<div className="flow-label">1. Deaf → Hearing Flow</div>
<div className="workflow-row">
<div className="workflow-step">
<span className="icon">🤟</span>
<strong>Deaf User</strong>
<small>Camera input</small>
</div>
<div className="workflow-step">
<span className="icon">📷</span>
<strong>Recognition</strong>
<small>Sign sequence</small>
</div>
<div className="workflow-step">
<span className="icon">文</span>
<strong>Translation</strong>
<small>Sinhala / English</small>
</div>
<div className="workflow-step">
<span className="icon">🔊</span>
<strong>Hearing User</strong>
<small>Text &amp; voice</small>
</div>
</div>
<div className="flow-label">2. Hearing → Deaf Flow</div>
<div className="workflow-row">
<div className="workflow-step">
<span className="icon">🎤</span>
<strong>Hearing User</strong>
<small>Voice / text reply</small>
</div>
<div className="workflow-step">
<span className="icon">🧠</span>
<strong>Context Engine</strong>
<small>Intent extraction</small>
</div>
<div className="workflow-step">
<span className="icon">☝</span>
<strong>Sign Selection</strong>
<small>Variant matching</small>
</div>
<div className="workflow-step">
<span className="icon">🤟</span>
<strong>Deaf User</strong>
<small>SLSL response</small>
</div>
</div>
<div className="flow-label">3. Automated Learner Feedback</div>
<div className="workflow-row">
<div className="workflow-step">
<span className="icon">👤</span>
<strong>Learner Gesture</strong>
<small>Live camera</small>
</div>
<div className="workflow-step">
<span className="icon">⌕</span>
<strong>Error Analysis</strong>
<small>Shape/Pos/Move</small>
</div>
<div className="workflow-step">
<span className="icon">💬</span>
<strong>Bilingual Tip</strong>
<small>Sinhala &amp; English</small>
</div>
<div className="workflow-step">
<span className="icon">📈</span>
<strong>Progress</strong>
<small>Metric tracking</small>
</div>
</div>
</article>
<article className="card activity-card">
<h3>Recent Research Logs</h3>
<div className="activity-list">
<div className="activity-item">
<span className="activity-icon">📷</span>
<div>
<strong>Recognition session logged</strong>
<span>Temporal sign sequence validated</span>
</div>
<time>10:24 AM</time>
</div>
<div className="activity-item">
<span className="activity-icon">文</span>
<div>
<strong>Bilingual translation test</strong>
<span>Sinhala and English text synthesized</span>
</div>
<time>10:18 AM</time>
</div>
<div className="activity-item">
<span className="activity-icon">🎓</span>
<div>
<strong>Motion error analysis run</strong>
<span>Hand position correction generated</span>
</div>
<time>10:05 AM</time>
</div>
<div className="activity-item">
<span className="activity-icon">💬</span>
<div>
<strong>Bidirectional conversation test</strong>
<span>End-to-end communication verified</span>
</div>
<time>09:50 AM</time>
</div>
</div>
</article>
</section>
</main>
</div>


</>);
}
