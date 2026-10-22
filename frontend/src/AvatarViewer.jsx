/**
 * AvatarViewer.jsx  —  Sri Lankan Sign Language 3D Avatar
 *
 * Loads MediaPipe Holistic keypoint JSON and drives a GLB avatar's
 * bones to reproduce the sign.  Camera is framed to show only the
 * upper body (chest, arms, hands, face) — the important parts for
 * sign language.
 *
 * Motion JSON served from /water_motion.json (Vite public/) so there
 * is no CORS issue.  Production can pass a custom motionUrl prop.
 */

import React, { useEffect, useMemo, useRef, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, useGLTF } from '@react-three/drei';
import * as THREE from 'three';

// ─────────────────────────────────────────────
// Constants
// ─────────────────────────────────────────────

/** Served directly by Vite (no CORS) */
const DEFAULT_MOTION_URL = '/water_motion.json';

/** GLB model in public/assets/models/ */
const MODEL_URL = '/assets/models/male-base-mesh-base_male.glb';

const FPS = 15;

// MediaPipe Pose indices we care about
const P = {
  lShoulder: 11, rShoulder: 12,
  lElbow: 13, rElbow: 14,
  lWrist: 15, rWrist: 16,
  lHip: 23, rHip: 24,
};

// MediaPipe Hand indices
const H = {
  wrist: 0,
  thumbCmc: 1, thumbMcp: 2, thumbIp: 3, thumbTip: 4,
  indexMcp: 5, indexPip: 6, indexDip: 7, indexTip: 8,
  midMcp: 9, midPip: 10, midDip: 11, midTip: 12,
  ringMcp: 13, ringPip: 14, ringDip: 15, ringTip: 16,
  pinkyMcp: 17, pinkyPip: 18, pinkyDip: 19, pinkyTip: 20,
};

// ─────────────────────────────────────────────
// Bone name helpers
// ─────────────────────────────────────────────

/**
 * Try every candidate name (case-insensitive) against the bone map.
 * Returns the first match or null, and logs a warning if nothing matches.
 */
function findBone(boneMap, candidates, label) {
  for (const name of candidates) {
    // exact key
    if (boneMap[name]) return boneMap[name];
    // case-insensitive fallback
    const lo = name.toLowerCase();
    const hit = Object.values(boneMap).find(b => b.name.toLowerCase() === lo);
    if (hit) return hit;
  }
  console.warn(`[Avatar] bone "${label}" not found. Tried: ${candidates.join(', ')}`);
  return null;
}

/**
 * Build a structured map from the flat boneMap dict.
 * Each slot tries several naming conventions used by
 * Mixamo, Blender, and generic rigs.
 */
