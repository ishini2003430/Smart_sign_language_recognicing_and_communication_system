import React from "react";
import { UserNav, ResearchSidebar } from "../components/Navigation";

export default function DatasetPage() {
  
  return (<>

<div className="research-shell">
<ResearchSidebar />
<main className="research-main">
<header className="research-topbar">
<div>
<h1>Dataset Management</h1>
<p>Manage sign classes, signer annotations, split distributions, and environmental capture metadata.</p>
</div>
<div className="research-account">
<span className="research-avatar">I</span>
<div>
<strong>Ishini</strong>
<small>Researcher</small>
</div>
</div>
</header>

<section className="section">
<div className="overview-grid">
<article className="card overview-card">
<span className="overview-icon">☝</span>
<div>
<span>Sign Classes</span>
<strong>100</strong>
<small>Vocabulary coverage</small>
</div>
</article>
<article className="card overview-card">
<span className="overview-icon">▧</span>
<div>
<span>Gesture Samples</span>
<strong>485</strong>
<small>Recorded sequences</small>
</div>
</article>
<article className="card overview-card">
<span className="overview-icon">👥</span>
<div>
<span>Signer IDs</span>
<strong>10</strong>
<small>Disjoint signers</small>
</div>
</article>
<article className="card overview-card">
<span className="overview-icon">✓</span>
<div>
<span>Annotation</span>
<strong style={{fontSize: "15px", color: "var(--green)"}}>In Progress</strong>
<small>Landmark verification</small>
</div>
</article>
</div>
</section>

<div className="toolbar">
<div style={{flex: "1", maxWidth: "320px"}}>
<input id="datasetSearch" className="search-input" placeholder="Search sign name or signer ID..." />
</div>
<div className="toolbar-actions">
<select className="select-input">
<option>All Splits</option>
<option>Train (S01–S07)</option>
<option>Validation (S08)</option>
<option>Unseen Test (S09–S10)</option>
</select>
<button id="addSample" className="research-btn primary">+ Add Sample</button>
</div>
</div>

<section className="card research-table-card">
<table className="data-table">
<thead>
<tr>
<th>Sample ID</th>
<th>Sign Class</th>
<th>Signer ID</th>
<th>Split</th>
<th>Lighting</th>
<th>Background</th>
<th>Status</th>
</tr>
</thead>
<tbody id="datasetRows">
<tr data-row="ayubowan s01">
<td>SL001</td>
<td><strong>AYUBOWAN</strong></td>
<td>S01</td>
<td>Train</td>
<td>Normal</td>
<td>Plain</td>
<td><span className="small-badge good">Annotated</span></td>
</tr>
<tr data-row="ayubowan s09">
<td>SL002</td>
<td><strong>AYUBOWAN</strong></td>
<td>S09</td>
<td>Unseen Test</td>
<td>Low</td>
<td>Complex</td>
<td><span className="small-badge good">Annotated</span></td>
</tr>
<tr data-row="hospital s03">
<td>SL003</td>
<td><strong>HOSPITAL</strong></td>
<td>S03</td>
<td>Train</td>
<td>Normal</td>
<td>Plain</td>
<td><span className="small-badge warning">Review</span></td>
</tr>
<tr data-row="go s08">
<td>SL004</td>
<td><strong>GO</strong></td>
<td>S08</td>
<td>Validation</td>
<td>Normal</td>
<td>Complex</td>
<td><span className="small-badge good">Annotated</span></td>
</tr>
<tr data-row="tomorrow s10">
<td>SL005</td>
<td><strong>TOMORROW</strong></td>
<td>S10</td>
<td>Unseen Test</td>
<td>Normal</td>
<td>Plain</td>
<td><span className="small-badge good">Annotated</span></td>
</tr>
</tbody>
</table>
</section>

<section className="section two-grid">
<article className="card padded">
<div className="section-heading">
<div>
<h2>Signer Split Distribution</h2>
<p>Participant partitioning across splits.</p>
</div>
</div>
<div className="split-grid">
<div>
<span>Training</span>
<strong>S01–S07 (70%)</strong>
</div>
<div>
<span>Validation</span>
<strong>S08 (10%)</strong>
</div>
<div className="highlight">
<span>Unseen Test</span>
<strong>S09–S10 (20%)</strong>
</div>
</div>
</article>
<article className="card padded">
<div className="section-heading">
<div>
<h2>Capture Metadata Fields</h2>
<p>Environmental tracking parameters.</p>
</div>
</div>
<div className="diagnostic-grid">
<div>
<span>Lighting</span>
<strong>Normal / Low</strong>
</div>
<div>
<span>Background</span>
<strong>Plain / Complex</strong>
</div>
<div>
<span>Camera Angle</span>
<strong>±15° Tracked</strong>
</div>
<div>
<span>Signer ID</span>
<strong>Strict Tagging</strong>
</div>
</div>
</article>
</section>
</main>
</div>



</>);
}
