import React from "react";
import { UserNav, ResearchSidebar } from "../components/Navigation";
import { RecognitionProvider, RecognitionControls, RecognitionPreview, RecognitionResults } from "../components/Recognition";

export default function RecognitionPage() {
  
  return (<>
<RecognitionProvider>
<UserNav />
<main className="user-main">
<section className="hud-page-head">
<div>
<div className="hud-kicker">SLSL Video Recognition</div>
<h1>SLSL Recognition</h1>
<p>Upload a recorded SLSL sign and run your trained recognition model when the backend is available.</p>
</div>
<div className="page-actions">
<span className="hud-system-chip"><i></i> Prototype — Backend Pending</span>
<a className="secondary-btn" href="/communication">💬 Open Live Communication</a>
</div>
</section>

<section className="hud-recognition-grid">

<article className="card hud-camera-card">
<div className="hud-titlebar">
<div>
<div className="hud-label">Recording</div>
<h2>Video Preview</h2>
</div>
<span id="recognitionCameraState" className="state-badge">UPLOAD MODE</span>
</div>

<div className="hud-camera" aria-label="Live SLSL camera tracking feed">
<RecognitionPreview />
<div className="hud-camera-meta">
<span className="live">● UPLOADED VIDEO PREVIEW</span>
<span>NO LIVE TRACKING</span>
</div>
<div className="hud-camera-footer">
<div className="hud-statusline">
<span className="pulse"></span>
<b>PREVIEW ONLY</b>
<span>Upper body &amp; hands</span>
</div>
</div>
</div>

<RecognitionControls />

<div className="camera-status-pills">
<span className="camera-status-pill"><i>•</i> Hands</span>
<span className="camera-status-pill"><i>•</i> Tracking</span>
<span className="camera-status-pill"><i>✓</i> Lighting</span>
<span className="camera-status-pill"><i>✓</i> Camera</span>
</div>
</article>

<RecognitionResults />
</section>

<div style={{marginTop: "14px", display: "flex", alignItems: "center", justifyContent: "space-between", padding: "12px 16px", border: "1px solid var(--line)", borderRadius: "12px", background: "var(--card)"}}>
<div>
<strong style={{fontSize: "13px", color: "var(--ink)"}}>Ready to communicate?</strong>
<span style={{fontSize: "12px", color: "var(--text-secondary)", marginLeft: "8px"}}>Use the conversation workspace for full Deaf ↔ Hearing two-way communication.</span>
</div>
<a className="secondary-btn" href="/communication" style={{whiteSpace: "nowrap"}}>Open Communication →</a>
</div>
</main>


</RecognitionProvider>
</>);
}
