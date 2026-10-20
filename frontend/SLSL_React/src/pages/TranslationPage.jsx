import React from "react";
import { UserNav, ResearchSidebar } from "../components/Navigation";

export default function TranslationPage() {
  
  return (<>

<UserNav />
<main className="user-main">
<section className="hud-page-head">
<div>
<div className="hud-kicker">SLSL Translation</div>
<h1>Translate Signs → Sinhala &amp; English</h1>
<p>Convert recognized SLSL sign sequences into natural Sinhala and English sentences with voice playback.</p>
</div>
<div className="page-actions">
<span className="hud-system-chip"><i></i> Translation Ready</span>
<a className="secondary-btn" href="/recognition">← Recognition</a>
</div>
</section>
<section className="hud-translation-layout">

<article className="card hud-gloss-console">
<div className="hud-titlebar">
<div>
<div className="hud-label">Recognized Signs</div>
<h2>Your SLSL Sign Sequence</h2>
</div>
<span className="small-badge">SIGN STREAM</span>
</div>
<div id="translationSequence" className="sequence-editor">
<span>I</span><b>›</b><span>TOMORROW</span><b>›</b><span>HOSPITAL</span><b>›</b><span>GO</span>
</div>
<div className="hud-telemetry">
<div>
<span>Input</span>
<strong>SLSL Signs</strong>
<div className="hud-bar"><i style={{width: "100%"}}></i></div>
</div>
<div>
<span>Status</span>
<strong>Ready</strong>
<div className="hud-bar"><i style={{width: "85%"}}></i></div>
</div>
<div>
<span>Sentence</span>
<strong>Detected</strong>
<div className="hud-bar"><i style={{width: "100%"}}></i></div>
</div>
</div>
<div className="hud-controls">
<button id="translateBtn" className="primary-btn">文 Generate Translation</button>
<button id="clearTranslation" className="secondary-btn">Clear</button>
</div>
<div className="hud-feedback-line" style={{marginTop: "14px"}}>
        ℹ Translation produces natural, complete sentences — not word-by-word.
      </div>
</article>

<article className="card hud-translation-console">
<div className="hud-titlebar">
<div>
<div className="hud-label">Translation Result</div>
<h2>Sinhala &amp; English</h2>
</div>
<span id="translationState" className="state-badge">READY</span>
</div>
<div id="translationPlaceholder" className="translation-waiting">
<div>文</div>
<strong>Ready to Translate</strong>
<p>Click "Generate Translation" to view Sinhala, English and voice synthesis.</p>
</div>
<div id="translationResults" className="translation-results hidden">
<div className="result-language">
<span>Sinhala Translation</span>
<p id="trSinhala">මම හෙට රෝහලට යනවා.</p>
<button id="trSpeakSinhala" className="secondary-btn">🔊 Play Sinhala Voice</button>
</div>
<div className="result-language">
<span>English Translation</span>
<p id="trEnglish">I will go to the hospital tomorrow.</p>
<button id="trSpeakEnglish" className="secondary-btn">🔊 Play English Voice</button>
</div>
<div className="hud-audio-console">
<div className="hud-titlebar">
<div>
<div className="hud-label">Voice Synthesis</div>
<h2 style={{fontSize: "13px"}}>Speech Waveform</h2>
</div>
<span className="small-badge good">AUDIO READY</span>
</div>
<div className="hud-wave" aria-label="Speech playback animation">
<i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i>
</div>
</div>
</div>
</article>
</section>

<section className="hud-flow-strip">
<div className="flow-step">
<span>🤟</span>
<strong>You Sign</strong>
<small>Camera detects your signs</small>
</div>
<div className="flow-step">
<span>🧩</span>
<strong>Signs Recognized</strong>
<small>Sequence captured</small>
</div>
<div className="flow-step">
<span>文</span>
<strong>Translated</strong>
<small>Sinhala &amp; English</small>
</div>
<div className="flow-step">
<span>✓</span>
<strong>Natural Sentence</strong>
<small>Fluent phrasing</small>
</div>
<div className="flow-step">
<span>🔊</span>
<strong>Voice Plays</strong>
<small>Spoken aloud</small>
</div>
</section>
</main>



</>);
}
