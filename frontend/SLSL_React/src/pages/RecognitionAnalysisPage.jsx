import React from "react";
import { UserNav, ResearchSidebar } from "../components/Navigation";

export default function RecognitionAnalysisPage() {
  
  return (<>

<div className="research-shell">
<ResearchSidebar />
<main className="research-main">
<header className="research-topbar">
<div>
<h1>Recognition Analysis</h1>
<p>Signer independence, similar-sign confusion matrix, environmental robustness, and model comparison.</p>
</div>
<div className="research-account">
<span className="research-avatar">I</span>
<div>
<strong>Ishini</strong>
<small>Researcher</small>
</div>
</div>
</header>

<div className="tabs">
<button className="tab-btn active" data-tab="overview">Overview</button>
<button className="tab-btn" data-tab="signer">Signer Independence</button>
<button className="tab-btn" data-tab="similar">Similar Sign Analysis</button>
<button className="tab-btn" data-tab="robustness">Robustness</button>
<button className="tab-btn" data-tab="models">Model Comparison</button>
</div>

<section id="overview" className="tab-panel active">
<div className="stat-grid">
<article className="card analysis-stat">
<span>Overall Accuracy</span>
<strong>—</strong>
<small>Awaiting experimental evaluation</small>
</article>
<article className="card analysis-stat">
<span>Macro F1</span>
<strong>—</strong>
<small>Awaiting experimental evaluation</small>
</article>
<article className="card analysis-stat">
<span>Unseen-Signer Accuracy</span>
<strong>—</strong>
<small>Signer-independent test protocol</small>
</article>
<article className="card analysis-stat">
<span>Average Latency</span>
<strong>—</strong>
<small>Real-time inference benchmark</small>
</article>
</div>
<div className="section two-grid">
<article className="card padded">
<div className="section-heading">
<div>
<h2>Signer-Disjoint Split Protocol</h2>
<p>Signer allocation structure for experimental evaluation.</p>
</div>
</div>
<div className="split-grid">
<div>
<span>Training Signers</span>
<strong>S01–S07</strong>
</div>
<div>
<span>Validation</span>
<strong>S08</strong>
</div>
<div className="highlight">
<span>Unseen Test</span>
<strong>S09–S10</strong>
</div>
</div>
<p className="note">Signers in the test split are never seen during training to guarantee generalizability evidence.</p>
</article>
<article className="card padded">
<div className="section-heading">
<div>
<h2>Real-Time Diagnostics</h2>
<p>Inference pipeline operational parameters.</p>
</div>
</div>
<div className="diagnostic-grid">
<div>
<span>Target FPS</span>
<strong>—</strong>
</div>
<div>
<span>Model Latency</span>
<strong>—</strong>
</div>
<div>
<span>Pipeline Status</span>
<strong className="good">Ready</strong>
</div>
<div>
<span>Landmarks</span>
<strong className="good">Teal 21-pt</strong>
</div>
</div>
</article>
</div>
</section>

<section id="signer" className="tab-panel">
<div className="section two-grid">
<article className="card padded">
<div className="section-heading">
<div>
<h2>Unseen Signer Generalization</h2>
<p>Performance on signers completely excluded from training.</p>
</div>
</div>
<table className="data-table">
<thead>
<tr>
<th>Split</th>
<th>Signer IDs</th>
<th>Accuracy</th>
<th>Macro F1</th>
</tr>
</thead>
<tbody>
<tr>
<td>Training</td>
<td>S01–S07</td>
<td>—</td>
<td>—</td>
</tr>
<tr>
<td>Validation</td>
<td>S08</td>
<td>—</td>
<td>—</td>
</tr>
<tr>
<td>Unseen Test</td>
<td>S09–S10</td>
<td>—</td>
<td>—</td>
</tr>
</tbody>
</table>
</article>
<article className="card padded">
<div className="section-heading">
<div>
<h2>Signer Independence Protocol Note</h2>
</div>
</div>
<p className="note">A strict signer-disjoint split evaluates whether the network learns sign representations rather than memorizing individual signers' appearance or signing nuances.</p>
</article>
</div>
</section>

<section id="similar" className="tab-panel">
<div className="section two-grid">
<article className="card padded">
<div className="section-heading">
<div>
<h2>Confusion Matrix</h2>
<p>Top confused class matrix (populated from test evaluations).</p>
</div>
</div>
<div className="confusion-grid">
<div className="diag">—</div><div>—</div><div>—</div><div>—</div><div>—</div>
<div>—</div><div className="diag">—</div><div>—</div><div>—</div><div>—</div>
<div>—</div><div>—</div><div className="diag">—</div><div>—</div><div>—</div>
<div>—</div><div>—</div><div>—</div><div className="diag">—</div><div>—</div>
<div>—</div><div>—</div><div>—</div><div>—</div><div className="diag">—</div>
</div>
<p className="note">Confusion values will be calculated directly from final test predictions.</p>
</article>
<article className="card padded">
<div className="section-heading">
<div>
<h2>Most Confused Sign Pairs</h2>
<p>Pairs with similar hand shapes or motion paths.</p>
</div>
</div>
<div className="pair-list">
<div className="pair"><strong>AYUBOWAN ↔ THANK YOU</strong><span>Awaiting test run</span></div>
<div className="pair"><strong>HOSPITAL ↔ SCHOOL</strong><span>Awaiting test run</span></div>
<div className="pair"><strong>GO ↔ COME</strong><span>Awaiting test run</span></div>
</div>
</article>
</div>
</section>

<section id="robustness" className="tab-panel">
<article className="card padded">
<div className="section-heading">
<div>
<h2>Environmental Robustness Conditions</h2>
<p>Evaluation across lighting, distance, and background variations.</p>
</div>
</div>
<table className="data-table">
<thead>
<tr>
<th>Condition</th>
<th>Accuracy</th>
<th>Macro F1</th>
<th>Notes</th>
</tr>
</thead>
<tbody>
<tr>
<td>Normal Lighting</td>
<td>—</td>
<td>—</td>
<td>Standard lab illumination</td>
</tr>
<tr>
<td>Low Lighting</td>
<td>—</td>
<td>—</td>
<td>Reduced ambient light test</td>
</tr>
<tr>
<td>Complex Background</td>
<td>—</td>
<td>—</td>
<td>Non-uniform real-world environment</td>
</tr>
<tr>
<td>Camera Angle Variation</td>
<td>—</td>
<td>—</td>
<td>±15° off-axis orientation</td>
</tr>
</tbody>
</table>
</article>
</section>

<section id="models" className="tab-panel">
<article className="card padded">
<div className="section-heading">
<div>
<h2>Baseline Model Comparison</h2>
<p>Comparison across identical datasets and signer-disjoint splits.</p>
</div>
</div>
<table className="data-table">
<thead>
<tr>
<th>Model Architecture</th>
<th>Accuracy</th>
<th>Macro F1</th>
<th>Unseen Signer F1</th>
<th>Latency</th>
<th>Status</th>
</tr>
</thead>
<tbody>
<tr>
<td>Landmark + LSTM Baseline</td>
<td>—</td>
<td>—</td>
<td>—</td>
<td>—</td>
<td>To Evaluate</td>
</tr>
<tr>
<td>CNN + BiLSTM + Attention</td>
<td>—</td>
<td>—</td>
<td>—</td>
<td>—</td>
<td>To Evaluate</td>
</tr>
<tr>
<td>Landmark Spatial-Temporal Transformer</td>
<td>—</td>
<td>—</td>
<td>—</td>
<td>—</td>
<td>To Evaluate</td>
</tr>
<tr>
<td><strong>Proposed Recognition Model</strong></td>
<td>—</td>
<td>—</td>
<td>—</td>
<td>—</td>
<td><span className="small-badge">Proposed</span></td>
</tr>
</tbody>
</table>
<p className="note">All baselines will be benchmarked on the identical SLSL dataset split.</p>
</article>
</section>
<div className="footer-tip">
      Research evaluation metrics deliberately remain blank (—) until measured on the finalized experimental protocol.
    </div>
</main>
</div>



</>);
}