function buildRig(boneMap) {
  const F = (candidates, label) => findBone(boneMap, candidates, label);
  return {
    // Spine
    spine: F(['Spine', 'spine', 'spine01', 'Spine1', 'spine1'], 'spine'),
    chest: F(['Spine1', 'spine02', 'spine2', 'Chest', 'chest', 'Spine2'], 'chest'),
    neck: F(['Neck', 'neck'], 'neck'),
    head: F(['Head', 'head'], 'head'),

    // Left arm
    lUpper: F(['LeftArm', 'upperarm_l', 'upperarm.L', 'upperarm01L', 'Left_arm'], 'lUpper'),
    lLower: F(['LeftForeArm', 'forearm_l', 'lowerarm.L', 'lowerarm01L', 'Left_forearm'], 'lLower'),
    lWrist: F(['LeftHand', 'wrist_l', 'wrist.L', 'wristL', 'Left_wrist'], 'lWrist'),

    // Right arm
    rUpper: F(['RightArm', 'upperarm_r', 'upperarm.R', 'upperarm01R', 'Right_arm'], 'rUpper'),
    rLower: F(['RightForeArm', 'forearm_r', 'lowerarm.R', 'lowerarm01R', 'Right_forearm'], 'rLower'),
    rWrist: F(['RightHand', 'wrist_r', 'wrist.R', 'wristR', 'Right_wrist'], 'rWrist'),

    // ── RIGHT HAND FINGERS ──────────────────────
    // Thumb
    rThumb1: F(['RightHandThumb1', 'thumb_01_r', 'thumb01R', 'r_thumb_01', 'f_thumb01R'], 'rThumb1'),
    rThumb2: F(['RightHandThumb2', 'thumb_02_r', 'thumb02R', 'r_thumb_02', 'f_thumb02R'], 'rThumb2'),
    rThumb3: F(['RightHandThumb3', 'thumb_03_r', 'thumb03R', 'r_thumb_03', 'f_thumb03R'], 'rThumb3'),
    // Index
    rIndex1: F(['RightHandIndex1', 'index_01_r', 'f_index01R', 'r_index_01'], 'rIndex1'),
    rIndex2: F(['RightHandIndex2', 'index_02_r', 'f_index02R', 'r_index_02'], 'rIndex2'),
    rIndex3: F(['RightHandIndex3', 'index_03_r', 'f_index03R', 'r_index_03'], 'rIndex3'),
    // Middle
    rMid1: F(['RightHandMiddle1', 'middle_01_r', 'f_middle01R', 'r_middle_01'], 'rMid1'),
    rMid2: F(['RightHandMiddle2', 'middle_02_r', 'f_middle02R', 'r_middle_02'], 'rMid2'),
    rMid3: F(['RightHandMiddle3', 'middle_03_r', 'f_middle03R', 'r_middle_03'], 'rMid3'),
    // Ring
    rRing1: F(['RightHandRing1', 'ring_01_r', 'f_ring01R', 'r_ring_01'], 'rRing1'),
    rRing2: F(['RightHandRing2', 'ring_02_r', 'f_ring02R', 'r_ring_02'], 'rRing2'),
    rRing3: F(['RightHandRing3', 'ring_03_r', 'f_ring03R', 'r_ring_03'], 'rRing3'),
    // Pinky
    rPinky1: F(['RightHandPinky1', 'pinky_01_r', 'f_pinky01R', 'r_pinky_01'], 'rPinky1'),
    rPinky2: F(['RightHandPinky2', 'pinky_02_r', 'f_pinky02R', 'r_pinky_02'], 'rPinky2'),
    rPinky3: F(['RightHandPinky3', 'pinky_03_r', 'f_pinky03R', 'r_pinky_03'], 'rPinky3'),

    // ── LEFT HAND FINGERS ───────────────────────
    lThumb1: F(['LeftHandThumb1', 'thumb_01_l', 'thumb01L', 'l_thumb_01', 'f_thumb01L'], 'lThumb1'),
    lThumb2: F(['LeftHandThumb2', 'thumb_02_l', 'thumb02L', 'l_thumb_02', 'f_thumb02L'], 'lThumb2'),
    lThumb3: F(['LeftHandThumb3', 'thumb_03_l', 'thumb03L', 'l_thumb_03', 'f_thumb03L'], 'lThumb3'),
    lIndex1: F(['LeftHandIndex1', 'index_01_l', 'f_index01L', 'l_index_01'], 'lIndex1'),
    lIndex2: F(['LeftHandIndex2', 'index_02_l', 'f_index02L', 'l_index_02'], 'lIndex2'),
    lIndex3: F(['LeftHandIndex3', 'index_03_l', 'f_index03L', 'l_index_03'], 'lIndex3'),
    lMid1: F(['LeftHandMiddle1', 'middle_01_l', 'f_middle01L', 'l_middle_01'], 'lMid1'),
    lMid2: F(['LeftHandMiddle2', 'middle_02_l', 'f_middle02L', 'l_middle_02'], 'lMid2'),
    lMid3: F(['LeftHandMiddle3', 'middle_03_l', 'f_middle03L', 'l_middle_03'], 'lMid3'),
    lRing1: F(['LeftHandRing1', 'ring_01_l', 'f_ring01L', 'l_ring_01'], 'lRing1'),
    lRing2: F(['LeftHandRing2', 'ring_02_l', 'f_ring02L', 'l_ring_02'], 'lRing2'),
    lRing3: F(['LeftHandRing3', 'ring_03_l', 'f_ring03L', 'l_ring_03'], 'lRing3'),
    lPinky1: F(['LeftHandPinky1', 'pinky_01_l', 'f_pinky01L', 'l_pinky_01'], 'lPinky1'),
    lPinky2: F(['LeftHandPinky2', 'pinky_02_l', 'f_pinky02L', 'l_pinky_02'], 'lPinky2'),
    lPinky3: F(['LeftHandPinky3', 'pinky_03_l', 'f_pinky03L', 'l_pinky_03'], 'lPinky3'),
  };
}

