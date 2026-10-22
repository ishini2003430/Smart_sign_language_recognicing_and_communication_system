/**
 * RecognitionReceiver.jsx
 * =======================
 * Integration panel for the sign-recognition component.
 *
 * This section allows teammates to test the /api/recognized-text endpoint
 * directly from the UI.  In the deployed system, the recognition module will
 * call that endpoint programmatically; this panel simulates that.
 *
 * The panel also displays the most recently received recognised text and the
 * pipeline result for that text.
 */

import React, { useState } from 'react';
import { sendRecognisedText } from '../services/api.js';

export default function RecognitionReceiver({ onResult }) {
  const [text, setText] = useState('');
  const [recognizer, setRecognizer] = useState('recognition_module_v1');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [lastResult, setLastResult] = useState(null);

  const handleSend = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const result = await sendRecognisedText(text.trim(), recognizer);
      setLastResult(result);
      onResult?.(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-card" style={{ padding: '24px' }}>
      <div style={{ marginBottom: '16px' }}>
        <span className="section-label">Recognition Integration</span>
        <h2 style={{ marginTop: '6px', fontSize: '1.1rem', fontWeight: 600 }}>
          Receive from Sign Recognition Module
        </h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginTop: '4px' }}>
          Simulate the text output from your teammate's recognition component.
          In the final system, the recognition module calls{' '}
          <code style={{ background: 'rgba(255,255,255,0.06)', padding: '1px 6px', borderRadius: '4px', fontSize: '0.8rem' }}>
            POST /api/recognized-text
          </code>{' '}
          directly.
        </p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '14px' }}>
        <input
          className="input"
          type="text"
          id="recognition-module-id"
          placeholder="Recognition module ID (e.g. slsl_recognition_v1)"
          value={recognizer}
          onChange={e => setRecognizer(e.target.value)}
        />
        <div style={{ display: 'flex', gap: '10px' }}>
          <input
            className="input"
            type="text"
            id="recognition-text-input"
            placeholder="Enter recognised text (e.g. 'mother go hospital')"
            value={text}
            onChange={e => setText(e.target.value)}
            onKeyDown={e => { if (e.key === 'Enter') handleSend(); }}
            style={{ flex: 1 }}
          />
          <button
            className="btn btn-primary"
            onClick={handleSend}
            disabled={loading || !text.trim()}
            id="recognition-send-btn"
          >
            {loading ? <span className="spinner" style={{ width: 16, height: 16 }} /> : null}
            Send
          </button>
        </div>
      </div>

      {error && (
        <div className="alert alert-danger" style={{ marginBottom: '12px', fontSize: '0.85rem' }}>
          <span>⚠️</span>
          <span>{error}</span>
        </div>
      )}

      {lastResult && (
        <div style={{
          background: 'rgba(255,255,255,0.03)',
          border: '1px solid var(--border)',
          borderRadius: 'var(--radius-md)',
          padding: '14px',
          fontSize: '0.85rem',
        }}>
          <div style={{ display: 'flex', gap: '8px', marginBottom: '8px', flexWrap: 'wrap' }}>
            <span className="badge badge-info">
              Received from: {lastResult.recognized_by}
            </span>
            <span className={`badge ${lastResult.coverage > 0 ? 'badge-success' : 'badge-warning'}`}>
              {Math.round(lastResult.coverage * 100)}% matched
            </span>
          </div>

          <p style={{ color: 'var(--text-secondary)' }}>
            <strong>Input:</strong> "{lastResult.original_input}"
          </p>

          {lastResult.playback_sequence?.length > 0 && (
            <p style={{ color: 'var(--text-secondary)', marginTop: '4px' }}>
              <strong>Signs found:</strong>{' '}
              {lastResult.playback_sequence.map(s => s.label).join(' → ')}
            </p>
          )}

          {lastResult.missing_tokens?.length > 0 && (
            <p style={{ color: 'var(--warning)', marginTop: '4px' }}>
              <strong>Missing:</strong> {lastResult.missing_tokens.join(', ')}
            </p>
          )}
        </div>
      )}
    </div>
  );
}
