import React from "react";
import { UserNav, ResearchSidebar } from "../components/Navigation";

export default function ProfilePage() {
  
  return (<>

<UserNav />
<main className="user-main">
<section className="user-page-header">
<div>
<h1>User Profile</h1>
<p>Manage your account settings and personal preferences.</p>
</div>
<button className="primary-btn">Save Changes</button>
</section>

<section className="card profile-hero">
<div className="profile-big-avatar">K</div>
<div>
<h2>Kamani Perera</h2>
<p>SLSL Community User · Colombo, Sri Lanka</p>
<span className="small-badge">Normal User Account</span>
</div>
</section>

<section className="section settings-grid">
<article className="card settings-card">
<div className="section-title-row">
<div>
<h2>Personal Information</h2>
</div>
</div>
<label className="field">
        Full Name
        <input defaultValue="Kamani Perera" />
</label>
<label className="field">
        Email Address
        <input type="email" defaultValue="kamani@example.com" />
</label>
<label className="field">
        Preferred Primary Language
        <select>
<option>Sinhala (සිංහල)</option>
<option>English</option>
</select>
</label>
<label className="field">
        Location
        <input defaultValue="Colombo, Sri Lanka" />
</label>
</article>
<article className="card settings-card">
<div className="section-title-row">
<div>
<h2>Account &amp; Security</h2>
</div>
</div>
<div className="setting-row">
<div>
<strong>Account Role</strong>
<span>Standard user access</span>
</div>
<span className="small-badge">User</span>
</div>
<div className="setting-row">
<div>
<strong>Password</strong>
<span>Last updated 1 month ago</span>
</div>
<button className="secondary-btn">Change</button>
</div>
<div className="setting-row">
<div>
<strong>Learning Dashboard</strong>
<span>View your progress logs</span>
</div>
<a className="secondary-btn" href="/progress">View</a>
</div>
<div className="setting-row">
<div>
<strong>Sign Out</strong>
<span>End current session</span>
</div>
<a className="danger-btn" href="/">Logout</a>
</div>
</article>
</section>
</main>


</>);
}
