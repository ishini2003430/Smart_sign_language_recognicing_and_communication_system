import React from "react";
import { UserNav, ResearchSidebar } from "../components/Navigation";
import { navigate } from "../navigation";

export default function SignupPage() {
  
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
<h1>Start using SLSL Smart Communication.</h1>
<p>Create a user account to recognize signs, practice SLSL with AI motion analysis, and communicate seamlessly with hearing peers.</p>
<div className="auth-flow">
<span>Accessible</span>
<span>Bilingual Sinhala &amp; English</span>
<span>Visual-First</span>
</div>
</div>
<small>Sri Lankan Sign Language AI Platform Prototype</small>
</section>

<section className="auth-form-side">
<div style={{width: "min(440px, 100%)"}}>
<div style={{display: "flex", justifyContent: "flex-end", marginBottom: "12px"}}>
<button type="button" className="theme-toggle" aria-label="Switch theme">☾ Theme</button>
</div>
<form id="signupForm" onSubmit={e => {e.preventDefault();navigate("/dashboard");}} className="auth-card">
<h2>Create Account</h2>
<p>Register for a normal user account.</p>
<label className="field">
          Full Name
          <input required={true} placeholder="Your full name" />
</label>
<label className="field">
          Email Address
          <input type="email" required={true} placeholder="name@example.com" />
</label>
<label className="field">
          Password
          <input type="password" required={true} placeholder="Create secure password" />
</label>
<label className="field">
          Confirm Password
          <input type="password" required={true} placeholder="Confirm your password" />
</label>
<button className="auth-submit" type="submit">Create Account</button>
<div className="auth-bottom">
          Already registered? <a href="/">Sign in</a>
</div>
</form>
</div>
</section>
</main>


</>);
}
