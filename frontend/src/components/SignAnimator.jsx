/**
 * SignAnimator.jsx
 * ================
 * Canvas-based SLSL sign language animator.
 *
 * Replaces the MediaPipe-driven Three.js avatar with smooth, predefined
 * keyframe animations for each sign in the vocabulary.  Every sign is
 * defined as a set of (time, rightHand, leftHand, handShapes) keyframes;
 * the renderer interpolates between them with easing every frame using
 * requestAnimationFrame.
 *
 * Supports: I, you, mother, father, child, home, school, water, eat,
 *           drink, go, come, want, doctor, pain, today, tomorrow, + more.
 */

import React, {
  useEffect, useRef, useState, useCallback,
} from 'react';

// ─────────────────────────────────────────────────────────────────────────────
// CanvasRenderingContext2D.roundRect polyfill (Chrome < 99, Firefox < 112)
// ─────────────────────────────────────────────────────────────────────────────
if (typeof CanvasRenderingContext2D !== 'undefined' &&
    !CanvasRenderingContext2D.prototype.roundRect) {
  CanvasRenderingContext2D.prototype.roundRect = function(x, y, w, h, r) {
    const rx = Math.min(Array.isArray(r) ? r[0] : r, Math.abs(w) / 2, Math.abs(h) / 2);
    this.beginPath();
    this.moveTo(x + rx, y);
    this.lineTo(x + w - rx, y);
    this.quadraticCurveTo(x + w, y, x + w, y + rx);
    this.lineTo(x + w, y + h - rx);
    this.quadraticCurveTo(x + w, y + h, x + w - rx, y + h);
    this.lineTo(x + rx, y + h);
    this.quadraticCurveTo(x, y + h, x, y + h - rx);
    this.lineTo(x, y + rx);
    this.quadraticCurveTo(x, y, x + rx, y);
    this.closePath();
    return this;
  };
}

// ─────────────────────────────────────────────────────────────────────────────
// Canvas / figure constants
// ─────────────────────────────────────────────────────────────────────────────

const W = 400;
const H = 490;
const CX = 200;

// Body landmarks (canvas pixel coords)
const HD_CY = 78;   // head center Y
const HD_R  = 37;   // head radius
const NECK_TOP = HD_CY + HD_R;
const NECK_BOT = 135;
const RSH = [258, 148];   // right shoulder
const LSH = [142, 148];   // left shoulder
const RHP = [228, 292];   // right hip
const LHP = [172, 292];   // left hip

// ─────────────────────────────────────────────────────────────────────────────
// Easing & interpolation
// ─────────────────────────────────────────────────────────────────────────────

const easeInOut = t => -(Math.cos(Math.PI * t) - 1) / 2;
const lerp = (a, b, t) => a + (b - a) * t;
const lerpPt = ([ax, ay], [bx, by], t) => [lerp(ax, bx, t), lerp(ay, by, t)];

/** Interpolate between keyframes at normalised time t ∈ [0,1]. */
function samplePose(keyframes, t) {
  if (t <= keyframes[0].t) return keyframes[0];
  const last = keyframes[keyframes.length - 1];
  if (t >= last.t) return last;

  for (let i = 1; i < keyframes.length; i++) {
    const a = keyframes[i - 1];
    const b = keyframes[i];
    if (t <= b.t) {
      const local = (t - a.t) / (b.t - a.t);
      const e = easeInOut(local);
      return {
        t,
        rHand:  lerpPt(a.rHand,  b.rHand,  e),
        rElbow: lerpPt(a.rElbow, b.rElbow, e),
        rShape: local < 0.5 ? a.rShape : b.rShape,
        lHand:  lerpPt(a.lHand,  b.lHand,  e),
        lElbow: lerpPt(a.lElbow, b.lElbow, e),
        lShape: local < 0.5 ? a.lShape : b.lShape,
      };
    }
  }
  return last;
}

// ─────────────────────────────────────────────────────────────────────────────
// Keyframe database
// Format: { t, rElbow, rHand, rShape, lElbow, lHand, lShape }
// Positions are [x, y] canvas coords.
// ─────────────────────────────────────────────────────────────────────────────

// Shorthand
const kf = (t, re, rh, rs, le, lh, ls) =>
  ({ t, rElbow: re, rHand: rh, rShape: rs, lElbow: le, lHand: lh, lShape: ls });

// Rest (arms hanging at sides)
const REST_R_ELBOW = [280, 222]; const REST_R_HAND = [278, 328]; const REST_R_SHAPE = 'open';
const REST_L_ELBOW = [120, 222]; const REST_L_HAND = [122, 328]; const REST_L_SHAPE = 'open';

