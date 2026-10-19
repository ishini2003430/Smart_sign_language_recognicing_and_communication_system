import React from "react";
import { UserNav, ResearchSidebar } from "../components/Navigation";
import { useState } from "react";
import { navigate } from "../navigation";

export default function IndexPage() {
  const [role,setRole]=useState("user");
  return (<>

<main className="auth-shell">

<section className="auth-visual">
<div className="auth-brand">
<span className="auth-logo">🤟</span>
<span>
<strong>SLSL</strong>
<small>Smart Communication</small>
</span>
</div>
<div className="auth-copy">
<h1>Communication without barriers.</h1>
<p>Recognize Sri Lankan Sign Language in real-time, translate messages seamlessly with voice synthesis, learn signs with motion feedback, and connect Deaf and hearing users.</p>
<div className="auth-flow">
<span>📷 Real-Time Vision</span>
<span>文 Bilingual Translation</span>
<span>🎓 Corrective Learning</span>
<span>💬 2-Way Chat</span>
</div>
</div>
<small>Sri Lankan Sign Language AI Platform Prototype</small>
</section>

<section className="auth-form-side">
<div style={{width: "min(440px, 100%)"}}>
<div style={{display: "flex", justifyContent: "flex-end", marginBottom: "12px"}}>
<button type="button" className="theme-toggle" aria-label="Switch theme">☾ Theme</button>
</div>
<form id="loginForm" className="auth-card" onSubmit={e => {e.preventDefault(); navigate(role === "researcher" ? "/research-dashboard" : "/dashboard");}}>
<h2>Welcome back</h2>
<p>Sign in to continue to the SLSL platform.</p>
<label className="field">
          Email Address
          <input type="email" defaultValue="kamani@example.com" required={true} />
</label>
<label className="field">
          Password
          <input type="password" defaultValue="prototype" required={true} />
</label>
<div className="role-label">Select Prototype Role</div>
<div className="role-grid">
<button type="button" className={role === "user" ? "role-btn active" : "role-btn"} data-role="user" onClick={() => setRole("user")}>👤 User</button>
<button type="button" className={role === "researcher" ? "role-btn active" : "role-btn"} data-role="researcher" onClick={() => setRole("researcher")}>🧪 Researcher</button>
</div>
<input type="hidden" id="loginRole" value={role} readOnly={true} />
<button className="auth-submit" type="submit">Sign In</button>
<div className="auth-note">
          Select <strong>User</strong> for normal communication and learning, or <strong>Researcher</strong> for the evaluation console.
        </div>
<div className="auth-bottom">
          New user? <a href="/signup">Create an account</a>
</div>
</form>
</div>
</section>
</main>


</>);
}
