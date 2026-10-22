
import React, { useRef, useEffect, useState, useCallback } from 'react';

const PlayIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
    <path d="M8 5v14l11-7z" />
  </svg>
);

const PauseIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
    <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z" />
  </svg>
);

const PrevIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
    <path d="M6 6h2v12H6zm3.5 6l8.5 6V6z" />
  </svg>
);

const NextIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
    <path d="M6 18l8.5-6L6 6v12zm10-12h2v12h-2z" />
  </svg>
);

const ReplayIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
    <path d="M12 5V1L7 6l5 5V7c3.31 0 6 2.69 6 6s-2.69 6-6 6-6-2.69-6-6H4c0 4.42 3.58 8 8 8s8-3.58 8-8-3.58-8-8-8z" />
  </svg>
);

export default function SignPlayer({ sequence }) {
  const videoRef = useRef(null);

  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const total = sequence?.length ?? 0;
  const current = sequence?.[currentIndex];

  // Reset the player when a new translation arrives.
  useEffect(() => {
    setCurrentIndex(0);
    setIsPlaying(false);
    setIsLoading(false);
  }, [sequence]);

  // Find the next available video, skipping missing sign videos.
  const findAvailableIndex = useCallback((startIndex, direction = 1) => {
    if (!sequence?.length) return -1;

    for (
      let i = startIndex;
      i >= 0 && i < sequence.length;
      i += direction
    ) {
      if (sequence[i]?.available && sequence[i]?.video_url) {
        return i;
      }
    }

    return -1;
  }, [sequence]);

  // When a new video becomes available, start it if playback is active.
  const handleCanPlay = () => {
    setIsLoading(false);

    if (isPlaying && videoRef.current) {
      videoRef.current.play().catch(() => {
        setIsPlaying(false);
      });
    }
  };

  // Automatically move to the next available sign when a video ends.
  const handleVideoEnded = useCallback(() => {
    const nextIndex = findAvailableIndex(currentIndex + 1);

    if (nextIndex !== -1) {
      setCurrentIndex(nextIndex);
      // Keep isPlaying true so the next video starts automatically.
    } else {
      setIsPlaying(false);
      setIsLoading(false);
    }
  }, [currentIndex, findAvailableIndex]);

  // Start or pause the complete sequence.
  const togglePlay = () => {
    if (isPlaying) {
      videoRef.current?.pause();
      setIsPlaying(false);
      return;
    }

    // If the current sign is unavailable, find the next available one.
    if (!current?.available || !current?.video_url) {
      const nextIndex = findAvailableIndex(currentIndex);

      if (nextIndex === -1) {
        setIsPlaying(false);
        return;
      }

      if (nextIndex !== currentIndex) {
        setCurrentIndex(nextIndex);
      }
    }

    setIsPlaying(true);
  };

  // Replay the complete sentence from its first available sign.
  const replaySequence = () => {
    const firstIndex = findAvailableIndex(0);

    if (firstIndex === -1) return;

    setCurrentIndex(firstIndex);
    setIsPlaying(true);
  };

  // Selecting a sign manually pauses automatic sequence playback.
  const goTo = (index) => {
    if (index < 0 || index >= total) return;

    videoRef.current?.pause();
    setCurrentIndex(index);
    setIsPlaying(false);
    setIsLoading(false);
  };

  // Pause the video immediately when playback is switched off.
  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    if (!isPlaying) {
      video.pause();
    }
  }, [isPlaying]);

  if (!total) {
    return (
      <div className="glass-card" style={{ padding: 40, textAlign: 'center' }}>
        <div style={{ fontSize: '3rem', marginBottom: 12 }}>🤟</div>
        <p>Enter text above and press Translate to Sign.</p>
      </div>
    );
  }

  const progress = ((currentIndex + 1) / total) * 100;

  return (
    <div className="glass-card fade-up" style={{ padding: 20 }}>
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          marginBottom: 14,
        }}
      >
        <span className="section-label">Sign Sequence Player</span>
        <span style={{ color: 'var(--text-muted)', fontSize: '0.82rem' }}>
          {currentIndex + 1} / {total}
        </span>
      </div>

      <div className="progress-bar" style={{ marginBottom: 16 }}>
        <div
          className="progress-bar-fill"
          style={{ width: `${progress}%` }}
        />
      </div>

      <div style={{ textAlign: 'center', marginBottom: 14 }}>
        <h3 style={{ fontSize: '1.3rem', fontWeight: 700 }}>
          {current?.label ?? 'Sign video'}
        </h3>
        <span className="badge badge-success">
          {current?.available ? '✓ Video ready' : 'Video unavailable'}
        </span>
      </div>

      {current?.available && current?.video_url ? (
        <div style={{ position: 'relative' }}>
          {isLoading && (
            <div
              style={{
                position: 'absolute',
                inset: 0,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                background: 'rgba(0,0,0,0.45)',
                zIndex: 1,
                borderRadius: 'var(--radius-md)',
              }}
            >
              <div className="spinner" />
            </div>
          )}

          <video
            key={current.video_url}
            ref={videoRef}
            className="sign-video"
            src={current.video_url}
            onEnded={handleVideoEnded}
            onWaiting={() => setIsLoading(true)}
            onCanPlay={handleCanPlay}
            onLoadStart={() => setIsLoading(true)}
            onError={() => setIsLoading(false)}
            playsInline
            preload="auto"
            controls
            controlsList="nodownload"
            style={{
              width: '100%',
              display: 'block',
              borderRadius: 'var(--radius-md)',
            }}
          />
        </div>
      ) : (
        <div className="alert alert-warning">
          ⚠️ {current?.message ?? 'This sign video is not available.'}
        </div>
      )}

      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 10,
          marginTop: 16,
        }}
      >
        <button
          className="btn btn-ghost btn-icon"
          onClick={() => goTo(findAvailableIndex(currentIndex - 1, -1))}
          disabled={findAvailableIndex(currentIndex - 1, -1) === -1}
          aria-label="Previous sign"
          title="Previous sign"
        >
          <PrevIcon />
        </button>

        <button
          className="btn btn-primary btn-icon-lg"
          onClick={togglePlay}
          disabled={findAvailableIndex(currentIndex) === -1}
          aria-label={isPlaying ? 'Pause sequence' : 'Play sequence'}
          title={isPlaying ? 'Pause sequence' : 'Play sequence'}
        >
          {isPlaying ? <PauseIcon /> : <PlayIcon />}
        </button>

        <button
          className="btn btn-ghost btn-icon"
          onClick={replaySequence}
          disabled={findAvailableIndex(0) === -1}
          aria-label="Replay complete sequence"
          title="Replay entire sentence"
        >
          <ReplayIcon />
        </button>

        <button
          className="btn btn-ghost btn-icon"
          onClick={() => goTo(findAvailableIndex(currentIndex + 1))}
          disabled={findAvailableIndex(currentIndex + 1) === -1}
          aria-label="Next sign"
          title="Next sign"
        >
          <NextIcon />
        </button>
      </div>

      <p
        style={{
          textAlign: 'center',
          color: 'var(--text-muted)',
          fontSize: '0.85rem',
          marginTop: 12,
        }}
      >
        Press Play once to watch the complete sign sequence.
      </p>

      {total > 1 && (
        <div
          className="chip-list"
          style={{ marginTop: 16, justifyContent: 'center' }}
        >
          {sequence.map((item, idx) => (
            <button
              key={`${item.sign_id ?? item.label}-${idx}`}
              className={`chip${idx === currentIndex ? ' active' : ''}`}
              onClick={() => goTo(idx)}
              title={item.label}
            >
              {item.label}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
