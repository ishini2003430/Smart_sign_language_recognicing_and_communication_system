import React from "react";
import { UserNav, ResearchSidebar } from "../components/Navigation";

export default function CommunicationPage() {
  
  return (<>

<UserNav />
<main className="user-main communication-main">

<section className="hud-page-head">
<div>
<div className="hud-kicker">Live Communication Session</div>
<h1>Deaf ↔ Hearing Live Conversation</h1>
<p>Two-way communication with synchronized sign language recognition, translations, and SLSL reply animation.</p>
</div>
<div className="page-actions">
<span className="hud-system-chip"><i></i> Session Active</span>
<button id="enterFocus" className="secondary-btn enter-focus-btn">⛶ Focus Mode</button>
<button id="exitFocus" className="secondary-btn exit-focus-btn">← Exit Focus</button>
</div>
</section>

<section className="hud-comm-grid">

<article className="card hud-comm-left">
<div className="hud-titlebar">
<div>
<div className="hud-label">Deaf User</div>
<h2>Deaf User — Live Camera</h2>
</div>
<span id="cameraState" className="state-badge">READY</span>
</div>

<div className="hud-camera" aria-label="Live camera tracking feed">

<svg className="realistic-signer-mockup" viewBox="0 0 420 300" preserveAspectRatio="xMidYMid meet">
<defs>
<linearGradient id="bodyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
<stop offset="0%" stopColor="#3D4764"></stop>
<stop offset="100%" stopColor="#242B3E"></stop>
</linearGradient>
<linearGradient id="skinGrad" x1="0%" y1="0%" x2="0%" y2="100%">
<stop offset="0%" stopColor="#7B8CA8"></stop>
<stop offset="100%" stopColor="#55627C"></stop>
</linearGradient>
<linearGradient id="meshGlow" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stopColor="#18A999" stopOpacity="0.22"></stop>
<stop offset="100%" stopColor="#18A999" stopOpacity="0.02"></stop>
</linearGradient>
</defs>

<path d="M120,300 C125,245 145,210 180,195 L240,195 C275,210 295,245 300,300 Z" fill="url(#bodyGrad)"></path>

<rect x="195" y="160" width="30" height="38" rx="6" fill="url(#skinGrad)"></rect>

<ellipse cx="210" cy="120" rx="36" ry="46" fill="url(#skinGrad)"></ellipse>
<path d="M182,105 C185,80 235,80 238,105 C225,95 195,95 182,105 Z" fill="#242B3E" opacity="0.65"></path>

<path d="M135,225 C120,250 115,280 110,300" stroke="#3D4764" strokeWidth="26" strokeLinecap="round"></path>

<path d="M285,225 C305,240 315,210 295,170 L275,130" stroke="#3D4764" strokeWidth="24" strokeLinecap="round" strokeLinejoin="round"></path>
<path d="M285,225 C305,240 315,210 295,170 L275,130" stroke="url(#skinGrad)" strokeWidth="16" strokeLinecap="round" strokeLinejoin="round"></path>

<rect x="235" y="45" width="105" height="120" rx="8" fill="url(#meshGlow)" stroke="#18A999" strokeWidth="1.5" strokeDasharray="4 2"></rect>

<circle cx="210" cy="120" r="3" fill="#18A999" opacity="0.8"></circle>
<circle cx="160" cy="210" r="3.5" fill="#18A999" opacity="0.8"></circle>
<circle cx="260" cy="210" r="3.5" fill="#18A999" opacity="0.8"></circle>
<circle cx="305" cy="215" r="3.5" fill="#18A999" opacity="0.8"></circle>
<line x1="160" y1="210" x2="260" y2="210" stroke="#18A999" strokeWidth="1.5" strokeOpacity="0.6" strokeDasharray="3 3"></line>
<line x1="260" y1="210" x2="305" y2="215" stroke="#18A999" strokeWidth="1.5" strokeOpacity="0.6"></line>
<line x1="305" y1="215" x2="275" y2="135" stroke="#18A999" strokeWidth="1.5" strokeOpacity="0.8"></line>

<g id="handLandmarks">

<line x1="275" y1="135" x2="258" y2="118" stroke="#18A999" strokeWidth="2.2" strokeLinecap="round"></line>
<line x1="275" y1="135" x2="268" y2="98" stroke="#18A999" strokeWidth="2.2" strokeLinecap="round"></line>
<line x1="275" y1="135" x2="282" y2="95" stroke="#18A999" strokeWidth="2.2" strokeLinecap="round"></line>
<line x1="275" y1="135" x2="296" y2="100" stroke="#18A999" strokeWidth="2.2" strokeLinecap="round"></line>
<line x1="275" y1="135" x2="308" y2="112" stroke="#18A999" strokeWidth="2.2" strokeLinecap="round"></line>

<polyline points="275,135 258,118 248,106 242,95 238,84" stroke="#18A999" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"></polyline>

<polyline points="275,135 268,98 266,78 264,62 262,48" stroke="#18A999" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"></polyline>

<polyline points="275,135 282,95 284,74 285,58 286,45" stroke="#18A999" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"></polyline>

<polyline points="275,135 296,100 299,82 301,68 302,56" stroke="#18A999" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"></polyline>

<polyline points="275,135 308,112 314,98 318,86 322,76" stroke="#18A999" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"></polyline>

<circle cx="275" cy="135" r="4" fill="#18A999" stroke="#FFFFFF" strokeWidth="1.5"></circle>

<circle cx="258" cy="118" r="3" fill="#18A999" stroke="#FFFFFF" strokeWidth="1"></circle>
<circle cx="248" cy="106" r="3" fill="#18A999" stroke="#FFFFFF" strokeWidth="1"></circle>
<circle cx="242" cy="95" r="3" fill="#18A999" stroke="#FFFFFF" strokeWidth="1"></circle>
<circle cx="238" cy="84" r="3.5" fill="#2DD4BF" stroke="#FFFFFF" strokeWidth="1.5"></circle>

<circle cx="268" cy="98" r="3" fill="#18A999" stroke="#FFFFFF" strokeWidth="1"></circle>
<circle cx="266" cy="78" r="3" fill="#18A999" stroke="#FFFFFF" strokeWidth="1"></circle>
<circle cx="264" cy="62" r="3" fill="#18A999" stroke="#FFFFFF" strokeWidth="1"></circle>
<circle cx="262" cy="48" r="3.5" fill="#2DD4BF" stroke="#FFFFFF" strokeWidth="1.5"></circle>

<circle cx="282" cy="95" r="3" fill="#18A999" stroke="#FFFFFF" strokeWidth="1"></circle>
<circle cx="284" cy="74" r="3" fill="#18A999" stroke="#FFFFFF" strokeWidth="1"></circle>
<circle cx="285" cy="58" r="3" fill="#18A999" stroke="#FFFFFF" strokeWidth="1"></circle>
<circle cx="286" cy="45" r="3.5" fill="#2DD4BF" stroke="#FFFFFF" strokeWidth="1.5"></circle>

<circle cx="296" cy="100" r="3" fill="#18A999" stroke="#FFFFFF" strokeWidth="1"></circle>
<circle cx="299" cy="82" r="3" fill="#18A999" stroke="#FFFFFF" strokeWidth="1"></circle>
<circle cx="301" cy="68" r="3" fill="#18A999" stroke="#FFFFFF" strokeWidth="1"></circle>
<circle cx="302" cy="56" r="3.5" fill="#2DD4BF" stroke="#FFFFFF" strokeWidth="1.5"></circle>

<circle cx="308" cy="112" r="3" fill="#18A999" stroke="#FFFFFF" strokeWidth="1"></circle>
<circle cx="314" cy="98" r="3" fill="#18A999" stroke="#FFFFFF" strokeWidth="1"></circle>
<circle cx="318" cy="86" r="3" fill="#18A999" stroke="#FFFFFF" strokeWidth="1"></circle>
<circle cx="322" cy="76" r="3.5" fill="#2DD4BF" stroke="#FFFFFF" strokeWidth="1.5"></circle>
</g>
</svg>

<div className="hud-camera-meta">
<span className="live">● LIVE FEED</span>
<span>HAND TRACKING</span>
</div>

<div className="hud-camera-footer">
<div className="hud-statusline">
<span className="pulse"></span>
<b>TRACKING ACTIVE</b>
<span>21 Hand Points</span>
</div>
<div className="hud-statusline">
<span>Lighting:</span>
<b>Optimal</b>
</div>
</div>
</div>

<div className="camera-controls-bar">
<button id="startSigning" className="primary-btn"><span className="btn-icon">▶</span> Start Signing</button>
<button id="pauseSigning" className="secondary-btn" disabled={true}><span className="btn-icon">❚❚</span> Pause</button>
<button id="endSentence" className="success-btn" disabled={true}><span className="btn-icon">✓</span> End Sentence</button>
<button id="clearSigning" className="secondary-btn">Clear</button>
</div>

<div className="camera-status-pills">
<span className="camera-status-pill"><i>✓</i> Hands</span>
<span className="camera-status-pill"><i>✓</i> Tracking</span>
<span className="camera-status-pill"><i>✓</i> Lighting</span>
<span className="camera-status-pill"><i>✓</i> Camera</span>
</div>

<div className="live-sequence-area">
<div className="live-sequence-head">
<strong style={{fontSize: "12.5px", color: "var(--ink)"}}>Recognized Sequence</strong>
<span id="sequenceStatus" className="small-badge">Waiting</span>
</div>
<div id="liveSequence" className="sequence-box">
<p>Start signing to build the sequence.</p>
</div>
</div>
</article>

<article className="card hud-comm-right-workspace">

<div>
<div className="hud-titlebar" style={{marginBottom: "10px"}}>
<div>
<h2>Spoken &amp; Written Translation</h2>
</div>
<span id="translationStatus" className="small-badge">Waiting</span>
</div>
<div id="translationWaiting" className="translation-waiting">
<div>文</div>
<strong>Waiting for Deaf user's sentence</strong>
<p>Complete signing on the left to generate Sinhala &amp; English translations and voice.</p>
</div>
<div id="translationResult" className="hidden">
<div className="trans-block-sinhala" style={{marginBottom: "8px"}}>
<div className="trans-block-header">
<strong>Sinhala Translation (සිංහල)</strong>
<button id="playSinhala" className="play-btn">🔊 Play Sinhala</button>
</div>
<p id="sinhalaOutput" className="trans-block-text">මම හෙට රෝහලට යනවා.</p>
</div>
<div className="trans-block-english">
<div className="trans-block-header">
<strong>English Translation</strong>
<button id="playEnglish" className="play-btn">🔊 Play English</button>
</div>
<p id="englishOutput" className="trans-block-text">I will go to the hospital tomorrow.</p>
</div>
<div className="hud-wave" aria-label="Speech playback animation">
<i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i>
</div>
</div>
</div>

<div className="rec-section-divider">
<div className="hud-titlebar" style={{marginBottom: "8px"}}>
<div>
<h2>Reply to Deaf User</h2>
</div>
<span id="speechStatus" className="small-badge">MIC READY</span>
</div>
<div className="chat-composer-row">
<button id="speakReply" className="chat-mic-btn" title="Speak via microphone">🎤</button>
<input id="replyInput" className="chat-composer-input" defaultValue="What time will you go?" placeholder="Type your reply to the Deaf user..." />
<button id="sendReply" className="chat-send-btn">Send →</button>
</div>
</div>

<div className="rec-section-divider">
<div className="hud-titlebar" style={{marginBottom: "10px"}}>
<div>
<h2>Generated SLSL Reply</h2>
</div>
<span id="slslState" className="small-badge">Waiting</span>
</div>

<div id="slslWaiting">
<div className="friendly-status-card" id="slslFriendlyStatus">
<span>Send a reply above to generate the SLSL signing reply.</span>
</div>
<div style={{display: "none"}} id="piyasiriStages">
<div id="ps1"></div><div id="ps2"></div><div id="ps3"></div><div id="ps4"></div>
</div>
</div>

<div id="slslResult" className="hidden">

<div className="slsl-video-player" style={{position: "relative"}}>

<svg viewBox="0 0 340 190" style={{width: "100%", display: "block"}} aria-label="SLSL animation signer">
<defs>
<linearGradient id="pBodyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
<stop offset="0%" stopColor="#6C4DE6"></stop>
<stop offset="100%" stopColor="#4A34AC"></stop>
</linearGradient>
<linearGradient id="pSkinGrad" x1="0%" y1="0%" x2="0%" y2="100%">
<stop offset="0%" stopColor="#9DB0CC"></stop>
<stop offset="100%" stopColor="#6B80A0"></stop>
</linearGradient>
</defs>

<path d="M95,190 C100,154 118,134 150,122 L190,122 C222,134 240,154 245,190 Z" fill="url(#pBodyGrad)"></path>
<rect x="158" y="102" width="24" height="24" rx="5" fill="url(#pSkinGrad)"></rect>
<ellipse cx="170" cy="76" rx="28" ry="36" fill="url(#pSkinGrad)"></ellipse>

<path d="M220,148 C238,158 248,136 228,104 L208,72" stroke="#583CD4" strokeWidth="18" strokeLinecap="round"></path>
<path d="M220,148 C238,158 248,136 228,104 L208,72" stroke="url(#pSkinGrad)" strokeWidth="10" strokeLinecap="round"></path>
<path d="M120,148 C102,158 92,136 112,104 L132,72" stroke="#583CD4" strokeWidth="18" strokeLinecap="round"></path>
<path d="M120,148 C102,158 92,136 112,104 L132,72" stroke="url(#pSkinGrad)" strokeWidth="10" strokeLinecap="round"></path>

<path d="M130,68 Q170,52 210,68" stroke="#20AFA4" strokeWidth="2" strokeDasharray="4 3" fill="none"></path>

<circle cx="130" cy="68" r="4" fill="#20AFA4" stroke="#FFFFFF" strokeWidth="1.5"></circle>
<circle cx="210" cy="68" r="4" fill="#20AFA4" stroke="#FFFFFF" strokeWidth="1.5"></circle>
<circle cx="170" cy="52" r="3" fill="#2DD4BF" stroke="#FFFFFF" strokeWidth="1"></circle>
</svg>

<div className="slsl-player-overlay-top">
<span className="player-sign-label">WHAT · TIME · YOU · GO</span>
<span className="player-live-dot"><i></i> PLAYING</span>
</div>
</div>

<div className="slsl-player-controls">
<div className="player-progress-row">
<span className="player-time-label">0:02</span>
<div className="player-timeline" id="piyasiriTimeline">
<div className="player-timeline-fill" id="piyasiriTimelineFill" style={{width: "35%"}}></div>
</div>
<span className="player-time-label">0:06</span>
</div>
<div className="player-btn-row">
<button className="player-ctrl-btn" title="Replay">↩</button>
<button className="player-ctrl-btn play-main" id="piyasiriPlayBtn" title="Play/Pause">▶</button>
<button className="player-ctrl-btn" title="Skip forward">⏭</button>
<select className="player-speed-select" title="Playback speed">
<option>0.5×</option>
<option selected={true}>1×</option>
<option>1.5×</option>
</select>
<button className="player-ctrl-btn" style={{marginLeft: "auto"}} title="Fullscreen">⛶</button>
</div>
</div>

<div className="slsl-sequence" style={{marginTop: "10px"}}>
<span>WHAT</span><span>TIME</span><span>YOU</span><span>GO</span>
</div>
<p style={{margin: "6px 0 0", fontSize: "12px", color: "var(--text-secondary)"}}>
<span style={{color: "var(--green)"}}>✓ SLSL Reply Ready</span> · Appropriate signs selected for your reply
          </p>
</div>
</div>
</article>
</section>

<section className="hud-conversation-strip">
<div>
<span>Latest Conversation</span>
<strong id="latestConversation">No completed messages yet.</strong>
</div>
<a className="secondary-btn" href="/history">View History →</a>
</section>
</main>



</>);
}
