r"""Manually mark the active signing interval of one existing pilot video.

Run from the repository root:
  .\.venv\Scripts\python.exe .\scripts\annotate_pilot_boundaries.py --video expert_01/S01_amma.mp4

No raw video or landmark files are changed. Annotations are saved to
  dataset/annotations/pilot_sign_boundaries.csv

Frame convention:
  start_frame = included in the sign
  end_frame_exclusive = first frame AFTER the sign (Python slice end)
"""

import argparse
import csv
import math

import numpy as np
from pathlib import Path

import cv2

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "dataset" / "metadata" / "pilot_video_manifest.csv"
OUTPUT = ROOT / "dataset" / "annotations" / "pilot_sign_boundaries.csv"
FIELDS = [
    "video_path", "sign_id", "label", "signer_id",
    "start_frame", "end_frame_exclusive", "start_ms", "end_ms",
    "annotation_status", "notes",
]


def find_video_row(selector):
    if not MANIFEST.is_file():
        raise FileNotFoundError(f"Pilot manifest not found: {MANIFEST}")
    with MANIFEST.open(newline="", encoding="utf-8-sig") as handle:
        entries = list(csv.DictReader(handle))

    normalized = selector.replace("\\", "/").strip("/")
    candidates = [
        row for row in entries
        if row["video_path"].replace("\\", "/").endswith(normalized)
    ]
    if not candidates:
        choices = "\n".join(
            "  " + "/".join(row["video_path"].split("/")[-2:])
            for row in entries
        )
        raise ValueError(f"Video not found in manifest: {selector}\nAvailable choices:\n{choices}")
    if len(candidates) != 1:
        raise ValueError("Ambiguous video name. Include expert_01/ or expert_02/.")
    return candidates[0]


def already_annotated(video_path):
    if not OUTPUT.exists():
        return False
    with OUTPUT.open(newline="", encoding="utf-8-sig") as f:
        return any(r.get("video_path") == video_path for r in csv.DictReader(f))


def save_annotation(row, start, end, fps, notes):
    if start is None or end is None or start >= end:
        raise ValueError("Set a start and an end frame first; end must follow start")
    if already_annotated(row["video_path"]):
        raise FileExistsError(
            f"Already annotated {row['video_path']} in {OUTPUT}. "
            "Open the CSV and review/edit that row instead of writing a duplicate."
        )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    new_file = not OUTPUT.exists()
    record = {
        "video_path": row["video_path"],
        "sign_id": row["sign_id"],
        "label": row["label"],
        "signer_id": row["signer_id"],
        "start_frame": start,
        "end_frame_exclusive": end,
        "start_ms": round(1000 * start / fps),
        "end_ms": round(1000 * end / fps),
        "annotation_status": "needs_expert_review",
        "notes": notes,
    }
    with OUTPUT.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if new_file:
            writer.writeheader()
        writer.writerow(record)
    return record


