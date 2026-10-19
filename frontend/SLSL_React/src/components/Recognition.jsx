import React, {useCallback, useContext, useEffect, useMemo, useState, createContext} from 'react';
const RecContext=createContext(null);

function normalizedResult(data) {
  if (!data || typeof data!=='object') throw new Error('API returned an invalid JSON result.');
  const prediction = data.prediction || data.top1 || (Array.isArray(data.candidates) ? data.candidates[0] : null);
  const candidates = data.candidates || data.top_k || data.topK || [];
  if (!prediction && (!Array.isArray(candidates) || !candidates.length)) throw new Error('The API response has no predictions.');
  return {prediction, candidates:Array.isArray(candidates)?candidates:[], raw:data};
}
export function RecognitionProvider({children}) {
 const [file,setFile]=useState(null);
 const [url,setUrl]=useState('');
 const [model,setModel]=useState('lstm');
 const [loading,setLoading]=useState(false);
 const [status,setStatus]=useState('Upload a recorded SLSL sign to start.');
 const [result,setResult]=useState(null);
 useEffect(()=>{
  if (!file){setUrl('');return;}
  const next=URL.createObjectURL(file);setUrl(next);return ()=>URL.revokeObjectURL(next);
 },[file]);
 const clear=useCallback(()=>{setFile(null);setResult(null);setStatus('Upload a recorded SLSL sign to start.');},[]);
 const run=useCallback(async()=>{
  if(!file)return;
  setLoading(true);setResult(null);setStatus('Contacting the Python recognition API...');
  const form=new FormData();form.append('video',file);form.append('model_id',model);
  const endpoint=import.meta.env.VITE_RECOGNITION_ENDPOINT || '/api/recognition/predict';
  try {
    const response=await fetch(endpoint,{method:'POST',body:form});
    if(!response.ok)throw new Error(`Backend returned HTTP ${response.status}. Check API endpoint and trained model.`);
    const payload=await response.json();setResult(normalizedResult(payload));setStatus('Prediction returned by backend.');
  } catch(e) {
    setStatus(`Backend not connected: ${e.message}. This React frontend does not invent predictions.`);
  } finally {setLoading(false);}
 },[file,model]);
 const value=useMemo(()=>({file,url,model,setModel,setFile,loading,status,result,clear,run}),[file,url,model,loading,status,result,clear,run]);
 return <RecContext.Provider value={value}>{children}</RecContext.Provider>;
}
function useRec(){const ctx=useContext(RecContext);if(!ctx)throw new Error('Requires RecognitionProvider');return ctx;}
export function RecognitionPreview(){
 const {url}=useRec();
 return <div style={{width:'100%',height:'100%',minHeight:'270px',display:'flex',justifyContent:'center',alignItems:'center',background:'#111b2b',borderRadius:'10px',overflow:'hidden'}}>
   {url?<video key={url} src={url} controls playsInline style={{width:'100%',height:'100%',maxHeight:'430px',objectFit:'contain'}} />:<div style={{textAlign:'center',color:'#dde7f1',padding:'34px 18px'}}><div style={{fontSize:'48px',marginBottom:'8px'}}>🤟</div><strong>Video preview</strong><p style={{marginTop:'8px',fontSize:'13px'}}>Choose an MP4 clip below. The original camera illustration has been replaced with a real video preview.</p></div>}
 </div>;
}
export function RecognitionControls(){
 const {file,setFile,model,setModel,loading,status,run,clear}=useRec();
 return <div className="recognition-upload-panel">
  <div className="rec-upload-row">
   <label className="rec-upload-label">Recorded SLSL video <input type="file" accept="video/*,.mp4" onChange={e=>setFile(e.target.files?.[0] || null)} /></label>
   <label className="rec-model-label">Recognition model <select value={model} onChange={e=>setModel(e.target.value)}><option value="lstm">LSTM</option><option value="gru">GRU</option><option value="conv1d_bilstm">Conv1D + BiLSTM</option></select></label>
  </div>
  <div className="camera-controls-bar">
   <button type="button" className="primary-btn" disabled={!file||loading} onClick={run}>{loading?'◌ Running…':'▶ Predict Sign'}</button>
   <button type="button" className="secondary-btn" onClick={clear}>Clear</button>
  </div>
  <div className="rec-api-status" role="status">{status}</div>
 </div>;
}
export function RecognitionResults(){
 const {result,model}=useRec();
 const prediction=result?.prediction;
 const candidates=result?.candidates || [];
 return <article className="card recognition-results-workspace">
  <div className="hud-titlebar"><div><div className="hud-label">Model Inference</div><h2>Recognized Sign</h2></div><span className="small-badge">{model.toUpperCase()}</span></div>
  {prediction ? <div className="rec-result-hero"><div className="symbol">🖐</div><div className="label">Predicted SLSL sign</div><div className="value">{prediction.sinhala || prediction.gloss || prediction.label || prediction.sign_id || 'Unknown'}</div><div className="muted">Sign ID: {prediction.sign_id || 'Not provided'} · Visual score: {typeof prediction.score === 'number' ? prediction.score.toFixed(3) : 'Not provided'}</div></div>
   : <div className="rec-result-hero"><div className="symbol">🤟</div><div className="label">Recognition status</div><div className="value" style={{fontSize:'18px'}}>Waiting for a backend prediction</div><div className="muted">No hard-coded or simulated AI result is displayed.</div></div>}
  <div className="rec-section-divider"><div className="rec-section-header"><h3>Top-K Visual Candidates</h3><span className="small-badge">{candidates.length?`${candidates.length} candidates`:'Not available'}</span></div>
   <div className="sequence-box">{candidates.length?<ol className="rec-candidate-list">{candidates.map((c,i)=><li key={i}><strong>{c.gloss || c.label || c.sign_id || `Candidate ${i+1}`}</strong> <span>{c.sign_id || ''}</span><span>{typeof c.score==='number'?c.score.toFixed(3):'—'}</span></li>)}</ol>:<p>Top-k predictions will appear here after the model API responds.</p>}</div>
  </div>
  <div className="rec-section-divider"><div className="rec-section-header"><h3>Mendis's context component</h3><span className="small-badge">Integration pending</span></div><p className="muted" style={{fontSize:'13px'}}>This page will pass ranked visual sign IDs and scores to the context-aware interpretation service after backend integration.</p></div>
 </article>;
}
