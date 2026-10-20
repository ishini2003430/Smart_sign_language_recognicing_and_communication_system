import React from "react";
import { UserNav, ResearchSidebar } from "../components/Navigation";

export default function HistoryPage() {
  
  return (<>

<UserNav />
<main className="user-main">
<section className="user-page-header">
<div>
<h1>Activity History</h1>
<p>Review past sign recognition, practice feedback, and live communication sessions.</p>
</div>
<button className="secondary-btn">Export History</button>
</section>

<section className="card filter-bar">
<input className="search-input" placeholder="Search activity logs..." />
<select className="select-input">
<option>All Modules</option>
<option>Recognition</option>
<option>Live Communication</option>
<option>Learn SLSL</option>
<option>Translation</option>
</select>
<select className="select-input">
<option>Recent First</option>
<option>Oldest First</option>
</select>
<button className="secondary-btn">Filter</button>
</section>

<section className="section activity-timeline">
<div className="timeline-item">
<div className="timeline-left">
<div className="timeline-icon-box rec">📷</div>
<div className="timeline-content">
<strong>Recognition Session</strong>
<span>Recognized sequence: I → TOMORROW → HOSPITAL → GO</span>
</div>
</div>
<div className="timeline-meta">
<span className="timeline-time">Today · 10:24 AM</span>
<span className="timeline-tag teal">Recognition</span>
</div>
</div>
<div className="timeline-item">
<div className="timeline-left">
<div className="timeline-icon-box comm">💬</div>
<div className="timeline-content">
<strong>Live Communication Session</strong>
<span>Deaf ↔ hearing two-way dialogue · 2 messages exchanged</span>
</div>
</div>
<div className="timeline-meta">
<span className="timeline-time">Today · 10:05 AM</span>
<span className="timeline-tag purple">Communication</span>
</div>
</div>
<div className="timeline-item">
<div className="timeline-left">
<div className="timeline-icon-box learn">🎓</div>
<div className="timeline-content">
<strong>Practice Session: AYUBOWAN</strong>
<span>78% Overall Match · Hand shape &amp; movement confirmed</span>
</div>
</div>
<div className="timeline-meta">
<span className="timeline-time">Yesterday · 4:30 PM</span>
<span className="timeline-tag orange">Learning</span>
</div>
</div>
<div className="timeline-item">
<div className="timeline-left">
<div className="timeline-icon-box trans">文</div>
<div className="timeline-content">
<strong>Bilingual Translation</strong>
<span>Natural sentence generated: "මම හෙට රෝහලට යනවා."</span>
</div>
</div>
<div className="timeline-meta">
<span className="timeline-time">Yesterday · 2:12 PM</span>
<span className="timeline-tag blue">Translation</span>
</div>
</div>
</section>
<section className="section card padded-card">
<div className="section-title-row">
<div>
<h2>About Your History</h2>
</div>
</div>
<p className="muted" style={{margin: "0", fontSize: "13px", lineHeight: "1.6"}}>
      Activity logs shown here are saved during your current session. In the connected version, all sessions will sync securely with your account.
    </p>
</section>
</main>


</>);
}
