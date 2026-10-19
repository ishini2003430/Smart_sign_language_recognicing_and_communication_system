import React from "react";
import { UserNav, ResearchSidebar } from "../components/Navigation";

export default function LearnPage() {
  
  return (<>

<UserNav />
<main className="user-main">

<div className="learn-top-bar">
<div className="learn-tabs">
<button type="button" className="learn-tab-btn active">Practice &amp; Analysis</button>
<a href="/progress" className="learn-tab-btn">My Progress</a>
<button type="button" className="learn-tab-btn">Leaderboard</button>
</div>

<div className="compact-sign-selector">
<label htmlFor="selectedSignSelect">Target Sign:</label>
<select id="selectedSignSelect" aria-label="Select Sign">
<option value="AYUBOWAN" data-emoji="🤟">AYUBOWAN (Greeting)</option>
<option value="THANK YOU" data-emoji="🙏">THANK YOU (Common Phrase)</option>
<option value="HELP" data-emoji="🫶">HELP (Communication)</option>
<option value="HOSPITAL" data-emoji="🏥">HOSPITAL (Place)</option>
<option value="GO" data-emoji="👉">GO (Action)</option>
</select>
<span id="selectedSignBadge" className="hidden">AYUBOWAN</span>
<span id="referenceEmoji" className="hidden">🤟</span>
</div>
</div>

<section className="hud-page-head" style={{marginBottom: "14px"}}>
<div>
<div className="hud-kicker">SLSL Sign Practice</div>
<h1>Practice &amp; Feedback</h1>
<p>Compare your signing against the expert reference for helpful guidance on hand shape, position, and movement.</p>
</div>
<div className="page-actions">
<span className="hud-system-chip"><i></i> Ready to Analyze</span>
</div>
</section>

<section className="learn-analysis-grid">

<article className="card learn-col-card">
<div className="hud-titlebar">
<div>
<div className="hud-label">Expert Reference</div>
<h2 id="referenceName">AYUBOWAN</h2>
</div>
<span className="small-badge good">Reference</span>
</div>

<div className="hud-video" aria-label="Expert reference demonstration">
<svg className="realistic-signer-mockup" viewBox="0 0 380 280" preserveAspectRatio="xMidYMid meet">
<defs>
<linearGradient id="expBodyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
<stop offset="0%" stopColor="#4A5578"></stop>
<stop offset="100%" stopColor="#283048"></stop>
</linearGradient>
<linearGradient id="expSkinGrad" x1="0%" y1="0%" x2="0%" y2="100%">
<stop offset="0%" stopColor="#8898B6"></stop>
<stop offset="100%" stopColor="#60708E"></stop>
</linearGradient>
</defs>

<path d="M100,280 C105,230 125,200 160,185 L220,185 C255,200 275,230 280,280 Z" fill="url(#expBodyGrad)"></path>
<rect x="175" y="150" width="30" height="38" rx="6" fill="url(#expSkinGrad)"></rect>
<ellipse cx="190" cy="112" rx="34" ry="44" fill="url(#expSkinGrad)"></ellipse>
<path d="M164,98 C167,74 213,74 216,98 C204,88 176,88 164,98 Z" fill="#283048" opacity="0.6"></path>

<path d="M260,215 C280,230 290,200 270,160 L250,118" stroke="#4A5578" strokeWidth="22" strokeLinecap="round"></path>
<path d="M260,215 C280,230 290,200 270,160 L250,118" stroke="url(#expSkinGrad)" strokeWidth="14" strokeLinecap="round"></path>

<rect x="215" y="38" width="95" height="110" rx="6" fill="none" stroke="#2DAA72" strokeWidth="1.5" strokeDasharray="3 2"></rect>

<circle cx="250" cy="118" r="3.5" fill="#2DAA72" stroke="#FFFFFF" strokeWidth="1"></circle>
<polyline points="250,118 238,102 230,88 226,76" stroke="#2DAA72" strokeWidth="2" strokeLinecap="round" fill="none"></polyline>
<polyline points="250,118 246,84 242,66 238,50" stroke="#2DAA72" strokeWidth="2" strokeLinecap="round" fill="none"></polyline>
<polyline points="250,118 258,82 260,62 262,48" stroke="#2DAA72" strokeWidth="2" strokeLinecap="round" fill="none"></polyline>
<polyline points="250,118 272,88 276,72 278,60" stroke="#2DAA72" strokeWidth="2" strokeLinecap="round" fill="none"></polyline>
<polyline points="250,118 284,98 290,86 294,76" stroke="#2DAA72" strokeWidth="2" strokeLinecap="round" fill="none"></polyline>
</svg>
<div className="hud-video-footer">
<span>TARGET REFERENCE</span>
<span>00:02 / 00:06</span>
</div>
</div>
<div style={{marginTop: "12px"}}>
<strong style={{fontSize: "12.5px", color: "var(--ink)", display: "block"}}>Standard Demonstration</strong>
<p className="muted" style={{margin: "2px 0 0", fontSize: "12px", lineHeight: "1.4"}}>
          Watch the expert gesture demonstration to practice your hand positioning and rhythm.
        </p>
</div>
</article>

<article className="card learn-col-card">
<div className="hud-titlebar">
<div>
<div className="hud-label">Your Practice</div>
<h2>Live Practice Camera</h2>
</div>
<span id="learnerState" className="state-badge">CAMERA READY</span>
</div>

<div className="hud-video" aria-label="Learner live practice camera">
<svg className="realistic-signer-mockup" viewBox="0 0 380 280" preserveAspectRatio="xMidYMid meet">

<path d="M100,280 C105,230 125,200 160,185 L220,185 C255,200 275,230 280,280 Z" fill="#384260"></path>
<rect x="175" y="150" width="30" height="38" rx="6" fill="#6B7C9C"></rect>
<ellipse cx="190" cy="112" rx="34" ry="44" fill="#6B7C9C"></ellipse>

<path d="M260,215 C275,230 285,200 265,165 L245,128" stroke="#384260" strokeWidth="22" strokeLinecap="round"></path>
<path d="M260,215 C275,230 285,200 265,165 L245,128" stroke="#6B7C9C" strokeWidth="14" strokeLinecap="round"></path>

<rect x="210" y="44" width="100" height="114" rx="6" fill="rgba(32, 175, 164, 0.06)" stroke="#20AFA4" strokeWidth="1.5" strokeDasharray="4 2"></rect>

<g>
<line x1="245" y1="128" x2="232" y2="112" stroke="#20AFA4" strokeWidth="2"></line>
<line x1="245" y1="128" x2="240" y2="92" stroke="#20AFA4" strokeWidth="2"></line>
<line x1="245" y1="128" x2="252" y2="90" stroke="#20AFA4" strokeWidth="2"></line>
<line x1="245" y1="128" x2="266" y2="95" stroke="#20AFA4" strokeWidth="2"></line>
<line x1="245" y1="128" x2="278" y2="108" stroke="#20AFA4" strokeWidth="2"></line>
<polyline points="245,128 232,112 224,100 218,88 214,78" stroke="#20AFA4" strokeWidth="2" fill="none"></polyline>
<polyline points="245,128 240,92 238,72 236,56 234,44" stroke="#20AFA4" strokeWidth="2" fill="none"></polyline>
<polyline points="245,128 252,90 254,70 255,54 256,42" stroke="#20AFA4" strokeWidth="2" fill="none"></polyline>
<polyline points="245,128 266,95 268,76 270,62 272,50" stroke="#20AFA4" strokeWidth="2" fill="none"></polyline>
<polyline points="245,128 278,108 284,94 288,82 292,72" stroke="#20AFA4" strokeWidth="2" fill="none"></polyline>

<circle cx="245" cy="128" r="3.5" fill="#20AFA4" stroke="#FFFFFF" strokeWidth="1.5"></circle>
<circle cx="214" cy="78" r="3" fill="#2DD4BF" stroke="#FFFFFF" strokeWidth="1"></circle>
<circle cx="234" cy="44" r="3" fill="#2DD4BF" stroke="#FFFFFF" strokeWidth="1"></circle>
<circle cx="256" cy="42" r="3" fill="#2DD4BF" stroke="#FFFFFF" strokeWidth="1"></circle>
<circle cx="272" cy="50" r="3" fill="#2DD4BF" stroke="#FFFFFF" strokeWidth="1"></circle>
<circle cx="292" cy="72" r="3" fill="#2DD4BF" stroke="#FFFFFF" strokeWidth="1"></circle>
</g>
</svg>
<div className="hud-video-footer">
<span>MOTION TRACKING ACTIVE</span>
<span>LIVE CAMERA</span>
</div>
</div>

<div className="camera-status-pills">
<span className="camera-status-pill"><i>✓</i> Hands</span>
<span className="camera-status-pill"><i>✓</i> Tracking</span>
<span className="camera-status-pill"><i>✓</i> Lighting</span>
<span className="camera-status-pill"><i>✓</i> Position</span>
</div>
</article>

<article className="card learn-col-card">
<div className="hud-titlebar">
<div>
<div className="hud-label">Your Feedback</div>
<h2>Evaluation &amp; Guidance</h2>
</div>
<span className="small-badge good">Analyzed</span>
</div>

<div className="score-hero-box">
<div className="score-badge-circle">
<strong>78%</strong>
</div>
<div className="score-hero-copy">
<strong>Overall Accuracy Match</strong>
<span>Good form with a small position adjustment needed</span>
</div>
</div>

<div className="eval-breakdown-list">

<div className="eval-row">
<div className="eval-row-header">
<strong>1. Hand Shape</strong>
<span className="good">92% · Correct</span>
</div>
<div className="eval-bar"><i className="good" style={{width: "92%"}}></i></div>
<div className="eval-note">Your finger position looks good.</div>
</div>

<div className="eval-row">
<div className="eval-row-header">
<strong>2. Hand Position</strong>
<span className="warning">64% · Adjust</span>
</div>
<div className="eval-bar"><i className="warning" style={{width: "64%"}}></i></div>
<div className="eval-note">Raise your right hand slightly higher.</div>
</div>

<div className="eval-row">
<div className="eval-row-header">
<strong>3. Hand Movement</strong>
<span className="good">85% · Good</span>
</div>
<div className="eval-bar"><i className="good" style={{width: "85%"}}></i></div>
<div className="eval-note">Your movement direction is correct.</div>
</div>

<div className="eval-row">
<div className="eval-row-header">
<strong>4. Timing &amp; Hold</strong>
<span className="good">80% · Steady</span>
</div>
<div className="eval-bar"><i className="good" style={{width: "80%"}}></i></div>
<div className="eval-note">Steady rhythm and hold.</div>
</div>
</div>
</article>
</section>

<section className="learn-action-bar">
<div style={{display: "flex", alignItems: "center", gap: "10px"}}>
<button id="practiceBtn" className="primary-btn submit-analyze-btn">▶ Submit &amp; Analyze</button>
<button id="resetPractice" className="secondary-btn">↺ Reset Practice</button>
</div>
<a className="text-link" href="/error-analysis">View Detailed Feedback Logs →</a>
</section>

<section className="card learn-feedback-card">
<div className="section-title-row" style={{marginBottom: "6px"}}>
<div>
<h2>Personalized Coaching Feedback</h2>
<p>Helpful suggestions to improve your SLSL signing accuracy.</p>
</div>
</div>
<div className="feedback-bullet-grid">
<div className="feedback-bullet success">
<span className="feedback-bullet-icon">✓</span>
<div className="feedback-bullet-text">
<strong>Hand Shape Looks Great</strong>
<p>Your finger extension, thumb placement, and palm angle closely match the reference demonstration.</p>
</div>
</div>
<div className="feedback-bullet alert">
<span className="feedback-bullet-icon">⚠</span>
<div className="feedback-bullet-text">
<strong>Adjust Hand Elevation</strong>
<p>Raise your right hand slightly higher toward chest level before initiating the outward greeting motion.</p>
</div>
</div>
<div className="feedback-bullet success">
<span className="feedback-bullet-icon">✓</span>
<div className="feedback-bullet-text">
<strong>Movement Direction Correct</strong>
<p>The forward gesture stroke follows the proper motion path smoothly.</p>
</div>
</div>
<div className="feedback-bullet alert">
<span className="feedback-bullet-icon">⚠</span>
<div className="feedback-bullet-text">
<strong>Hold the Final Sign</strong>
<p>Hold your hand steady for an additional moment at the end to complete the sign cleanly.</p>
</div>
</div>
</div>
</section>
</main>



</>);
}
