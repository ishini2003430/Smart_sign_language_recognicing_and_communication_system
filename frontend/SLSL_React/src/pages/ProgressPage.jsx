import React from "react";
import { UserNav, ResearchSidebar } from "../components/Navigation";

export default function ProgressPage() {
  
  return (<>

<UserNav />
<main className="user-main">
<section className="user-page-header">
<div>
<h1>My Learning Progress</h1>
<p>Track your SLSL sign accuracy, practice streaks, and mastery milestones.</p>
</div>
<a className="primary-btn" href="/learn">🎓 Continue Practice</a>
</section>

<section className="progress-hero-grid">
<article className="card progress-ring-card">
<div className="progress-ring">
<strong>68%</strong>
</div>
<div>
<h2 style={{margin: "0", fontSize: "18px", fontWeight: "700"}}>Overall Course Progress</h2>
<p className="muted" style={{margin: "4px 0 10px", fontSize: "13px", lineHeight: "1.5"}}>
          Based on 14 completed practice gestures and feedback reviews.
        </p>
<span className="small-badge good">🔥 7 Day Streak Active</span>
</div>
</article>
<article className="card padded-card">
<div className="section-title-row">
<div>
<h2>Weekly Practice Minutes</h2>
<p>Daily activity trend.</p>
</div>
</div>
<div className="bar-chart">
<div className="bar" style={{height: "45%"}}><span>Mon</span></div>
<div className="bar" style={{height: "70%"}}><span>Tue</span></div>
<div className="bar" style={{height: "55%"}}><span>Wed</span></div>
<div className="bar" style={{height: "82%"}}><span>Thu</span></div>
<div className="bar" style={{height: "63%"}}><span>Fri</span></div>
<div className="bar" style={{height: "90%"}}><span>Sat</span></div>
<div className="bar" style={{height: "74%"}}><span>Sun</span></div>
</div>
</article>
</section>

<section className="section stat-grid">
<article className="card stat-card stat-purple">
<span className="stat-icon">🎯</span>
<div>
<span>Completed Sessions</span>
<strong>18</strong>
<small>Total practices</small>
</div>
</article>
<article className="card stat-card stat-amber">
<span className="stat-icon">🏆</span>
<div>
<span>Earned Badges</span>
<strong>12</strong>
<small>Mastery achievements</small>
</div>
</article>
<article className="card stat-card stat-coral">
<span className="stat-icon">🔥</span>
<div>
<span>Current Streak</span>
<strong>7 Days</strong>
<small>Consistent learning</small>
</div>
</article>
<article className="card stat-card stat-teal">
<span className="stat-icon">⏱</span>
<div>
<span>Learning Time</span>
<strong>12 Hours</strong>
<small>Total logged</small>
</div>
</article>
</section>

<section className="section dashboard-lower">
<article className="card padded-card">
<div className="section-title-row">
<div>
<h2>Recent Practice Activity</h2>
</div>
</div>
<div className="mini-list">
<div className="mini-list-item">
<span className="mini-list-icon">🤟</span>
<div>
<strong>AYUBOWAN</strong>
<span>Hand Position Adjusted · Good Match</span>
</div>
</div>
<div className="mini-list-item">
<span className="mini-list-icon">🙏</span>
<div>
<strong>THANK YOU</strong>
<span>Completed with high accuracy</span>
</div>
</div>
<div className="mini-list-item">
<span className="mini-list-icon">👉</span>
<div>
<strong>GO</strong>
<span>Movement path verified</span>
</div>
</div>
</div>
</article>
<article className="card padded-card">
<div className="section-title-row">
<div>
<h2>Next Goal</h2>
</div>
</div>
<p className="muted" style={{margin: "0 0 12px", fontSize: "13px", lineHeight: "1.6"}}>
        Complete 3 more practice sessions this week to unlock the <strong>Conversational SLSL</strong> achievement badge.
      </p>
<div className="progress-track">
<div style={{width: "60%"}}></div>
</div>
<a className="primary-btn" style={{marginTop: "16px"}} href="/learn">Start Next Session →</a>
</article>
</section>
</main>


</>);
}
