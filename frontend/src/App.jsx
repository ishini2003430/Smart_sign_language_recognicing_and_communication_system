
import { useState, useRef } from 'react';
import './App.css';
import SignAnimatorPanel from './components/SignAnimator';

// Use relative paths — Vite proxy forwards /api/* to http://localhost:8000
const API_URL = '';


const QUICK_PHRASES = [
  'I want water',
  'Hello',
  'How are you',
  'Thank you',
  'Help me',
];

export default function App() {
  const [text, setText] = useState('');
  const [results, setResults] = useState([]);
  const [unsupported, setUnsupported] = useState([]);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [history, setHistory] = useState([]);
  const [selectedHistory, setSelectedHistory] = useState(null);

  const avatarRef = useRef(null);

  async function translateText(event) {
    event?.preventDefault();

    if (!text.trim()) {
      setError('Please enter some text first.');
      return;
    }

    setLoading(true);
    setError('');
    setMessage('');
    setResults([]);
    setUnsupported([]);
    setSelectedHistory(null);

    try {
      const response = await fetch(
        `${API_URL}/api/translation/text-to-sign`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: text.trim() }),
        }
      );

      if (!response.ok) {
        throw new Error(`Request failed (${response.status}).`);
      }

      const data = await response.json();
      const matchedSigns = data.matched_signs || [];
      const unsupportedWords = data.unsupported_words || [];

      setResults(matchedSigns);
      setUnsupported(unsupportedWords);
      setMessage(data.message || '');

      setHistory((previous) => [
        {
          id: Date.now(),
          text: text.trim(),
          results: matchedSigns,
          unsupported: unsupportedWords,
          message: data.message || '',
        },
        ...previous,
      ].slice(0, 8));

      // Scroll down to the animator section
      avatarRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });

    } catch (err) {
      setError(
        'Could not connect to the backend. Check that your FastAPI server is running on port 8000.'
      );
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  function startSpeechRecognition() {
    const SpeechRecognition =
      window.SpeechRecognition ||
      window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setError(
        'Speech recognition is not supported in this browser. Try a recent version of Chrome.'
      );
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
      setError('');
      setMessage('Listening for English speech...');
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setText(transcript);
      setMessage('Speech captured. Select Translate to Sign to continue.');
    };

    recognition.onerror = () => {
      setError('Speech recognition failed. Please try again.');
      setMessage('');
    };

    recognition.start();
  }

  function loadHistory(item) {
    setText(item.text);
    setResults(item.results);
    setUnsupported(item.unsupported);
    setMessage(item.message);
    setError('');
    setSelectedHistory(item.id);
  }

  const availableWords = [
    ...new Set(results.map((item) => item.word).filter(Boolean)),
  ];

  return (
    <main className="slsl-app">
      <header className="topbar">
        <div className="brand">
          <div className="brand-icon" aria-hidden="true">S</div>
          <div>
            <p className="brand-name">SMART SLSL</p>
            <p className="brand-caption">
              Sign Language Communication
            </p>
          </div>
        </div>

        <div className="connection-status">
          <span className="status-dot" />
          <span>Translation workspace</span>
        </div>
      </header>

      <section className="page-heading">
        <div>
          <p className="eyebrow">BIDIRECTIONAL COMMUNICATION</p>
          <h1>Text to Sign Language</h1>
          <p className="page-description">
            Enter English text and view the Sri Lankan Sign Language
            videos available in your dataset. Click any sign card to
            drive the 3D avatar.
          </p>
        </div>

        <span className="language-badge">
          English <span aria-hidden="true">→</span> SLSL
        </span>
      </section>

      <section className="workspace">
        <aside className="panel input-panel">
          <div className="panel-heading">
            <div>
              <p className="section-label">STEP 01</p>
              <h2>Enter your message</h2>
            </div>
            <span className="heading-icon" aria-hidden="true">Aa</span>
          </div>

          <form onSubmit={translateText}>
            <label htmlFor="english-text">Your English text</label>

            <textarea
              id="english-text"
              className="message-input"
              value={text}
              onChange={(event) => setText(event.target.value)}
              placeholder="Type a message here, such as I want water..."
              maxLength={1000}
              rows={7}
            />

            <div className="input-meta">
              <span>English text input</span>
              <span>{text.length}/1000</span>
            </div>

            <div className="input-actions">
              <button
                className="secondary-button"
                type="button"
                onClick={startSpeechRecognition}
                disabled={loading}
              >
                <span aria-hidden="true">🎙</span> Speak
              </button>

              <button
                className="secondary-button"
                type="button"
                onClick={() => {
                  setText('');
                  setError('');
                  setMessage('');
                }}
                disabled={loading || !text}
              >
                Clear
              </button>
            </div>

            <button
              className="primary-button translate-button"
              type="submit"
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="spinner" />
                  Processing...
                </>
              ) : (
                <>
                  Translate to Sign
                  <span aria-hidden="true">→</span>
                </>
              )}
            </button>
          </form>

          {error && (
            <div className="notice notice-error" role="alert">
              <strong>Something went wrong</strong>
              <p>{error}</p>
            </div>
          )}

          {message && (
            <div className="notice notice-info" role="status">
              {message}
            </div>
          )}

          {unsupported.length > 0 && (
            <div className="notice notice-warning">
              <strong>Signs not available</strong>
              <p>{unsupported.join(', ')}</p>
              <small>
                These words were reported as unsupported by the backend.
              </small>
            </div>
          )}

          <div className="quick-phrases">
            <p className="section-label">QUICK PHRASES</p>
            <div className="phrase-list">
              {QUICK_PHRASES.map((phrase) => (
                <button
                  className="phrase-chip"
                  key={phrase}
                  type="button"
                  onClick={() => {
                    setText(phrase);
                    setError('');
                    setMessage('');
                  }}
                >
                  {phrase}
                </button>
              ))}
            </div>
          </div>
        </aside>

        <section className="panel output-panel">
          <div className="panel-heading">
            <div>
              <p className="section-label">STEP 02</p>
              <h2>Sign video results</h2>
            </div>
            <span className="heading-icon" aria-hidden="true">▶</span>
          </div>

          {loading ? (
            <div className="empty-state">
              <span className="large-spinner" />
              <h3>Finding available signs</h3>
              <p>Waiting for the translation service...</p>
            </div>
          ) : results.length > 0 ? (
            <>
              <div className="results-summary">
                <span className="result-count">
                  {results.length} sign result
                  {results.length === 1 ? '' : 's'}
                </span>
                <span className="result-caption">
                  Click a card to animate the 3D avatar below
                </span>
              </div>

              <div className="video-grid">
                {results.map((item, index) => {
                  const index_n = index + 1;
                  return (
                    <article
                      className="video-card"
                      key={`${item.word || 'sign'}-${index}`}
                    >
                      <div className="video-card-heading">
                        <h3>{item.word || `Sign ${index + 1}`}</h3>
                        <span className="sign-number">
                          {String(index + 1).padStart(2, '0')}
                        </span>
                      </div>

                      {item.video_found && item.video_url ? (
                        <video
                          className="sign-video"
                          controls
                          playsInline
                          preload="metadata"
                          src={`${API_URL}${item.video_url}`}
                        >
                          Your browser does not support video playback.
                        </video>
                      ) : (
                        <div className="missing-video">
                          <span aria-hidden="true">▧</span>
                          <p>No video is available for this sign.</p>
                        </div>
                      )}

                      <p className="video-label">
                        <span>Sign:</span> {item.label || item.word || 'N/A'}
                      </p>
                    </article>
                  );
                })}
              </div>
            </>
          ) : (
            <div className="empty-state">
              <div className="empty-illustration" aria-hidden="true">
                <span>文</span>
                <span className="illustration-arrow">→</span>
                <span>✋</span>
              </div>
              <h3>Your signs will appear here</h3>
              <p>
                Enter an English message and select Translate to Sign
                to view available recorded videos.
              </p>
            </div>
          )}

          {availableWords.length > 0 && (
            <div className="available-signs">
              <p className="section-label">WORDS IN THESE RESULTS</p>
              <div className="phrase-list">
                {availableWords.map((word) => (
                  <span className="result-chip" key={word}>
                    {word}
                  </span>
                ))}
              </div>
            </div>
          )}
        </section>

        <aside className="panel history-panel">
          <div className="panel-heading">
            <div>
              <p className="section-label">RECENT ACTIVITY</p>
              <h2>Recent messages</h2>
            </div>
            <span className="heading-icon" aria-hidden="true">↺</span>
          </div>

          {history.length > 0 ? (
            <div className="history-list">
              {history.map((item) => (
                <button
                  type="button"
                  key={item.id}
                  className={`history-item ${
                    selectedHistory === item.id ? 'history-item-active' : ''
                  }`}
                  onClick={() => loadHistory(item)}
                >
                  <span className="history-icon" aria-hidden="true">Aa</span>
                  <span className="history-content">
                    <strong>{item.text}</strong>
                    <small>
                      {item.results.length} sign result
                      {item.results.length === 1 ? '' : 's'}
                    </small>
                  </span>
                  <span className="history-arrow" aria-hidden="true">›</span>
                </button>
              ))}
            </div>
          ) : (
            <div className="history-empty">
              <span aria-hidden="true">◷</span>
              <p>Your recent translations will appear here.</p>
            </div>
          )}

          <div className="history-note">
            <span aria-hidden="true">ⓘ</span>
            <p>
              Recent messages are kept in this page while it remains open.
              They are not saved to a database.
            </p>
          </div>
        </aside>
      </section>

      {/* AI SIGN ANIMATOR SECTION */}
      <section className="panel avatar-section" ref={avatarRef} id="avatar-section">
        <div className="panel-heading">
          <div>
            <p className="section-label">STEP 03</p>
            <h2>AI Sign Language Animation</h2>
          </div>
          <span className="heading-icon" aria-hidden="true">✋</span>
        </div>

        <p className="page-description" style={{ marginBottom: 18 }}>
          Each word is animated by a canvas-based avatar using predefined
          SLSL keyframe poses. Use the controls to play, pause, and step
          through each sign in your sentence.
        </p>

        <SignAnimatorPanel signs={results} />
      </section>

      <footer className="app-footer">
        <p>
          Smart Sri Lankan Sign Language Recognition and Communication System
        </p>
        <span>Research prototype</span>
      </footer>
    </main>
  );
}
