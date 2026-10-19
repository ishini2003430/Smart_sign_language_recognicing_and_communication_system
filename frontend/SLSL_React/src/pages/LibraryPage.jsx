import React from "react";
import { UserNav, ResearchSidebar } from "../components/Navigation";

export default function LibraryPage() {
  
  return (<>

<UserNav />
<main className="user-main">
<section className="hud-page-head">
<div>
<div className="hud-kicker">Text / Speech to SLSL</div>
<h1>SLSL Sign Animation</h1>
<p>Generate Sri Lankan Sign Language animation from text or speech using appropriate signs.</p>
</div>
<div className="page-actions">
<span className="hud-system-chip"><i></i> Animation Ready</span>
</div>
</section>

<section className="slsl-gen-shell">

<div className="slsl-gen-col">
<article className="card input-panel">
<div className="hud-titlebar" style={{marginBottom: "14px"}}>
<div>
<div className="hud-label">Message Input</div>
<h2>Text / Speech Input</h2>
</div>
</div>

<label className="field" style={{marginBottom: "10px"}}>
          Input Language
          <select id="genLangSelect" className="select-input" style={{border: "1px solid var(--line)", borderRadius: "8px", padding: "6px 10px", background: "var(--surface-secondary)"}}>
<option value="en">English</option>
<option value="si">Sinhala (සිංහල)</option>
</select>
</label>

<label className="field" style={{marginBottom: "10px"}}>
          Message
          <textarea id="genInput" rows="3" style={{width: "100%", padding: "10px", border: "1px solid var(--line)", borderRadius: "8px", resize: "vertical", fontSize: "14px", fontFamily: "inherit", background: "var(--surface-secondary)", color: "var(--ink)", outline: "none"}} placeholder="Type your message to generate SLSL...">How are you today?</textarea>
</label>

<div style={{display: "flex", gap: "8px", marginBottom: "14px"}}>
<button id="genSpeakBtn" className="secondary-btn" style={{flexShrink: "0"}} title="Speak via microphone">🎤 Speak</button>
<button id="genSLSLBtn" className="primary-btn" style={{flex: "1", fontWeight: "700"}}>Generate SLSL →</button>
</div>

<div>
<span style={{fontSize: "11px", fontWeight: "700", color: "var(--text-secondary)", textTransform: "uppercase", letterSpacing: "0.05em"}}>Quick Phrases</span>
<div className="quick-phrases">
<button className="phrase-chip" data-phrase="Hello">Hello</button>
<button className="phrase-chip" data-phrase="Thank You">Thank You</button>
<button className="phrase-chip" data-phrase="How are you?">How are you?</button>
<button className="phrase-chip" data-phrase="Nice to meet you">Nice to meet you</button>
<button className="phrase-chip" data-phrase="I don't understand">I don't understand</button>
<button className="phrase-chip" data-phrase="Please wait">Please wait</button>
</div>
</div>
</article>

<article className="card" style={{padding: "14px"}}>
<div className="hud-titlebar" style={{marginBottom: "8px"}}>
<div>
<div className="hud-label">Preparing SLSL</div>
<h2>Sign Selection</h2>
</div>
</div>
<div className="piyasiri-stage-list" id="genStages">
<div className="piyasiri-stage" id="gs1">
<span className="piyasiri-stage-icon">1</span> Understanding message...
          </div>
<div className="piyasiri-stage" id="gs2">
<span className="piyasiri-stage-icon">2</span> Selecting appropriate signs...
          </div>
<div className="piyasiri-stage" id="gs3">
<span className="piyasiri-stage-icon">3</span> Generating SLSL sequence...
          </div>
<div className="piyasiri-stage" id="gs4">
<span className="piyasiri-stage-icon">4</span> Preparing animation...
          </div>
</div>
</article>
</div>

<div className="slsl-gen-col">
<article className="card slsl-gen-player-card">
<div className="hud-titlebar" style={{marginBottom: "12px"}}>
<div>
<div className="hud-label">Generated Signer</div>
<h2>SLSL Avatar Output</h2>
</div>
<span id="genPlayerState" className="small-badge">Ready</span>
</div>

<div className="context-status-pills" id="genContextPills" style={{display: "none"}}>
<span className="context-pill understood">✓ Message understood</span>
<span className="context-pill selected">✓ Appropriate signs selected</span>
</div>

<div className="slsl-video-player" style={{position: "relative"}}>
<svg viewBox="0 0 400 260" style={{width: "100%", display: "block"}} aria-label="SLSL animation signer output">
<defs>
<linearGradient id="libBodyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
<stop offset="0%" stopColor="#5B4DCE"></stop>
<stop offset="100%" stopColor="#3B30A8"></stop>
</linearGradient>
<linearGradient id="libSkinGrad" x1="0%" y1="0%" x2="0%" y2="100%">
<stop offset="0%" stopColor="#A0B4CC"></stop>
<stop offset="100%" stopColor="#7090A8"></stop>
</linearGradient>
<radialGradient id="libBg" cx="50%" cy="40%">
<stop offset="0%" stopColor="#28304A"></stop>
<stop offset="100%" stopColor="#141726"></stop>
</radialGradient>
</defs>

<rect width="400" height="260" fill="url(#libBg)"></rect>

<path d="M120,260 C126,208 148,178 190,162 L210,162 C252,178 274,208 280,260 Z" fill="url(#libBodyGrad)"></path>

<rect x="192" y="138" width="26" height="28" rx="5" fill="url(#libSkinGrad)"></rect>

<ellipse cx="205" cy="104" rx="34" ry="44" fill="url(#libSkinGrad)"></ellipse>

<path d="M177,90 C179,65 231,65 233,90 C218,80 192,80 177,90 Z" fill="#141726" opacity="0.7"></path>

<path d="M138,198 C114,210 100,185 122,148 L148,108" stroke="#3B30A8" strokeWidth="22" strokeLinecap="round"></path>
<path d="M138,198 C114,210 100,185 122,148 L148,108" stroke="url(#libSkinGrad)" strokeWidth="14" strokeLinecap="round"></path>

<path d="M268,198 C292,210 306,185 284,148 L258,108" stroke="#3B30A8" strokeWidth="22" strokeLinecap="round"></path>
<path d="M268,198 C292,210 306,185 284,148 L258,108" stroke="url(#libSkinGrad)" strokeWidth="14" strokeLinecap="round"></path>

<line x1="155" y1="195" x2="255" y2="195" stroke="#14AFA3" strokeWidth="1.5" strokeOpacity="0.45" strokeDasharray="4 3"></line>
<circle cx="155" cy="195" r="3" fill="#14AFA3" stroke="#FFFFFF" strokeWidth="1"></circle>
<circle cx="255" cy="195" r="3" fill="#14AFA3" stroke="#FFFFFF" strokeWidth="1"></circle>

<circle cx="148" cy="108" r="4" fill="#14AFA3" stroke="#FFFFFF" strokeWidth="1.5"></circle>
<polyline points="148,108 138,92 132,76 128,62" stroke="#14AFA3" strokeWidth="2" fill="none" strokeLinecap="round"></polyline>
<polyline points="148,108 144,88 140,72 138,58" stroke="#14AFA3" strokeWidth="2" fill="none" strokeLinecap="round"></polyline>
<polyline points="148,108 154,86 154,68 154,54" stroke="#14AFA3" strokeWidth="2" fill="none" strokeLinecap="round"></polyline>
<circle cx="128" cy="62" r="3" fill="#2DD4BF" stroke="#FFFFFF" strokeWidth="1"></circle>
<circle cx="138" cy="58" r="3" fill="#2DD4BF" stroke="#FFFFFF" strokeWidth="1"></circle>
<circle cx="154" cy="54" r="3" fill="#2DD4BF" stroke="#FFFFFF" strokeWidth="1"></circle>

<circle cx="258" cy="108" r="4" fill="#14AFA3" stroke="#FFFFFF" strokeWidth="1.5"></circle>
<polyline points="258,108 268,92 274,76 278,62" stroke="#14AFA3" strokeWidth="2" fill="none" strokeLinecap="round"></polyline>
<polyline points="258,108 262,88 266,72 268,58" stroke="#14AFA3" strokeWidth="2" fill="none" strokeLinecap="round"></polyline>
<polyline points="258,108 252,86 252,68 252,54" stroke="#14AFA3" strokeWidth="2" fill="none" strokeLinecap="round"></polyline>
<circle cx="278" cy="62" r="3" fill="#2DD4BF" stroke="#FFFFFF" strokeWidth="1"></circle>
<circle cx="268" cy="58" r="3" fill="#2DD4BF" stroke="#FFFFFF" strokeWidth="1"></circle>
<circle cx="252" cy="54" r="3" fill="#2DD4BF" stroke="#FFFFFF" strokeWidth="1"></circle>

<path d="M145,55 Q205,36 265,55" stroke="#14AFA3" strokeWidth="2" strokeDasharray="5 3" fill="none" strokeLinecap="round"></path>
</svg>

<div className="slsl-player-overlay-top">
<span className="player-sign-label" id="genSignLabel">HOW → ARE → YOU → TODAY</span>
<span className="player-live-dot"><i></i> PLAYING</span>
</div>
</div>

<div className="slsl-player-controls">
<div className="player-progress-row">
<span className="player-time-label">0:00</span>
<div className="player-timeline">
<div className="player-timeline-fill" id="genTimelineFill" style={{width: "0%"}}></div>
</div>
<span className="player-time-label">0:08</span>
</div>
<div className="player-btn-row">
<button className="player-ctrl-btn" title="Replay">↩</button>
<button className="player-ctrl-btn play-main" id="genPlayBtn" title="Play/Pause">▶</button>
<button className="player-ctrl-btn" title="Skip">⏭</button>
<select className="player-speed-select">
<option>0.5×</option>
<option selected={true}>1×</option>
<option>1.5×</option>
</select>
<button className="player-ctrl-btn" style={{marginLeft: "auto"}} title="Fullscreen">⛶</button>
</div>
</div>

<div id="genGlossSeq" className="slsl-sequence" style={{marginTop: "10px"}}>
<span>HOW</span><span>ARE</span><span>YOU</span><span>TODAY</span>
</div>
<p style={{margin: "6px 0 0", fontSize: "12px", color: "var(--text-secondary)"}}>
          Generated from context-appropriate stored SLSL signs · <span style={{color: "var(--green)"}}>✓ SLSL animation ready</span>
</p>
</article>
</div>

<div className="slsl-gen-col">
<article className="card" style={{padding: "16px"}}>
<div className="hud-titlebar" style={{marginBottom: "12px"}}>
<div>
<div className="hud-label">Session History</div>
<h2>Recent Outputs</h2>
</div>
</div>
<div className="slsl-history-list" id="genHistory">
<div className="slsl-history-item">
<div className="hi-input"><strong>How are you today?</strong> <span>English</span></div>
<div className="hi-seq"><span>HOW</span><span>ARE</span><span>YOU</span><span>TODAY</span></div>
<div className="hi-actions">
<small style={{color: "var(--green)", fontSize: "11px"}}>✓ Ready</small>
<button className="play-history-btn">▶ Play</button>
</div>
</div>
<div className="slsl-history-item">
<div className="hi-input"><strong>What is your name?</strong> <span>English</span></div>
<div className="hi-seq"><span>WHAT</span><span>NAME</span><span>YOU</span></div>
<div className="hi-actions">
<small style={{color: "var(--green)", fontSize: "11px"}}>✓ Ready</small>
<button className="play-history-btn">▶ Play</button>
</div>
</div>
<div className="slsl-history-item">
<div className="hi-input"><strong>Please wait here.</strong> <span>English</span></div>
<div className="hi-seq"><span>PLEASE</span><span>WAIT_B</span><span>HERE</span></div>
<div className="hi-actions">
<small style={{color: "var(--green)", fontSize: "11px"}}>✓ Ready</small>
<button className="play-history-btn">▶ Play</button>
</div>
</div>
</div>
</article>

<article className="card" style={{padding: "14px"}}>
<div className="hud-titlebar" style={{marginBottom: "10px"}}>
<div>
<div className="hud-label">Sign Vocabulary</div>
<h2>Available Signs</h2>
</div>
<span className="small-badge">100+</span>
</div>

<input id="signSearch" className="search-input" placeholder="Search sign vocabulary..." style={{width: "100%", marginBottom: "10px"}} />
<div id="signGrid" style={{display: "grid", gridTemplateColumns: "1fr 1fr", gap: "6px", maxHeight: "240px", overflowY: "auto"}}>
<div className="sign-card" data-name="ayubowan greeting" style={{padding: "8px", textAlign: "center", border: "1px solid var(--line)", borderRadius: "8px"}}>
<div style={{fontSize: "20px"}}>🤟</div>
<strong style={{fontSize: "11px", display: "block"}}>AYUBOWAN</strong>
</div>
<div className="sign-card" data-name="thank you common" style={{padding: "8px", textAlign: "center", border: "1px solid var(--line)", borderRadius: "8px"}}>
<div style={{fontSize: "20px"}}>🙏</div>
<strong style={{fontSize: "11px", display: "block"}}>THANK YOU</strong>
</div>
<div className="sign-card" data-name="help communication" style={{padding: "8px", textAlign: "center", border: "1px solid var(--line)", borderRadius: "8px"}}>
<div style={{fontSize: "20px"}}>🫶</div>
<strong style={{fontSize: "11px", display: "block"}}>HELP</strong>
</div>
<div className="sign-card" data-name="hospital place" style={{padding: "8px", textAlign: "center", border: "1px solid var(--line)", borderRadius: "8px"}}>
<div style={{fontSize: "20px"}}>🏥</div>
<strong style={{fontSize: "11px", display: "block"}}>HOSPITAL</strong>
</div>
<div className="sign-card" data-name="go action" style={{padding: "8px", textAlign: "center", border: "1px solid var(--line)", borderRadius: "8px"}}>
<div style={{fontSize: "20px"}}>👉</div>
<strong style={{fontSize: "11px", display: "block"}}>GO</strong>
</div>
<div className="sign-card" data-name="tomorrow time" style={{padding: "8px", textAlign: "center", border: "1px solid var(--line)", borderRadius: "8px"}}>
<div style={{fontSize: "20px"}}>📅</div>
<strong style={{fontSize: "11px", display: "block"}}>TOMORROW</strong>
</div>
<div className="sign-card" data-name="wait instruction" style={{padding: "8px", textAlign: "center", border: "1px solid var(--line)", borderRadius: "8px"}}>
<div style={{fontSize: "20px"}}>✋</div>
<strong style={{fontSize: "11px", display: "block"}}>WAIT</strong>
</div>
<div className="sign-card" data-name="what question" style={{padding: "8px", textAlign: "center", border: "1px solid var(--line)", borderRadius: "8px"}}>
<div style={{fontSize: "20px"}}>❓</div>
<strong style={{fontSize: "11px", display: "block"}}>WHAT</strong>
</div>
</div>
<button id="clearSearch" className="secondary-btn" style={{marginTop: "8px", fontSize: "12px"}}>Clear Search</button>
</article>
</div>
</section>
</main>



</>);
}