// ─────────────────────────────────────────────
// Math helpers
// ─────────────────────────────────────────────

/** Return landmark or null if invisible / invalid */
function lm(arr, idx) {
  if (!Array.isArray(arr)) return null;
  const p = arr[idx];
  if (!p || !Number.isFinite(p.x) || !Number.isFinite(p.y)) return null;
  if (typeof p.visibility === 'number' && p.visibility < 0.3) return null;
  return p;
}

/** Clamp to [-limit, limit] then wrap into [-π, π] */
function clampedAngle(raw, limit) {
  const c = THREE.MathUtils.clamp(raw, -limit, limit);
  return Math.atan2(Math.sin(c), Math.cos(c));
}

/**
 * Angle of vector (a→b) in image space.
 * MediaPipe Y grows downward, so we negate Y to get a standard
 * math-convention angle.
 */
function vecAngle(a, b) {
  return Math.atan2(-(b.y - a.y), b.x - a.x);
}

/**
 * Compute the bend at joint `mid` using vectors (prox→mid) and (mid→dist).
 * Returns value in [0, π] — 0 = straight, π = fully bent.
 */
function bendAngle(prox, mid, dist) {
  if (!prox || !mid || !dist) return 0;
  const ax = mid.x - prox.x, ay = mid.y - prox.y;
  const bx = dist.x - mid.x, by = dist.y - mid.y;
  const la = Math.hypot(ax, ay), lb = Math.hypot(bx, by);
  if (la < 0.005 || lb < 0.005) return 0;
  const dot = (ax * bx + ay * by) / (la * lb);
  return Math.acos(THREE.MathUtils.clamp(dot, -1, 1));
}

// ─────────────────────────────────────────────
// AvatarModel (three.js object inside Canvas)
// ─────────────────────────────────────────────

