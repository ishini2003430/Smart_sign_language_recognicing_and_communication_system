/**
 * api.js — API client for the SLSL sign animation backend.
 *
 * All fetch calls go through this module.  The Vite dev server proxies
 * /api/* and /static/* to http://localhost:8000 automatically.
 *
 * In production, set VITE_API_BASE in .env (defaults to empty string
 * so relative paths work).
 */

const BASE = import.meta.env.VITE_API_BASE ?? '';

/**
 * Check whether the backend is running and the sign database is loaded.
 * @returns {Promise<object>} Health response object.
 */
export async function fetchHealth() {
  const res = await fetch(`${BASE}/api/health`);
  if (!res.ok) throw new Error(`Health check failed: ${res.status}`);
  return res.json();
}

/**
 * Fetch all registered signs from the backend.
 * @returns {Promise<object>} { total, with_video, signs: [...] }
 */
export async function fetchSigns() {
  const res = await fetch(`${BASE}/api/signs`);
  if (!res.ok) throw new Error(`Failed to fetch signs: ${res.status}`);
  return res.json();
}

/**
 * Translate text into a sign playback sequence.
 *
 * @param {string} text — English or Sinhala input.
 * @param {string} source — 'text_input' | 'speech_input'
 * @returns {Promise<TranslateResponse>}
 */
export async function translateText(text, source = 'text_input') {
  const res = await fetch(`${BASE}/api/translate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, source }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail ?? `Translation failed: ${res.status}`);
  }
  return res.json();
}

/**
 * Send text recognised by a teammate's sign-recognition module to the backend.
 *
 * @param {string} text — Recognised text.
 * @param {string} recognizedBy — Identifier of the recognition module.
 * @returns {Promise<object>}
 */
export async function sendRecognisedText(text, recognizedBy = 'recognition_module') {
  const res = await fetch(`${BASE}/api/recognized-text`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, recognized_by: recognizedBy }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail ?? `Request failed: ${res.status}`);
  }
  return res.json();
}
