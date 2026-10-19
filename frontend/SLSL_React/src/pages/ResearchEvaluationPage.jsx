import React from "react";
import { UserNav, ResearchSidebar } from "../components/Navigation";

export default function ResearchEvaluationPage() {
  
  return (<>

<div className="research-shell">
<ResearchSidebar />
<main className="research-main">
<header className="research-topbar">
<div>
<h1>Research Evaluation</h1>
<p>Cross-component validation matrix, experiment status, and integrated system evidence.</p>
</div>
<div className="research-account">
<span className="research-avatar">I</span>
<div>
<strong>Ishini</strong>
<small>Researcher</small>
</div>
</div>
</header>

<section className="section stat-grid">
<article className="card analysis-stat">
<span>Recognition Validation</span>
<strong>—</strong>
<small>Awaiting full experiments</small>
</article>
<article className="card analysis-stat">
<span>Translation Validation</span>
<strong>—</strong>
<small>Awaiting full experiments</small>
</article>
<article className="card analysis-stat">
<span>Learner Feedback Accuracy</span>
<strong>—</strong>
<small>Awaiting full experiments</small>
</article>
<article className="card analysis-stat">
<span>End-to-End Latency</span>
<strong>—</strong>
<small>Awaiting full experiments</small>
</article>
</section>

<section className="section card padded">
<div className="section-heading">
<div>
<h2>Component Evaluation Matrix</h2>
<p>Evaluation protocols and planned performance targets.</p>
</div>
</div>
<table className="data-table">
<thead>
<tr>
<th>Component</th>
<th>Primary Evaluation Focus</th>
<th>Target Metrics</th>
<th>Status</th>
<th>Result</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>SLSL Recognition</strong></td>
<td>Unseen signers, similar sign pairs, environmental robustness</td>
<td>Accuracy, Macro F1, Inference Latency</td>
<td><span className="small-badge">Planned</span></td>
<td>—</td>
</tr>
<tr>
<td><strong>Context Translation</strong></td>
<td>Grammatical naturalness in Sinhala and English</td>
<td>BLEU / ROUGE / Human Evaluation</td>
<td><span className="small-badge">Planned</span></td>
<td>—</td>
</tr>
<tr>
<td><strong>Learner Error Detection</strong></td>
<td>Hand shape, spatial position, and movement trajectory</td>
<td>Error Classification Precision &amp; Recall</td>
<td><span className="small-badge">Planned</span></td>
<td>—</td>
</tr>
<tr>
<td><strong>Bidirectional Communication</strong></td>
<td>Two-way conversation throughput and user interaction</td>
<td>Task Completion Rate, Turn Latency</td>
<td><span className="small-badge">Planned</span></td>
<td>—</td>
</tr>
</tbody>
</table>
</section>

<section className="section two-grid">
<article className="card padded">
<div className="section-heading">
<div>
<h2>Recognition Evidence Protocol</h2>
<p>Required empirical evidence for publication.</p>
</div>
</div>
<div className="pair-list">
<div className="pair"><strong>Signer-Independent Test Set</strong><span>—</span></div>
<div className="pair"><strong>Similar-Sign Confusion Analysis</strong><span>—</span></div>
<div className="pair"><strong>Lighting &amp; Background Variation</strong><span>—</span></div>
<div className="pair"><strong>Baseline Architectural Comparison</strong><span>—</span></div>
</div>
</article>
<article className="card padded">
<div className="section-heading">
<div>
<h2>Integrated System Evidence</h2>
<p>Verification of end-to-end user workflows.</p>
</div>
</div>
<div className="pair-list">
<div className="pair"><strong>Deaf → Hearing Live Pipeline</strong><span style={{color: "var(--green)"}}>Prototype Ready</span></div>
<div className="pair"><strong>Hearing → Deaf SLSL Generation</strong><span style={{color: "var(--green)"}}>Prototype Ready</span></div>
<div className="pair"><strong>Learner Feedback Loop</strong><span style={{color: "var(--green)"}}>Prototype Ready</span></div>
<div className="pair"><strong>Measured Performance Values</strong><span>Awaiting Experiments</span></div>
</div>
</article>
</section>
<div className="footer-tip">
      This research console deliberately avoids fabricated metrics. Values remain "—" until experimentally measured.
    </div>
</main>
</div>


</>);
}