const SIGNS = {
  // ── PRONOUNS ──────────────────────────────────────────────────────────────
  S001: {                           // I / me — point index to chest
    label: 'I', duration: 1800,
    keyframes: [
      kf(0.0, [274,204], [205,193], 'point',   REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(0.4, [272,197], [204,184], 'point',   REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(0.7, [274,204], [205,193], 'point',   REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(1.0, [274,204], [205,193], 'point',   REST_L_ELBOW, REST_L_HAND, 'open'),
    ],
  },
  S002: {                           // you — point forward
    label: 'You', duration: 1800,
    keyframes: [
      kf(0.0, [278,202], [215,192], 'point',   REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(0.4, [282,200], [225,190], 'point',   REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(0.7, [278,202], [215,192], 'point',   REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(1.0, [278,202], [215,192], 'point',   REST_L_ELBOW, REST_L_HAND, 'open'),
    ],
  },
  // ── FAMILY ────────────────────────────────────────────────────────────────
  S003: {                           // mother — open-5 at chin, tap ×2
    label: 'Mother', duration: 2400,
    keyframes: [
      kf(0.0,  [292,200], [232,153], 'flat',   REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(0.25, [292,195], [232,147], 'flat',   REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(0.5,  [292,200], [232,154], 'flat',   REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(0.75, [292,195], [232,147], 'flat',   REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(1.0,  [292,200], [232,153], 'flat',   REST_L_ELBOW, REST_L_HAND, 'open'),
    ],
  },
  S004: {                           // father — open-5 at forehead, tap ×2
    label: 'Father', duration: 2400,
    keyframes: [
      kf(0.0,  [292,178], [228,108], 'flat',   REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(0.25, [292,172], [228,101], 'flat',   REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(0.5,  [292,178], [228,108], 'flat',   REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(0.75, [292,172], [228,101], 'flat',   REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(1.0,  [292,178], [228,108], 'flat',   REST_L_ELBOW, REST_L_HAND, 'open'),
    ],
  },
  S005: {                           // child — pat down (height indicator)
    label: 'Child', duration: 2000,
    keyframes: [
      kf(0.0, [282,228], [212,248], 'flat',  REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(0.4, [282,242], [212,268], 'flat',  REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(0.7, [282,228], [212,248], 'flat',  REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(1.0, [282,228], [212,248], 'flat',  REST_L_ELBOW, REST_L_HAND, 'open'),
    ],
  },
  // ── PLACES ────────────────────────────────────────────────────────────────
  S008: {                           // home — pinch at chin, move to cheek
    label: 'Home', duration: 2500,
    keyframes: [
      kf(0.0,  [292,198], [225,152], 'pinch', REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(0.45, [295,185], [248,128], 'pinch', REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(0.7,  [295,183], [250,125], 'pinch', REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(1.0,  [295,185], [248,128], 'pinch', REST_L_ELBOW, REST_L_HAND, 'open'),
    ],
  },
  S009: {                           // school — both hands clap ×2
    label: 'School', duration: 2200,
    keyframes: [
      kf(0.0,  [278,208], [232,208], 'flat',  [122,208], [168,208], 'flat'),
      kf(0.3,  [260,205], [215,205], 'flat',  [140,205], [185,205], 'flat'),
      kf(0.55, [278,208], [232,208], 'flat',  [122,208], [168,208], 'flat'),
      kf(0.8,  [260,205], [215,205], 'flat',  [140,205], [185,205], 'flat'),
      kf(1.0,  [278,208], [232,208], 'flat',  [122,208], [168,208], 'flat'),
    ],
  },
  // ── BASIC NEEDS ───────────────────────────────────────────────────────────
  S010: {                           // water — W-shape at mouth, tap ×2
    label: 'Water', duration: 2000,
    keyframes: [
      kf(0.0,  [292,198], [228,153], 'w',  REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(0.3,  [292,193], [228,147], 'w',  REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(0.55, [292,198], [228,153], 'w',  REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(0.8,  [292,193], [228,147], 'w',  REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(1.0,  [292,198], [228,153], 'w',  REST_L_ELBOW, REST_L_HAND, 'open'),
    ],
  },
  S011: {                           // food — flat-O to mouth (same as eat)
    label: 'Food', duration: 2000,
    keyframes: [
      kf(0.0,  [290,198], [212,155], 'pinch', REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(0.3,  [290,192], [210,148], 'pinch', REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(0.55, [290,198], [212,155], 'pinch', REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(0.8,  [290,192], [210,148], 'pinch', REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(1.0,  [290,198], [212,155], 'pinch', REST_L_ELBOW, REST_L_HAND, 'open'),
    ],
  },
  S013: {                           // eat — flat-O to mouth
    label: 'Eat', duration: 2000,
    keyframes: [
      kf(0.0,  [290,198], [212,155], 'pinch', REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(0.3,  [290,192], [210,148], 'pinch', REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(0.55, [290,198], [212,155], 'pinch', REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(0.8,  [290,192], [210,148], 'pinch', REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(1.0,  [290,198], [212,155], 'pinch', REST_L_ELBOW, REST_L_HAND, 'open'),
    ],
  },
  S014: {                           // drink — C-hand arc to mouth
    label: 'Drink', duration: 2200,
    keyframes: [
      kf(0.0,  [285,215], [215,185], 'c',  REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(0.4,  [288,200], [214,162], 'c',  REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(0.65, [290,192], [213,150], 'c',  REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(1.0,  [285,215], [215,185], 'c',  REST_L_ELBOW, REST_L_HAND, 'open'),
    ],
  },
  // ── ACTIONS ───────────────────────────────────────────────────────────────
  S015: {                           // go — both index fingers arc outward
    label: 'Go', duration: 2000,
    keyframes: [
      kf(0.0, [280,202], [240,200], 'point',  [120,202], [160,200], 'point'),
      kf(0.4, [292,198], [262,194], 'point',  [108,198], [138,194], 'point'),
      kf(0.7, [302,195], [278,190], 'point',  [98,195],  [122,190], 'point'),
      kf(1.0, [302,195], [278,190], 'point',  [98,195],  [122,190], 'point'),
    ],
  },
  S016: {                           // come — both index fingers arc inward
    label: 'Come', duration: 2000,
    keyframes: [
      kf(0.0, [298,200], [265,198], 'point',  [102,200], [135,198], 'point'),
      kf(0.4, [288,202], [250,200], 'point',  [112,202], [150,200], 'point'),
      kf(0.7, [275,205], [228,205], 'point',  [125,205], [172,205], 'point'),
      kf(1.0, [268,208], [218,208], 'point',  [132,208], [182,208], 'point'),
    ],
  },
  S017: {                           // want — both clawed hands pulled toward body
    label: 'Want', duration: 2200,
    keyframes: [
      kf(0.0, [290,200], [258,192], 'claw',  [110,200], [142,192], 'claw'),
      kf(0.4, [278,204], [238,198], 'claw',  [122,204], [162,198], 'claw'),
      kf(0.7, [265,208], [220,205], 'claw',  [135,208], [180,205], 'claw'),
      kf(1.0, [265,208], [220,205], 'claw',  [135,208], [180,205], 'claw'),
    ],
  },
  S016b: {                          // come alias
    label: 'Come', duration: 2000,
    keyframes: [
      kf(0.0, [298,200], [265,198], 'point',  [102,200], [135,198], 'point'),
      kf(0.5, [268,208], [218,208], 'point',  [132,208], [182,208], 'point'),
      kf(1.0, [268,208], [218,208], 'point',  [132,208], [182,208], 'point'),
    ],
  },
  // ── HEALTH ────────────────────────────────────────────────────────────────
  S006: {                           // doctor — D-hand taps wrist
    label: 'Doctor', duration: 2200,
    keyframes: [
      kf(0.0, [285,265], [215,290], 'point',  [138,268], [175,298], 'flat'),
      kf(0.4, [283,258], [214,283], 'point',  [138,268], [175,298], 'flat'),
      kf(0.7, [285,265], [215,290], 'point',  [138,268], [175,298], 'flat'),
      kf(1.0, [285,265], [215,290], 'point',  [138,268], [175,298], 'flat'),
    ],
  },
  S007: {                           // hospital — H traces cross on upper arm
    label: 'Hospital', duration: 2400,
    keyframes: [
      kf(0.0, [282,175], [228,182], 'flat',   REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(0.3, [282,190], [228,198], 'flat',   REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(0.5, [265,182], [240,184], 'flat',   REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(0.75,[280,182], [225,184], 'flat',   REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(1.0, [282,175], [228,182], 'flat',   REST_L_ELBOW, REST_L_HAND, 'open'),
    ],
  },
  S012: {                           // medicine — middle finger rubs palm
    label: 'Medicine', duration: 2000,
    keyframes: [
      kf(0.0, [286,202], [228,205], 'point',  [135,205], [175,205], 'flat'),
      kf(0.4, [284,196], [226,200], 'point',  [135,205], [175,205], 'flat'),
      kf(0.7, [286,202], [228,205], 'point',  [135,205], [175,205], 'flat'),
      kf(1.0, [286,202], [228,205], 'point',  [135,205], [175,205], 'flat'),
    ],
  },
  S018: {                           // pain — index fingers twist at each other
    label: 'Pain', duration: 2000,
    keyframes: [
      kf(0.0, [278,205], [230,202], 'point',  [122,205], [170,202], 'point'),
      kf(0.4, [274,202], [226,202], 'pointD', [126,202], [174,202], 'pointD'),
      kf(0.7, [278,205], [230,202], 'point',  [122,205], [170,202], 'point'),
      kf(1.0, [278,205], [230,202], 'point',  [122,205], [170,202], 'point'),
    ],
  },
  // ── TIME ──────────────────────────────────────────────────────────────────
  S019: {                           // today — Y-hands drop down
    label: 'Today', duration: 2000,
    keyframes: [
      kf(0.0, [285,208], [250,208], 'y',  [115,208], [150,208], 'y'),
      kf(0.5, [285,245], [250,248], 'y',  [115,245], [150,248], 'y'),
      kf(0.8, [285,265], [250,268], 'y',  [115,265], [150,268], 'y'),
      kf(1.0, [285,265], [250,268], 'y',  [115,265], [150,268], 'y'),
    ],
  },
  S020: {                           // tomorrow — thumb arcs forward from cheek
    label: 'Tomorrow', duration: 2200,
    keyframes: [
      kf(0.0, [295,182], [248,128], 'thumb', REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(0.4, [300,175], [265,120], 'thumb', REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(0.7, [308,168], [282,112], 'thumb', REST_L_ELBOW, REST_L_HAND, 'open'),
      kf(1.0, [312,165], [290,108], 'thumb', REST_L_ELBOW, REST_L_HAND, 'open'),
    ],
  },
};

// Fallback sign: gentle wave
const DEFAULT_SIGN = word => ({
  label: word || 'Sign',
  duration: 2000,
  keyframes: [
    kf(0.0, [292,198], [232,150], 'flat',  REST_L_ELBOW, REST_L_HAND, 'open'),
    kf(0.3, [290,192], [228,144], 'flat',  REST_L_ELBOW, REST_L_HAND, 'open'),
    kf(0.6, [292,198], [232,150], 'flat',  REST_L_ELBOW, REST_L_HAND, 'open'),
    kf(1.0, [292,198], [232,150], 'flat',  REST_L_ELBOW, REST_L_HAND, 'open'),
  ],
});

// ─────────────────────────────────────────────────────────────────────────────
// Canvas drawing helpers
// ─────────────────────────────────────────────────────────────────────────────

function drawBg(ctx) {
  // Deep gradient background
  const bg = ctx.createLinearGradient(0, 0, 0, H);
  bg.addColorStop(0,   '#08101e');
  bg.addColorStop(1,   '#111827');
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, W, H);

  // Ambient glow
  const glow = ctx.createRadialGradient(CX, 260, 0, CX, 260, 220);
  glow.addColorStop(0,   'rgba(139,92,246,0.07)');
  glow.addColorStop(1,   'transparent');
  ctx.fillStyle = glow;
  ctx.fillRect(0, 0, W, H);

  // Floor reflection
  ctx.fillStyle = 'rgba(139,92,246,0.04)';
  ctx.fillRect(0, H - 60, W, 60);
}

function drawBody(ctx) {
  ctx.lineCap  = 'round';
  ctx.lineJoin = 'round';

  // ── Head glow ─────────────────────────────────────────────────────────────
  ctx.shadowColor = 'rgba(139,92,246,0.55)';
  ctx.shadowBlur  = 22;

  // Head
  ctx.beginPath();
  ctx.arc(CX, HD_CY, HD_R, 0, Math.PI * 2);
  const headGrad = ctx.createRadialGradient(CX - 10, HD_CY - 10, 5, CX, HD_CY, HD_R);
  headGrad.addColorStop(0, '#e0b98a');
  headGrad.addColorStop(1, '#c49a65');
  ctx.fillStyle = headGrad;
  ctx.fill();

  ctx.shadowBlur = 0;

  // Face features
  // Eyes
  ctx.fillStyle = '#2d1a0a';
  ctx.beginPath(); ctx.ellipse(CX - 12, HD_CY - 6, 4.5, 5, 0, 0, Math.PI * 2); ctx.fill();
  ctx.beginPath(); ctx.ellipse(CX + 12, HD_CY - 6, 4.5, 5, 0, 0, Math.PI * 2); ctx.fill();

  // Pupils
  ctx.fillStyle = '#000';
  ctx.beginPath(); ctx.arc(CX - 12, HD_CY - 5, 2.2, 0, Math.PI * 2); ctx.fill();
  ctx.beginPath(); ctx.arc(CX + 12, HD_CY - 5, 2.2, 0, Math.PI * 2); ctx.fill();

  // Eyebrows
  ctx.strokeStyle = '#5c3a1a';
  ctx.lineWidth = 2.5;
  ctx.lineCap = 'round';
  ctx.beginPath(); ctx.moveTo(CX - 18, HD_CY - 16); ctx.lineTo(CX - 6, HD_CY - 14); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(CX + 6,  HD_CY - 14); ctx.lineTo(CX + 18, HD_CY - 16); ctx.stroke();

  // Smile
  ctx.strokeStyle = '#7a4d25';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(CX, HD_CY + 7, 10, 0.1 * Math.PI, 0.9 * Math.PI);
  ctx.stroke();

  // ── Neck ─────────────────────────────────────────────────────────────────
  ctx.fillStyle = '#c49a65';
  ctx.beginPath();
  ctx.rect(CX - 9, NECK_TOP, 18, NECK_BOT - NECK_TOP);
  ctx.fill();

  // ── Torso ────────────────────────────────────────────────────────────────
  ctx.shadowColor = 'rgba(109,40,217,0.4)';
  ctx.shadowBlur  = 18;

  ctx.beginPath();
  ctx.moveTo(LSH[0] + 6, LSH[1]);
  ctx.lineTo(LHP[0],     LHP[1]);
  ctx.lineTo(RHP[0],     RHP[1]);
  ctx.lineTo(RSH[0] - 6, RSH[1]);
  ctx.closePath();
  const torsoGrad = ctx.createLinearGradient(120, 0, 280, 0);
  torsoGrad.addColorStop(0,   '#6d28d9');
  torsoGrad.addColorStop(0.5, '#8b5cf6');
  torsoGrad.addColorStop(1,   '#6d28d9');
  ctx.fillStyle = torsoGrad;
  ctx.fill();

  // Shoulder bar
  ctx.beginPath();
  ctx.moveTo(LSH[0], LSH[1]);
  ctx.lineTo(RSH[0], RSH[1]);
  ctx.strokeStyle = '#a78bfa';
  ctx.lineWidth   = 18;
  ctx.stroke();

  // ── Legs ─────────────────────────────────────────────────────────────────
  ctx.strokeStyle = '#5b21b6';
  ctx.lineWidth   = 16;
  ctx.lineCap     = 'round';

  // Left leg
  ctx.beginPath();
  ctx.moveTo(LHP[0],      LHP[1]);
  ctx.lineTo(LHP[0] - 10, LHP[1] + 75);
  ctx.lineTo(LHP[0] - 12, LHP[1] + 155);
  ctx.stroke();

  // Right leg
  ctx.beginPath();
  ctx.moveTo(RHP[0],      RHP[1]);
  ctx.lineTo(RHP[0] + 10, RHP[1] + 75);
  ctx.lineTo(RHP[0] + 12, RHP[1] + 155);
  ctx.stroke();

  ctx.shadowBlur = 0;
}

function drawArm(ctx, shoulder, elbow, hand, shape, side) {
  const [sx, sy] = shoulder;
  const [ex, ey] = elbow;
  const [hx, hy] = hand;

  ctx.lineCap  = 'round';
  ctx.lineJoin = 'round';

  // Glow
  ctx.shadowColor = 'rgba(139,92,246,0.55)';
  ctx.shadowBlur  = 16;

  // Upper arm
  ctx.beginPath();
  ctx.moveTo(sx, sy);
  ctx.lineTo(ex, ey);
  ctx.strokeStyle = '#8b5cf6';
  ctx.lineWidth   = 15;
  ctx.stroke();

  // Elbow
  ctx.beginPath();
  ctx.arc(ex, ey, 7.5, 0, Math.PI * 2);
  ctx.fillStyle = '#a78bfa';
  ctx.fill();

  // Forearm
  ctx.beginPath();
  ctx.moveTo(ex, ey);
  ctx.lineTo(hx, hy);
  ctx.strokeStyle = '#7c3aed';
  ctx.lineWidth   = 13;
  ctx.stroke();

  // Wrist
  ctx.beginPath();
  ctx.arc(hx, hy, 5.5, 0, Math.PI * 2);
  ctx.fillStyle = '#c49a65';
  ctx.fill();

  ctx.shadowBlur = 0;

  drawHand(ctx, hx, hy, shape, side);
}

// ── Hand shapes ────────────────────────────────────────────────────────────

function drawHand(ctx, x, y, shape, side) {
  ctx.save();
  ctx.translate(x, y);

  const s   = side === 'right' ? 1 : -1;
  const H_  = '#d4b896';  // skin light
  const HD_ = '#b8906a';  // skin dark

  ctx.shadowColor = 'rgba(212,184,150,0.35)';
  ctx.shadowBlur  = 8;

  switch (shape) {

    case 'open':
    case 'flat': {
      // Palm
      ctx.fillStyle = H_;
      ctx.beginPath();
      ctx.ellipse(0, 2, 11, 12, 0, 0, Math.PI * 2);
      ctx.fill();
      // 5 fingers spread
      const fAngles = s > 0
        ? [-58, -30,  0, 28, 52].map(a => a * Math.PI / 180)
        : [58,  30, 0, -28, -52].map(a => a * Math.PI / 180);
      const fLen    = [21, 26, 28, 25, 20];
      fAngles.forEach((a, i) => {
        ctx.beginPath();
        ctx.moveTo(Math.sin(a) * 9, -Math.cos(a) * 9);
        ctx.lineTo(Math.sin(a) * fLen[i], -Math.cos(a) * fLen[i]);
        ctx.strokeStyle = H_;
        ctx.lineWidth   = 5.5 - i * 0.5;
        ctx.lineCap     = 'round';
        ctx.stroke();
        // Fingertip
        ctx.beginPath();
        ctx.arc(Math.sin(a)*fLen[i], -Math.cos(a)*fLen[i], 3, 0, Math.PI*2);
        ctx.fillStyle = H_;
        ctx.fill();
      });
      break;
    }

    case 'fist': {
      ctx.fillStyle = H_;
      ctx.beginPath();
      ctx.roundRect(-11, -8, 23, 18, 5);
      ctx.fill();
      ctx.strokeStyle = HD_;
      ctx.lineWidth   = 1.2;
      ctx.stroke();
      // Knuckle indents
      for (let i = 0; i < 4; i++) {
        ctx.beginPath();
        ctx.moveTo(-6 + i * 6, -8);
        ctx.lineTo(-6 + i * 6, -3);
        ctx.strokeStyle = HD_;
        ctx.lineWidth   = 1;
        ctx.stroke();
      }
      break;
    }

    case 'point': {
      // Fist base
      ctx.fillStyle = H_;
      ctx.beginPath();
      ctx.roundRect(-11, 0, 23, 15, 4);
      ctx.fill();
      // Index finger up
      ctx.beginPath();
      ctx.roundRect(-4 * s, -28, 8, 30, 4);
      ctx.fill();
      ctx.strokeStyle = HD_;
      ctx.lineWidth   = 1;
      ctx.stroke();
      break;
    }

    case 'pointD': {
      // Pointing downward
      ctx.fillStyle = H_;
      ctx.beginPath();
      ctx.roundRect(-11, -15, 23, 15, 4);
      ctx.fill();
      ctx.beginPath();
      ctx.roundRect(-4 * s, 0, 8, 28, 4);
      ctx.fill();
      ctx.strokeStyle = HD_;
      ctx.lineWidth   = 1;
      ctx.stroke();
      break;
    }

    case 'w': {
      // W: middle 3 fingers up, others closed
      ctx.fillStyle = H_;
      // Palm
      ctx.beginPath();
      ctx.ellipse(0, 5, 12, 10, 0, 0, Math.PI * 2);
      ctx.fill();
      // 3 fingers
      [-10, 0, 10].forEach(fx => {
        ctx.beginPath();
        ctx.moveTo(fx, 0);
        ctx.lineTo(fx, -30);
        ctx.strokeStyle = H_;
        ctx.lineWidth   = 7;
        ctx.lineCap     = 'round';
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(fx, -30, 3.5, 0, Math.PI * 2);
        ctx.fillStyle = H_;
        ctx.fill();
      });
      break;
    }

    case 'c': {
      // C-shape (glass hold)
      ctx.beginPath();
      ctx.arc(0, 0, 18, -0.25 * Math.PI, 1.25 * Math.PI, false);
      ctx.strokeStyle = H_;
      ctx.lineWidth   = 9;
      ctx.lineCap     = 'round';
      ctx.stroke();
      break;
    }

    case 'pinch': {
      // Flat-O / pinch to mouth
      ctx.fillStyle = H_;
      ctx.beginPath();
      ctx.arc(0, 0, 11, 0, Math.PI * 2);
      ctx.fill();
      // Fingertip cluster
      ctx.beginPath();
      ctx.arc(0, -15, 7, 0, Math.PI * 2);
      ctx.fill();
      // Lines
      for (let i = -2; i <= 2; i++) {
        ctx.beginPath();
        ctx.moveTo(i * 4, -2);
        ctx.lineTo(i * 2, -14);
        ctx.strokeStyle = HD_;
        ctx.lineWidth   = 1.5;
        ctx.stroke();
      }
      break;
    }

    case 'claw': {
      // Bent/claw (want)
      ctx.fillStyle = H_;
      ctx.beginPath();
      ctx.ellipse(0, 5, 12, 10, 0, 0, Math.PI * 2);
      ctx.fill();
      const clawA = s > 0
        ? [-40, -14, 6, 26, 46].map(a => a * Math.PI / 180)
        : [ 40,  14,-6,-26,-46].map(a => a * Math.PI / 180);
      clawA.forEach((a, i) => {
        const r = 16 + i * 2;
        ctx.beginPath();
        ctx.moveTo(Math.sin(a) * 9, -Math.cos(a) * 9);
        ctx.quadraticCurveTo(
          Math.sin(a) * r * 0.65, -Math.cos(a) * r * 0.65,
          Math.sin(a + 0.55 * s) * r, -Math.cos(a + 0.55 * s) * r,
        );
        ctx.strokeStyle = H_;
        ctx.lineWidth   = 5 - i * 0.3;
        ctx.lineCap     = 'round';
        ctx.stroke();
      });
      break;
    }

    case 'y': {
      // Y / ILY: thumb + pinky extended
      ctx.fillStyle = H_;
      ctx.beginPath();
      ctx.ellipse(0, 0, 9, 11, 0, 0, Math.PI * 2);
      ctx.fill();
      // Thumb (to side)
      ctx.beginPath();
      ctx.moveTo(-8 * s, 2);
      ctx.lineTo(-26 * s, -8);
      ctx.strokeStyle = H_;
      ctx.lineWidth   = 8;
      ctx.lineCap     = 'round';
      ctx.stroke();
      // Pinky (up-out)
      ctx.beginPath();
      ctx.moveTo(8 * s, -4);
      ctx.lineTo(18 * s, -26);
      ctx.lineWidth = 6;
      ctx.stroke();
      break;
    }

    case 'thumb': {
      // Thumbs-up / thumb extended
      ctx.fillStyle = H_;
      ctx.beginPath();
      ctx.roundRect(-9, 0, 20, 15, 5);
      ctx.fill();
      // Thumb
      ctx.beginPath();
      ctx.roundRect(-9 * s, -23, 9, 23, 4);
      ctx.fill();
      ctx.strokeStyle = HD_;
      ctx.lineWidth   = 1;
      ctx.stroke();
      break;
    }

    case 'l': {
      // L: index + thumb
      ctx.fillStyle = H_;
      ctx.beginPath();
      ctx.roundRect(-9, -2, 20, 15, 5);
      ctx.fill();
      ctx.beginPath();
      ctx.roundRect(-4 * s, -26, 8, 26, 4);
      ctx.fill();
      const tx = s > 0 ? 11 : -23;
      ctx.beginPath();
      ctx.roundRect(tx, -4, 13, 8, 3);
      ctx.fill();
      break;
    }

    default: {
      ctx.fillStyle = H_;
      ctx.beginPath();
      ctx.ellipse(0, 0, 10, 14, 0, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  ctx.restore();
}

function drawLabel(ctx, label) {
  // Bottom label
  const grad = ctx.createLinearGradient(0, 0, W, 0);
  grad.addColorStop(0,   'rgba(109,40,217,0)');
  grad.addColorStop(0.3, 'rgba(109,40,217,0.8)');
  grad.addColorStop(0.7, 'rgba(109,40,217,0.8)');
  grad.addColorStop(1,   'rgba(109,40,217,0)');
  ctx.fillStyle = grad;
  ctx.fillRect(0, H - 42, W, 42);

  ctx.fillStyle   = '#e9d5ff';
  ctx.font        = 'bold 15px Inter, system-ui, sans-serif';
  ctx.textAlign   = 'center';
  ctx.textBaseline= 'middle';
  ctx.letterSpacing = '0.08em';
  ctx.fillText(label.toUpperCase(), CX, H - 20);
}

// ─────────────────────────────────────────────────────────────────────────────
// Main component
// ─────────────────────────────────────────────────────────────────────────────

/**
 * SignAnimatorPanel
 *
 * Props
 * ─────
 * signs   {Array}   — matched_signs array from the translation API
 * className {string}
 */
export default function SignAnimatorPanel({ signs = [], className = '' }) {
  const canvasRef  = useRef(null);
  const rafRef     = useRef(null);
  const startRef   = useRef(null);
  const signDefRef = useRef(null);

  const [currentIdx, setCurrentIdx]   = useState(0);
  const [isPlaying,  setIsPlaying]    = useState(false);
  const [autoNext,   setAutoNext]     = useState(true);
  const [elapsed,    setElapsed]      = useState(0); // ms into current sign

  // Keep refs in sync for the RAF callback
  const currentIdxRef = useRef(currentIdx);
  const isPlayingRef  = useRef(isPlaying);
  const autoNextRef   = useRef(autoNext);
  useEffect(() => { currentIdxRef.current = currentIdx; }, [currentIdx]);
  useEffect(() => { isPlayingRef.current  = isPlaying;  }, [isPlaying]);
  useEffect(() => { autoNextRef.current   = autoNext;   }, [autoNext]);

  // Reset when a new translation arrives
  useEffect(() => {
    setCurrentIdx(0);
    setIsPlaying(signs.length > 0);
    startRef.current = null;
  }, [signs]);

  // Update signDef ref when current sign changes
  useEffect(() => {
    if (!signs[currentIdx]) { signDefRef.current = null; return; }
    const s = signs[currentIdx];
    signDefRef.current = SIGNS[s.sign_id] || DEFAULT_SIGN(s.word || s.label);
    startRef.current = null; // reset time on sign switch
  }, [currentIdx, signs]);

  // Animation loop
  const renderFrame = useCallback((ts) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx    = canvas.getContext('2d');
    const def    = signDefRef.current;

    // Draw body in rest pose if no sign
    if (!def) {
      ctx.clearRect(0, 0, W, H);
      drawBg(ctx);
      drawBody(ctx);
      const rest = {
        rElbow: REST_R_ELBOW, rHand: REST_R_HAND, rShape: 'open',
        lElbow: REST_L_ELBOW, lHand: REST_L_HAND, lShape: 'open',
      };
      drawArm(ctx, RSH, rest.rElbow, rest.rHand, rest.rShape, 'right');
      drawArm(ctx, LSH, rest.lElbow, rest.lHand, rest.lShape, 'left');
      drawBody(ctx); // redraw torso on top of arms

      ctx.fillStyle   = 'rgba(148,163,184,0.6)';
      ctx.font        = '13px Inter, system-ui';
      ctx.textAlign   = 'center';
      ctx.textBaseline= 'middle';
      ctx.fillText('Translate a sentence to animate', CX, H - 22);

      rafRef.current = requestAnimationFrame(renderFrame);
      return;
    }

    if (!startRef.current) startRef.current = ts;
    const elMs  = ts - startRef.current;
    const dur   = def.duration;
    const t     = isPlayingRef.current ? (elMs % dur) / dur : 0;

    setElapsed(Math.min(elMs, dur));

    // Auto-advance to next sign after one full cycle
    if (autoNextRef.current && isPlayingRef.current && elMs > dur) {
      const next = currentIdxRef.current + 1;
      if (next < signs.length) {
        setCurrentIdx(next);
      } else {
        setIsPlaying(false);
      }
    }

    const pose = samplePose(def.keyframes, t);

    ctx.clearRect(0, 0, W, H);
    drawBg(ctx);
    drawArm(ctx, RSH, pose.rElbow, pose.rHand, pose.rShape, 'right');
    drawArm(ctx, LSH, pose.lElbow, pose.lHand, pose.lShape, 'left');
    drawBody(ctx);  // body drawn over arms so torso occludes upper arm base
    drawLabel(ctx, def.label);

    rafRef.current = requestAnimationFrame(renderFrame);
  }, [signs.length]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    rafRef.current = requestAnimationFrame(renderFrame);
    return () => { if (rafRef.current) cancelAnimationFrame(rafRef.current); };
  }, [renderFrame]);

  // ── Derived ─────────────────────────────────────────────────────────────
  const def  = signDefRef.current;
  const dur  = def?.duration ?? 2000;
  const pct  = Math.min((elapsed / dur) * 100, 100);
  const hasMotion = Boolean(SIGNS[signs[currentIdx]?.sign_id]);

  // ── UI ───────────────────────────────────────────────────────────────────
  return (
    <div className={`sign-animator${className ? ' ' + className : ''}`}>
      {/* Canvas */}
      <div style={{ position: 'relative' }}>
        <canvas
          ref={canvasRef}
          width={W}
          height={H}
          style={{
            width: '100%',
            maxWidth: W,
            display: 'block',
            margin: '0 auto',
            borderRadius: 16,
            border: '1px solid rgba(139,92,246,0.2)',
          }}
        />
        {!hasMotion && signs.length > 0 && (
          <div style={{
            position: 'absolute', bottom: 48, left: '50%',
            transform: 'translateX(-50%)',
            background: 'rgba(245,158,11,0.12)',
            border: '1px solid rgba(245,158,11,0.3)',
            borderRadius: 8, padding: '6px 14px',
            fontSize: 12, color: '#fcd34d', whiteSpace: 'nowrap',
          }}>
            ⚠️ Approximate animation — sign not in database
          </div>
        )}
      </div>

      {/* Progress bar */}
      {signs.length > 0 && (
        <div style={{
          marginTop: 12,
          background: 'rgba(255,255,255,0.06)',
          borderRadius: 99, height: 4, overflow: 'hidden',
        }}>
          <div style={{
            width: `${pct}%`,
            height: '100%',
            background: 'linear-gradient(90deg, #8b5cf6, #38bdf8)',
            borderRadius: 99,
            transition: 'width 0.1s linear',
          }} />
        </div>
      )}

      {/* Controls */}
      {signs.length > 0 && (
        <div style={{
          display: 'flex', alignItems: 'center',
          justifyContent: 'center', gap: 10, marginTop: 12,
          flexWrap: 'wrap',
        }}>
          {/* Rewind */}
          <button className="anim-ctrl-btn" onClick={() => {
            setCurrentIdx(0); startRef.current = null;
            setIsPlaying(true);
          }} title="Restart">⏮</button>

          {/* Prev */}
          <button className="anim-ctrl-btn" disabled={currentIdx === 0}
            onClick={() => { setCurrentIdx(i => i - 1); startRef.current = null; }}
            title="Previous sign">‹</button>

          {/* Play / pause */}
          <button
            className="anim-ctrl-btn anim-ctrl-primary"
            onClick={() => { setIsPlaying(p => !p); startRef.current = null; }}
          >
            {isPlaying ? '⏸  Pause' : '▶  Play'}
          </button>

          {/* Next */}
          <button className="anim-ctrl-btn" disabled={currentIdx >= signs.length - 1}
            onClick={() => { setCurrentIdx(i => i + 1); startRef.current = null; }}
            title="Next sign">›</button>

          {/* Auto-advance toggle */}
          <button
            className={`anim-ctrl-btn anim-ctrl-sm${autoNext ? ' anim-ctrl-active' : ''}`}
            onClick={() => setAutoNext(p => !p)}
            title="Auto-advance through signs"
          >
            {autoNext ? '⇄ Auto' : '⇄ Manual'}
          </button>
        </div>
      )}

      {/* Sign navigation chips */}
      {signs.length > 1 && (
        <div style={{
          display: 'flex', flexWrap: 'wrap', gap: 7,
          justifyContent: 'center', marginTop: 12,
        }}>
          {signs.map((s, i) => (
            <button
              key={`${s.sign_id}-${i}`}
              onClick={() => { setCurrentIdx(i); startRef.current = null; setIsPlaying(true); }}
              style={{
                padding: '5px 13px',
                borderRadius: 99,
                border: `1px solid ${i === currentIdx
                  ? 'rgba(139,92,246,0.8)' : 'rgba(255,255,255,0.1)'}`,
                background: i === currentIdx
                  ? 'rgba(139,92,246,0.2)' : 'rgba(255,255,255,0.04)',
                color: i === currentIdx ? '#c4b5fd' : '#94a3b8',
                fontSize: 12, fontWeight: 600, cursor: 'pointer',
                transition: 'all 0.15s',
              }}
            >
              {s.word || s.label || s.sign_id}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