function AvatarModel({ frameRef, rigRef, baseRef, logBones }) {
  const { scene } = useGLTF(MODEL_URL);

  // Flat bone dictionary  { boneName: Bone }
  const boneMap = useMemo(() => {
    const m = {};
    scene.traverse(o => { if (o.isBone) m[o.name] = o; });
    return m;
  }, [scene]);

  // Initialise rig + rest rotations once the model loads
  useEffect(() => {
    const base = {};
    Object.values(boneMap).forEach(b => { base[b.name] = b.rotation.clone(); });
    baseRef.current = base;
    rigRef.current = buildRig(boneMap);

    if (logBones) {
      console.group('[AvatarViewer] All bone names in this GLB:');
      console.log(Object.keys(boneMap).sort().join('\n'));
      console.groupEnd();
      console.group('[AvatarViewer] Resolved rig slots:');
      const report = {};
      Object.entries(rigRef.current).forEach(([k, v]) => {
        report[k] = v ? `✅  ${v.name}` : '❌  NOT FOUND';
      });
      console.table(report);
      console.groupEnd();
    }
  }, [boneMap, rigRef, baseRef, logBones]);

  // Animation loop — runs every rendered frame
  useFrame(() => {
    const frame = frameRef.current;
    const base = baseRef.current;
    const rig = rigRef.current;
    if (!base || !rig) return;

    // Reset all bones to rest pose each frame
    Object.values(boneMap).forEach(b => {
      const r = base[b.name];
      if (r) b.rotation.copy(r);
    });

    if (!frame) return;

    const pose = frame.pose ?? null;
    const rHand = frame.right_hand ?? null;
    const lHand = frame.left_hand ?? null;

    // ── 1. SPINE LATERAL LEAN ──────────────────
    if (pose && rig.spine) {
      const ls = lm(pose, P.lShoulder), rs = lm(pose, P.rShoulder);
      const lh = lm(pose, P.lHip), rh = lm(pose, P.rHip);
      if (ls && rs && lh && rh) {
        const smx = (ls.x + rs.x) / 2;
        const hmx = (lh.x + rh.x) / 2;
        const lean = THREE.MathUtils.clamp((smx - hmx) * 1.2, -0.2, 0.2);
        rig.spine.rotation.z = base[rig.spine.name].z + lean;
      }
    }

    // ── 2. ARM ANIMATION ───────────────────────
    function applyArm(shoulderIdx, elbowIdx, wristIdx, upper, lower, wristBone, sign) {
      if (!upper || !lower || !pose) return;
      const S = lm(pose, shoulderIdx);
      const E = lm(pose, elbowIdx);
      const W = lm(pose, wristIdx);
      if (!S || !E) return;

      const bU = base[upper.name];
      const bL = base[lower.name];
      if (!bU || !bL) return;

      // Upper arm: angle from shoulder to elbow
      // +Math.PI/2 aligns image-space angle to bone's rest direction
      const upperAngle = vecAngle(S, E);
      upper.rotation.z = bU.z + sign * clampedAngle(upperAngle + Math.PI / 2, Math.PI * 0.65);

      // Forward/back from Z depth
      if (Number.isFinite(E.z) && Number.isFinite(S.z)) {
        upper.rotation.x = bU.x + THREE.MathUtils.clamp((E.z - S.z) * 1.5, -0.45, 0.45);
      }

      // Forearm: relative angle from upper-arm segment
      if (W) {
        const upperDir = vecAngle(S, E);
        const lowerDir = vecAngle(E, W);
        const rel = lowerDir - upperDir;
        lower.rotation.z = bL.z + sign * clampedAngle(rel, Math.PI * 0.9);
      }

      // Wrist slight rotation
      if (wristBone && W && E) {
        const bW = base[wristBone.name];
        if (bW) {
          const wAngle = vecAngle(E, W);
          wristBone.rotation.z = bW.z + sign * clampedAngle(wAngle * 0.35, 0.4);
        }
      }
    }

    applyArm(P.lShoulder, P.lElbow, P.lWrist, rig.lUpper, rig.lLower, rig.lWrist, 1);
    applyArm(P.rShoulder, P.rElbow, P.rWrist, rig.rUpper, rig.rLower, rig.rWrist, -1);

    // ── 3. FINGER ANIMATION ────────────────────
    /**
     * @param {Array}  hand  21 MediaPipe hand landmarks
     * @param {string} side  'r' | 'l'
     * @param {number} sign  +1 for right hand, -1 for left
     */
    function applyHand(hand, side, sign) {
      if (!hand || hand.length < 21) return;

      const fingers = [
        // [b1 slot, b2 slot, b3 slot,  prox idx, mid1 idx, mid2 idx, tip idx]
        [`${side}Thumb1`, `${side}Thumb2`, `${side}Thumb3`,
        H.thumbCmc, H.thumbMcp, H.thumbIp, H.thumbTip],
        [`${side}Index1`, `${side}Index2`, `${side}Index3`,
        H.indexMcp, H.indexMcp, H.indexPip, H.indexTip],
        [`${side}Mid1`, `${side}Mid2`, `${side}Mid3`,
        H.midMcp, H.midMcp, H.midPip, H.midTip],
        [`${side}Ring1`, `${side}Ring2`, `${side}Ring3`,
        H.ringMcp, H.ringMcp, H.ringPip, H.ringTip],
        [`${side}Pinky1`, `${side}Pinky2`, `${side}Pinky3`,
        H.pinkyMcp, H.pinkyMcp, H.pinkyPip, H.pinkyTip],
      ];

      fingers.forEach(([s1, s2, s3, i0, i1, i2, i3]) => {
        const b1 = rig[s1], b2 = rig[s2], b3 = rig[s3];
        const p0 = hand[i0], p1 = hand[i1], p2 = hand[i2], p3 = hand[i3];

        const curl1 = bendAngle(p0, p1, p2);  // mcp bend
        const curl2 = bendAngle(p1, p2, p3);  // pip bend

        if (b1 && base[b1.name]) b1.rotation.x = base[b1.name].x + sign * curl1 * 0.75;
        if (b2 && base[b2.name]) b2.rotation.x = base[b2.name].x + sign * curl1 * 0.55;
        if (b3 && base[b3.name]) b3.rotation.x = base[b3.name].x + sign * curl2 * 0.9;
      });
    }

    applyHand(rHand, 'r', 1);
    applyHand(lHand, 'l', -1);
  });

  return <primitive object={scene} />;
}

// ─────────────────────────────────────────────
// Main exported component
// ─────────────────────────────────────────────

/**
 * AvatarViewer
 *
 * Props
 * ─────
 * motionUrl {string|undefined}  URL of the motion JSON.  When undefined the
 *                               component shows an invitation to select a sign.
 * signLabel {string}            Label shown in the header.
 * autoPlay  {boolean}           Start playback on mount.  Defaults to false
 */
