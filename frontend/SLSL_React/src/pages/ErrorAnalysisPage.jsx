import React from "react";
import { UserNav, ResearchSidebar } from "../components/Navigation";

export default function ErrorAnalysisPage() {
  
  return (<>

<UserNav />
<main className="user-main">
<section className="user-page-header">
<div>
<h1>Practice Feedback</h1>
<p>Fine-grained motion evaluation for hand shape, spatial position, and movement trajectory.</p>
</div>
<a className="secondary-btn" href="/learn">← Back to Practice</a>
</section>

<section className="progress-hero-grid">
<article className="card progress-ring-card">
<div className="progress-ring" style={{background: "conic-gradient(var(--purple) 0 78%, #E4E7EC 78% 100%)"}}>
<strong>78%</strong>
</div>
<div>
<h2 style={{margin: "0", fontSize: "18px", fontWeight: "700"}}>Practice Motion Match</h2>
<p className="muted" style={{margin: "4px 0 10px", fontSize: "13px", lineHeight: "1.5"}}>
          Motion similarity score compared to expert demonstration.
        </p>
<span className="small-badge good">✓ High Match</span>
</div>
</article>
<article className="card padded-card">
<div className="section-title-row">
<div>
<h2>Motion Component Breakdown</h2>
<p>Targeted corrective analysis.</p>
</div>
</div>
<div className="hud-learning-metrics" style={{marginTop: "0"}}>
<div className="hud-metric-panel card" style={{padding: "10px"}}>
<div className="hud-titlebar" style={{marginBottom: "4px"}}>
<span className="hud-label">Hand Shape</span>
<span className="small-badge good">Good</span>
</div>
<strong style={{fontSize: "13px", color: "var(--green)"}}>Close to Expert</strong>
</div>
<div className="hud-metric-panel card" style={{padding: "10px"}}>
<div className="hud-titlebar" style={{marginBottom: "4px"}}>
<span className="hud-label">Position</span>
<span className="small-badge warning">Adjust</span>
</div>
<strong style={{fontSize: "13px", color: "var(--warning)"}}>Raise Hand 2cm</strong>
</div>
<div className="hud-metric-panel card" style={{padding: "10px"}}>
<div className="hud-titlebar" style={{marginBottom: "4px"}}>
<span className="hud-label">Movement</span>
<span className="small-badge good">Good</span>
</div>
<strong style={{fontSize: "13px", color: "var(--green)"}}>Smooth Finish</strong>
</div>
</div>
</article>
</section>

<section className="section card padded-card">
<div className="section-title-row">
<div>
<h2>Personalized Corrective Feedback</h2>
<p>Bilingual instructions for the learner.</p>
</div>
</div>
<div className="hud-translation-layout" style={{marginTop: "10px"}}>
<div className="result-language">
<span>English Feedback</span>
<p>Raise your right hand slightly closer to chest level and complete the final motion with a steady forward pause.</p>
</div>
<div className="result-language">
<span>Sinhala Feedback (සිංහල)</span>
<p>ඔබගේ දකුණු අත තරමක් පපුවේ මට්ටමට ඔසවා අවසාන චලනය ස්ථාවරව සම්පූර්ණ කරන්න.</p>
</div>
</div>
<div style={{display: "flex", gap: "10px", marginTop: "16px"}}>
<a className="secondary-btn" href="/learn">Try Again</a>
<a className="primary-btn" href="/progress">View Progress →</a>
</div>
</section>
</main>


</>);
}
