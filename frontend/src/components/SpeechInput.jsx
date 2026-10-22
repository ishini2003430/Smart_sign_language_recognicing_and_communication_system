/**
 * SpeechInput.jsx
 * ===============
 * Microphone-based speech input using the browser Web Speech API.
 *
 * - Works natively in Chrome and Edge (no API key, no server round-trip).
 * - Shows a clear message in Firefox/Safari where the API is unsupported.
 * - Handles permission errors gracefully.
 * - Calls onTranscript(text) when speech is recognised.
 */

import React, { useState, useRef, useEffect } from 'react';

const MicIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
    <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm-1-9c0-.55.45-1 1-1s1 .45 1 1v6c0 .55-.45 1-1 1s-1-.45-1-1V5zm6 6c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
  </svg>
);
const StopIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
    <path d="M6 6h12v12H6z"/>
  </svg>
);

const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;

/**
 * @param {{ onTranscript: (text: string) => void, disabled?: boolean }} props
 */
export default function SpeechInput({ onTranscript, disabled = false }) {
  const [isListening, setIsListening] = useState(false);
  const [interimText, setInterimText] = useState('');
  const [error, setError] = useState(null);
  const recognitionRef = useRef(null);

  const isSupported = Boolean(SpeechRecognition);

  useEffect(() => {
    return () => {
      recognitionRef.current?.abort();
    };
  }, []);

  const startListening = () => {
    if (!isSupported) return;
    setError(null);
    setInterimText('');

    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';      // English default
    recognition.interimResults = true;
    recognition.maxAlternatives = 1;
    recognition.continuous = false;

    recognition.onresult = (event) => {
      let interim = '';
      let final = '';
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const result = event.results[i];
        if (result.isFinal) {
          final += result[0].transcript;
        } else {
          interim += result[0].transcript;
        }
      }
      setInterimText(interim || final);
      if (final) {
        onTranscript(final.trim());
        setInterimText('');
      }
    };

    recognition.onerror = (event) => {
      setIsListening(false);
      setInterimText('');
      if (event.error === 'not-allowed') {
        setError('Microphone permission denied. Please allow microphone access in your browser settings and try again.');
      } else if (event.error === 'no-speech') {
        setError('No speech detected. Please speak clearly and try again.');
      } else if (event.error === 'network') {
        setError('Network error. The Web Speech API requires an internet connection for recognition.');
      } else {
        setError(`Speech recognition error: ${event.error}`);
      }
    };

    recognition.onend = () => {
      setIsListening(false);
      setInterimText('');
    };

    recognitionRef.current = recognition;
    recognition.start();
    setIsListening(true);
  };

  const stopListening = () => {
    recognitionRef.current?.stop();
    setIsListening(false);
    setInterimText('');
  };

  if (!isSupported) {
    return (
      <div className="alert alert-warning" style={{ fontSize: '0.85rem' }}>
        <span>🎤</span>
        <div>
          <strong>Speech input unavailable.</strong> Your browser does not support the Web Speech API.
          Please use <strong>Chrome</strong> or <strong>Edge</strong> for speech input, or type your text directly.
        </div>
      </div>
    );
  }

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <button
          className={`btn ${isListening ? 'btn-primary' : 'btn-ghost'} btn-icon`}
          onClick={isListening ? stopListening : startListening}
          disabled={disabled}
          aria-label={isListening ? 'Stop listening' : 'Start speech input'}
          title={isListening ? 'Stop' : 'Start speech input'}
          style={isListening ? {
            boxShadow: '0 0 0 4px rgba(239, 68, 68, 0.2)',
            background: 'var(--danger)',
          } : {}}
        >
          {isListening ? <StopIcon /> : <MicIcon />}
        </button>

        <div style={{ flex: 1, minWidth: 0 }}>
          {isListening && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div className="spinner" style={{ width: 14, height: 14 }} />
              <span style={{
                color: 'var(--text-secondary)', fontSize: '0.85rem',
                fontStyle: 'italic', overflow: 'hidden', textOverflow: 'ellipsis',
                whiteSpace: 'nowrap',
              }}>
                {interimText || 'Listening…'}
              </span>
            </div>
          )}
          {!isListening && !error && (
            <span style={{ color: 'var(--text-muted)', fontSize: '0.82rem' }}>
              Click the mic to speak — Chrome / Edge only
            </span>
          )}
        </div>
      </div>

      {error && (
        <div className="alert alert-danger" style={{ marginTop: '10px', fontSize: '0.83rem' }}>
          <span>⚠️</span>
          <span>{error}</span>
        </div>
      )}
    </div>
  );
}
