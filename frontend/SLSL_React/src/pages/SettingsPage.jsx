import React from "react";
import { UserNav, ResearchSidebar } from "../components/Navigation";

export default function SettingsPage() {
  
  return (<>

<UserNav />
<main className="user-main">
<section className="user-page-header">
<div>
<h1>Settings &amp; Accessibility</h1>
<p>Configure theme appearance, language preferences, and visual-first accessibility features.</p>
</div>
<button id="saveSettings" className="primary-btn">Save Settings</button>
</section>

<section className="settings-grid">
<article className="card settings-card">
<div className="section-title-row">
<div>
<h2>Theme Appearance</h2>
<p>Choose between clean light mode or high-contrast dark mode.</p>
</div>
</div>
<div className="theme-choice">
<button type="button" data-set-theme="light">☀️ Light Theme</button>
<button type="button" data-set-theme="dark">🌙 Dark Theme</button>
</div>
<p className="muted" style={{marginTop: "14px", fontSize: "12px"}}>
        You can also toggle the theme anytime using the button in the top navigation bar.
      </p>
</article>
<article className="card settings-card">
<div className="section-title-row">
<div>
<h2>Language &amp; Speech</h2>
</div>
</div>
<label className="field">
        Interface Language
        <select>
<option>English</option>
<option>Sinhala (සිංහල)</option>
</select>
</label>
<label className="field">
        Default TTS Voice
        <select>
<option>English (US) Female</option>
<option>Sinhala (LK) Native</option>
</select>
</label>
<div className="setting-row">
<div>
<strong>Auto Speak Translations</strong>
<span>Automatically synthesize speech for hearing users upon sentence finalization</span>
</div>
<label className="toggle"><input type="checkbox" checked={true} /><span className="slider"></span></label>
</div>
<div className="setting-row">
<div>
<strong>Always Show Captions</strong>
<span>Keep text visible on-screen at all times so Deaf users never miss messages</span>
</div>
<label className="toggle"><input type="checkbox" checked={true} /><span className="slider"></span></label>
</div>
</article>
</section>

<section className="section settings-grid">
<article className="card settings-card">
<div className="section-title-row">
<div>
<h2>Visual Accessibility</h2>
</div>
</div>
<div className="setting-row">
<div>
<strong>Larger Text Size</strong>
<span>Increase base font size across all modules</span>
</div>
<label className="toggle"><input id="toggleLargeText" type="checkbox" /><span className="slider"></span></label>
</div>
<div className="setting-row">
<div>
<strong>High Contrast Mode</strong>
<span>Enhance borders and text definition for maximum readability</span>
</div>
<label className="toggle"><input id="toggleHighContrast" type="checkbox" /><span className="slider"></span></label>
</div>
<div className="setting-row">
<div>
<strong>Voice Playback Controls</strong>
<span>Always display manual voice play buttons</span>
</div>
<label className="toggle"><input type="checkbox" checked={true} /><span className="slider"></span></label>
</div>
</article>
<article className="card settings-card">
<div className="section-title-row">
<div>
<h2>Camera Guidance Preferences</h2>
</div>
</div>
<div className="setting-row">
<div>
<strong>Show Capture Indicators</strong>
<span>Display hands detected, tracking, lighting, and position chips</span>
</div>
<label className="toggle"><input type="checkbox" checked={true} /><span className="slider"></span></label>
</div>
<div className="setting-row">
<div>
<strong>Simplified Statuses</strong>
<span>Show simple status badges instead of internal parameters</span>
</div>
<label className="toggle"><input type="checkbox" checked={true} /><span className="slider"></span></label>
</div>
</article>
</section>
</main>



</>);
}