export default function AvatarViewer({
  motionUrl = undefined,
  signLabel = 'Select a sign',
  autoPlay = false,
}) {
  const [frames, setFrames] = useState([]);
  const [idx, setIdx] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [logBones, setLogBones] = useState(false);

  // Shared refs for the animation loop
  const frameRef = useRef(null);
  const rigRef = useRef(null);
  const baseRef = useRef(null);

  // Keep frameRef in sync
  useEffect(() => { frameRef.current = frames[idx] ?? null; }, [frames, idx]);

  // ── Load motion JSON ──────────────────────
  useEffect(() => {
    // No URL supplied → show empty state
    if (!motionUrl) {
      setFrames([]);
      setIdx(0);
      setPlaying(false);
      setLoading(false);
      setError('');
      return;
    }

    let alive = true;
    setLoading(true);
    setError('');
    setFrames([]);
    setIdx(0);
    setPlaying(false);

    fetch(motionUrl)
      .then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status} — ${r.url}`);
        return r.json();
      })
      .then(data => {
        if (!alive) return;
        if (!Array.isArray(data)) throw new Error('Motion file is not an array of frames');
        setFrames(data);
        if (autoPlay) setPlaying(true);
      })
      .catch(err => {
        if (alive) setError(err.message);
      })
      .finally(() => {
        if (alive) setLoading(false);
      });

    return () => { alive = false; };
  }, [motionUrl, autoPlay]);

  // ── Playback timer ────────────────────────
  useEffect(() => {
    if (!playing || frames.length === 0) return;
    const timer = setInterval(() => {
      setIdx(i => {
        if (i >= frames.length - 1) { setPlaying(false); return 0; }
        return i + 1;
      });
    }, 1000 / FPS);
    return () => clearInterval(timer);
  }, [playing, frames.length]);

  // ── Derived state ─────────────────────────
  const frame = frames[idx] ?? null;
  const hasRH = frame?.right_hand?.length === 21;
  const hasLH = frame?.left_hand?.length === 21;
  const hasFace = (frame?.face?.length ?? 0) > 10;
  const pct = frames.length > 1 ? (idx / (frames.length - 1)) * 100 : 0;

  // ── Empty / no-selection state ─────────────
  if (!motionUrl && !loading) {
    return (
      <div style={S.card}>
        <div style={S.header}>
          <div>
            <p style={S.eyebrow}>SIGN LANGUAGE AVATAR</p>
            <h2 style={S.title}>🤟 {signLabel}</h2>
          </div>
        </div>
        <div style={{
          display: 'flex', flexDirection: 'column',
          alignItems: 'center', justifyContent: 'center',
          minHeight: 320, gap: 16, opacity: 0.7,
        }}>
          <div style={{ fontSize: 56 }}>🤟</div>
          <p style={{ color: '#94a3b8', fontSize: 14, textAlign: 'center', maxWidth: 300 }}>
            Click <strong style={{ color: '#8b5cf6' }}>Animate Avatar</strong> on any sign card above
            to see the 3D avatar perform that sign.
          </p>
        </div>
      </div>
    );
  }

  return (

    <div style={S.card}>
      {/* ── Header ── */}
      <div style={S.header}>
        <div>
          <p style={S.eyebrow}>SIGN LANGUAGE AVATAR</p>
          <h2 style={S.title}>🤟 {signLabel}</h2>
        </div>

        {/* Landmark availability badges */}
        <div style={S.badges}>
          {hasRH && <Badge color="#a78bfa" bg="rgba(139,92,246,.18)">✋ R-hand</Badge>}
          {hasLH && <Badge color="#38bdf8" bg="rgba(56,189,248,.18)">✋ L-hand</Badge>}
          {hasFace && <Badge color="#10b981" bg="rgba(16,185,129,.18)">😊 Face</Badge>}
        </div>
      </div>

      {/* ── Error ── */}
      {error && (
        <div style={S.errorBox} role="alert">
          ⚠️ {error}
        </div>
      )}

      {/* ── 3-D Canvas (upper body framing) ── */}
      <div style={S.canvasWrap}>
        {loading && (
          <div style={S.overlay}>
            <div style={S.spinner} />
            <p style={{ color: '#94a3b8', marginTop: 12, fontSize: 13 }}>
              Loading motion data…
            </p>
          </div>
        )}

        <Canvas
          camera={{
            /* Upper-body frame:
               position is slightly above belt, 2 units away.
               fov 38° keeps perspective natural without distortion. */
            position: [0, 1.55, 2.2],
            fov: 38,
            near: 0.1,
            far: 20,
          }}
          style={{ width: '100%', height: '100%' }}
        >
          {/* 3-point lighting */}
          <ambientLight intensity={0.9} />
          <directionalLight position={[1.5, 3, 3]} intensity={2.2} />
          <directionalLight position={[-2, 1, -2]} intensity={0.7} color="#b0c4ff" />
          <pointLight position={[0, 2, 1.5]} intensity={0.5} color="#8b5cf6" />

          {/* Subtle floor for visual grounding */}
          <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.01, 0]}>
            <planeGeometry args={[10, 10]} />
            <meshStandardMaterial color="#0d1220" />
          </mesh>

          {/* Avatar */}
          {!loading && !error && (
            <AvatarModel
              frameRef={frameRef}
              rigRef={rigRef}
              baseRef={baseRef}
              logBones={logBones}
            />
          )}

          {/*
            OrbitControls locked to upper-body area.
            Target y=1.4 ≈ mid-chest / shoulder height.
            Users can orbit to inspect hands from any angle.
          */}
          <OrbitControls
            target={[0, 1.4, 0]}
            enablePan={false}
            minDistance={0.8}
            maxDistance={4}
            minPolarAngle={0.2}
            maxPolarAngle={Math.PI * 0.6}
          />
        </Canvas>

        {/* Hand active indicators (overlay) */}
        <div style={S.handBadges}>
          <span style={{ opacity: hasRH ? 1 : 0.2 }} title="Right hand">🖐</span>
          <span style={{ opacity: hasLH ? 1 : 0.2 }} title="Left hand" >🤚</span>
          {hasFace && <span title="Face data">😊</span>}
        </div>
      </div>

      {/* ── Progress bar ── */}
      <div style={S.progressRow}>
        <span style={S.frameCount}>
          {frames.length ? idx + 1 : 0} / {frames.length}
        </span>
        <div style={S.progressTrack}>
          <div style={{ ...S.progressFill, width: `${pct}%` }} />
        </div>
      </div>

      {/* ── Scrubber ── */}
      <input
        type="range"
        min={0}
        max={Math.max(0, frames.length - 1)}
        value={idx}
        onChange={e => { setPlaying(false); setIdx(+e.target.value); }}
        style={{ width: '100%', marginBottom: 14, accentColor: '#8b5cf6' }}
        disabled={!frames.length}
        aria-label="Frame scrubber"
      />

      {/* ── Playback controls ── */}
      <div style={S.controls}>
        <Btn ghost onClick={() => { setPlaying(false); setIdx(0); }} title="Rewind">⏮</Btn>
        <Btn ghost onClick={() => setIdx(i => Math.max(0, i - 1))} disabled={idx === 0} title="Prev frame">‹</Btn>

        <Btn
          primary
          onClick={() => setPlaying(v => !v)}
          disabled={!frames.length}
          aria-label={playing ? 'Pause' : 'Play'}
        >
          {playing ? '⏸  Pause' : '▶  Play Sign'}
        </Btn>

        <Btn ghost onClick={() => setIdx(i => Math.min(frames.length - 1, i + 1))} disabled={idx >= frames.length - 1} title="Next frame">›</Btn>
        <Btn ghost onClick={() => { setIdx(0); setPlaying(true); }} disabled={!frames.length} title="Replay">↺</Btn>
      </div>

      {/* ── Debug ── */}
      <div style={S.debugRow}>
        <Btn
          small
          onClick={() => { setLogBones(true); setTimeout(() => setLogBones(false), 200); }}
          title="Print bone names to browser console (F12)"
        >
          🦴 Log Bones
        </Btn>
        <span style={S.hint}>Drag to orbit · Scroll to zoom</span>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────
// Tiny sub-components
// ─────────────────────────────────────────────

function Badge({ color, bg, children }) {
  return (
    <span style={{
      padding: '3px 10px', borderRadius: 999,
      fontSize: 11, fontWeight: 600,
      color, background: bg,
    }}>
      {children}
    </span>
  );
}

function Btn({ primary, ghost, small, children, ...props }) {
  let base = {
    display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
    border: 'none', cursor: 'pointer', fontFamily: 'inherit',
    transition: 'all .15s',
  };
  if (primary) Object.assign(base, {
    padding: '10px 24px', borderRadius: 10, fontSize: 14, fontWeight: 700,
    background: 'linear-gradient(135deg, #8b5cf6, #6d28d9)', color: '#fff',
    boxShadow: '0 2px 12px rgba(139,92,246,.35)',
  });
  if (ghost) Object.assign(base, {
    width: 40, height: 40, borderRadius: 8, fontSize: 18,
    background: 'rgba(255,255,255,.04)', color: '#94a3b8',
    border: '1px solid rgba(255,255,255,.1)',
  });
  if (small) Object.assign(base, {
    padding: '5px 12px', borderRadius: 7, fontSize: 11, fontWeight: 600,
    background: 'rgba(255,255,255,.05)', color: '#64748b',
    border: '1px solid rgba(255,255,255,.1)',
  });
  if (props.disabled) base.opacity = 0.4;
  return <button style={base} {...props}>{children}</button>;
}

// ─────────────────────────────────────────────
// Styles
// ─────────────────────────────────────────────

const S = {
  card: {
    width: '100%',
    padding: 20,
    background: 'rgba(11,17,28,.9)',
    border: '1px solid rgba(139,92,246,.22)',
    borderRadius: 18,
    backdropFilter: 'blur(14px)',
  },
  header: {
    display: 'flex', alignItems: 'flex-start',
    justifyContent: 'space-between', flexWrap: 'wrap',
    gap: 10, marginBottom: 16,
  },
  eyebrow: {
    fontSize: 10, fontWeight: 800, letterSpacing: '.1em',
    color: '#64748b', textTransform: 'uppercase', marginBottom: 4,
  },
  title: {
    fontSize: 20, fontWeight: 700, color: '#f1f5f9', letterSpacing: '-.02em',
  },
  badges: { display: 'flex', gap: 6, flexWrap: 'wrap' },
  errorBox: {
    padding: '10px 14px', marginBottom: 14,
    background: 'rgba(239,68,68,.1)', border: '1px solid rgba(239,68,68,.3)',
    borderRadius: 10, color: '#f87171', fontSize: 13,
  },
  canvasWrap: {
    position: 'relative', width: '100%',
    /* Taller canvas so the upper body has room, no legs needed */
    height: 480,
    borderRadius: 12, overflow: 'hidden',
    background: 'linear-gradient(170deg, #08101e 0%, #0f1827 100%)',
    border: '1px solid rgba(255,255,255,.06)',
    marginBottom: 14,
  },
  overlay: {
    position: 'absolute', inset: 0, zIndex: 10,
    display: 'flex', flexDirection: 'column',
    alignItems: 'center', justifyContent: 'center',
    background: 'rgba(8,16,30,.85)',
  },
  spinner: {
    width: 36, height: 36,
    border: '3px solid rgba(139,92,246,.2)',
    borderTopColor: '#8b5cf6',
    borderRadius: '50%',
    animation: 'spin .8s linear infinite',
  },
  handBadges: {
    position: 'absolute', top: 10, right: 12,
    fontSize: 22, display: 'flex', gap: 4,
    pointerEvents: 'none',
  },
  progressRow: {
    display: 'flex', alignItems: 'center', gap: 10, marginBottom: 8,
  },
  frameCount: {
    fontSize: 11, fontWeight: 600, color: '#64748b',
    minWidth: 56, whiteSpace: 'nowrap',
  },
  progressTrack: {
    flex: 1, height: 4, borderRadius: 99,
    background: 'rgba(255,255,255,.08)', overflow: 'hidden',
  },
  progressFill: {
    height: '100%', borderRadius: 99,
    background: 'linear-gradient(90deg, #8b5cf6, #38bdf8)',
    transition: 'width .1s linear',
  },
  controls: {
    display: 'flex', alignItems: 'center',
    justifyContent: 'center', gap: 8,
    flexWrap: 'wrap', marginBottom: 12,
  },
  debugRow: {
    display: 'flex', alignItems: 'center', gap: 8,
  },
  hint: {
    marginLeft: 'auto', color: '#475569',
    fontSize: 10, fontStyle: 'italic',
  },
};

// Preload the GLB model so it's ready before the user scrolls down
useGLTF.preload(MODEL_URL);