def annotate(row, notes):
    video_path = ROOT / row["video_path"]
    if not video_path.is_file():
        raise FileNotFoundError(video_path)
    if already_annotated(row["video_path"]):
        raise FileExistsError(
            "An annotation for this video already exists. "
            "Check dataset/annotations/pilot_sign_boundaries.csv before editing it."
        )

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open {video_path}")
    window = "Sign boundary annotation - drag Frame slider"
    try:
        fps = cap.get(cv2.CAP_PROP_FPS)
        if not math.isfinite(fps) or fps <= 0:
            raise RuntimeError("Invalid FPS")
        n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if n_frames <= 1:
            raise RuntimeError("Not enough video frames")
        cv2.namedWindow(window, cv2.WINDOW_NORMAL)
        cv2.createTrackbar("Frame", window, 0, n_frames - 1, lambda _: None)
        start, end = None, None
        last_frame_idx = None
        frame = None
        print(f"Review: {row['video_path']} ({n_frames} frames at {fps:.2f} FPS)")
        print("Drag slider to seek; A/D = 1 frame; J/L = 10 frames")
        print("S = mark first frame of sign; E = mark last frame of sign")
        print("W = save and close; Q = exit without saving")
        while True:
            idx = cv2.getTrackbarPos("Frame", window)
            if frame is None or idx != last_frame_idx:
                cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
                ok, frame = cap.read()
                if not ok:
                    raise RuntimeError(f"Could not decode frame {idx}")
                last_frame_idx = idx

            h, w = frame.shape[:2]
            scale = min(800 / max(w, 1), 600 / max(h, 1), 1.0)
            photo = cv2.resize(frame, (round(w * scale), round(h * scale)))
            panel_w = 450
            canvas_h = max(photo.shape[0], 340)
            canvas_w = photo.shape[1] + panel_w
            canvas = np.full((canvas_h, canvas_w, 3), 36, dtype="uint8")
            canvas[:photo.shape[0], :photo.shape[1]] = photo
            x0 = photo.shape[1] + 18
            lines = [
                row['video_path'].split('/')[-2] + ' / ' + video_path.name,
                f"FRAME: {idx}/{n_frames - 1}    TIME: {idx / fps:.2f} s",
                "",
                "DRAG the Frame slider to seek",
                "A / D : previous / next frame",
                "J / L : back / forward 10 frames",
                "S : set START (inclusive)",
                "E : set END (inclusive)",
                "W : SAVE     Q : QUIT",
                "",
                f"Start: {start if start is not None else 'not set'}",
                f"End:   {end - 1 if end is not None else 'not set'}",
                "",
                "Exclude preparing / camera-stop motions",
                "Check boundaries with SLSL expert",
                "Saved rows need expert review",
            ]
            y = 26
            for line in lines:
                cv2.putText(canvas, line, (x0, y), cv2.FONT_HERSHEY_SIMPLEX,
                            0.49, (230, 230, 230), 1, cv2.LINE_AA)
                y += 24
            cv2.imshow(window, canvas)
            key = cv2.waitKey(30) & 0xFF
            if key in (ord('a'), ord('A'), ord('j'), ord('J'), ord('d'), ord('D'), ord('l'), ord('L')):
                if key in (ord('a'), ord('A')):
                    amount = -1
                elif key in (ord('j'), ord('J')):
                    amount = -10
                elif key in (ord('d'), ord('D')):
                    amount = 1
                elif key in (ord('l'), ord('L')):
                    amount = 10
                cv2.setTrackbarPos("Frame", window, max(0, min(n_frames - 1, idx + amount)))
            elif key in (ord('s'), ord('S')):
                start = idx
                print(f"START marked at frame {start} ({start / fps:.2f}s)")
            elif key in (ord('e'), ord('E')):
                end = idx + 1  # exclusive Python slice boundary
                print(f"END marked at frame {idx} ({(idx + 1) / fps:.2f}s exclusive)")
            elif key in (ord('w'), ord('W')):
                if start is None or end is None or start >= end:
                    print("Not saved: mark start (S) and a later end (E) first.")
                    continue
                saved = save_annotation(row, start, end, fps, notes)
                print(f"SAVED to {OUTPUT}")
                print(f"  {saved['video_path']}")
                print(f"  frames [{start}:{end}], {saved['start_ms']}–{saved['end_ms']} ms")
                return
            elif key in (ord('q'), ord('Q'), 27):
                print("Closed without saving.")
                return
            try:
                if cv2.getWindowProperty(window, cv2.WND_PROP_VISIBLE) < 1:
                    print("Window closed without saving.")
                    return
            except cv2.error:
                print("Window closed without saving.")
                return
    finally:
        cap.release()
        cv2.destroyAllWindows()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--video", required=True,
                   help="Manifest suffix, e.g. expert_01/S01_amma.mp4")
    p.add_argument("--notes", default="manual pilot annotation; verify with SLSL expert")
    args = p.parse_args()
    annotate(find_video_row(args.video), args.notes)


if __name__ == "__main__":
    main()
