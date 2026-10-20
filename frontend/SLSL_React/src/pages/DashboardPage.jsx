import React from "react";
import { UserNav, ResearchSidebar } from "../components/Navigation";

export default function DashboardPage() {
  
  return (<>

<UserNav />
<main className="user-main">
<section className="user-page-header">
<div>
<h1>Dashboard</h1>
<p>Your SLSL communication and learning home.</p>
</div>
</section>

<section className="dashboard-hero">
<div className="dashboard-hero-copy">
<span className="welcome-pill">👋 Welcome back, Kamani</span>
<h2>Communicate &amp; Learn with SLSL</h2>
<p>Recognize signs via camera, converse in real-time with hearing users through bilingual captions and voice, and practice SLSL with corrective AI guidance.</p>
<div className="hero-actions">
<a className="hero-primary" href="/communication">💬 Start Communication</a>
<a className="hero-secondary" href="/recognition">📷 Open Recognition</a>
</div>
</div>
<div className="hero-art" aria-hidden="true">
<span>🤟</span>
<span>💬</span>
</div>
</section>

<section className="section">
<div className="section-title-row">
<div>
<h2>Quick Actions</h2>
<p>Choose an activity to start.</p>
</div>
</div>
<div className="action-grid">
<a className="action-card action-rec" href="/recognition">
<div className="action-card-head">
<span className="action-icon">📷</span>
</div>
<div className="action-card-body">
<h3>SLSL Recognition</h3>
<p>Recognize Sri Lankan Sign Language gestures in real-time using camera tracking.</p>
<b>Open Recognition →</b>
</div>
</a>
<a className="action-card action-comm" href="/communication">
<div className="action-card-head">
<span className="action-icon">💬</span>
</div>
<div className="action-card-body">
<h3>Live Communication</h3>
<p>Two-way Deaf ↔ hearing conversations with text captions, voice, and SLSL.</p>
<b>Start Conversation →</b>
</div>
</a>
<a className="action-card action-learn" href="/learn">
<div className="action-card-head">
<span className="action-icon">🎓</span>
</div>
<div className="action-card-body">
<h3>Learn SLSL</h3>
<p>Practice signs and receive friendly feedback on hand shape, position, and movement.</p>
<b>Start Practice →</b>
</div>
</a>
<a className="action-card action-lib" href="/library">
<div className="action-card-head">
<span className="action-icon">☝</span>
</div>
<div className="action-card-body">
<h3>Sign Library</h3>
<p>Explore Sri Lankan Sign Language vocabulary and reference demonstrations.</p>
<b>Browse Signs →</b>
</div>
</a>
</div>
</section>

<section className="section">
<div className="section-title-row">
<div>
<h2>Your Activity Summary</h2>
<p>Your SLSL learning and conversation overview.</p>
</div>
<a className="text-link" href="/history">View History →</a>
</div>
<div className="stat-grid">
<article className="card stat-card stat-teal">
<span className="stat-icon">📷</span>
<div>
<span>Recognition Sessions</span>
<strong>12</strong>
<small>Completed practices</small>
</div>
</article>
<article className="card stat-card stat-amber">
<span className="stat-icon">🎓</span>
<div>
<span>Practice Sessions</span>
<strong>8</strong>
<small>Guided reviews</small>
</div>
</article>
<article className="card stat-card stat-purple">
<span className="stat-icon">💬</span>
<div>
<span>Conversations</span>
<strong>5</strong>
<small>Live dialogues</small>
</div>
</article>
<article className="card stat-card stat-blue">
<span className="stat-icon">☝</span>
<div>
<span>Available Signs</span>
<strong>100+</strong>
<small>Vocabulary library</small>
</div>
</article>
</div>
</section>

<section className="section dashboard-lower">
<article className="card padded-card">
<div className="section-title-row">
<div>
<h2>Recent Activity</h2>
</div>
<a className="text-link" href="/history">View all</a>
</div>
<div className="mini-list">
<div className="mini-list-item">
<span className="mini-list-icon">📷</span>
<div>
<strong>Recognition session completed</strong>
<span>Today · 10:24 AM</span>
</div>
</div>
<div className="mini-list-item">
<span className="mini-list-icon">💬</span>
<div>
<strong>Live communication session</strong>
<span>Today · 10:05 AM</span>
</div>
</div>
<div className="mini-list-item">
<span className="mini-list-icon">🎓</span>
<div>
<strong>SLSL practice: AYUBOWAN</strong>
<span>Yesterday · 4:30 PM</span>
</div>
</div>
</div>
</article>
<article className="card padded-card">
<div className="section-title-row">
<div>
<h2>Learning Progress</h2>
</div>
<a className="text-link" href="/progress">Open Progress →</a>
</div>
<p className="muted" style={{fontSize: "13px", margin: "0 0 6px"}}>Overall curriculum completion</p>
<div className="progress-track">
<div style={{width: "68%"}}></div>
</div>
<div className="progress-mini">
<div>
<strong>7</strong>
<span>Day Streak</span>
</div>
<div>
<strong>12</strong>
<span>Badges</span>
</div>
<div>
<strong>5h</strong>
<span>Practice Time</span>
</div>
</div>
</article>
</section>
</main>


</>);
}
