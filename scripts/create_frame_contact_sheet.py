
from pathlib import Path
import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
FRAME_DIR = ROOT / "dataset" / "processed" / "video_inspection_frames"
OUTPUT = FRAME_DIR / "comparison_contact_sheet.jpg"

files = [
    ("Learner", f"learner_attempt01_frame_{n:04d}.jpg")
    for n in [0, 10, 21, 31, 41]
] + [
    ("Expert 02", f"expert_02_frame_{n:04d}.jpg")
    for n in [0, 18, 36, 54, 71]
]

tiles = []
for label, filename in files:
    path = FRAME_DIR / filename
    image = cv2.imread(str(path))

    if image is None:
        print("Missing or unreadable:", path)
        continue

    image = cv2.resize(image, (320, 400))
    cv2.rectangle(image, (0, 0), (320, 35), (0, 0, 0), -1)
    cv2.putText(
        image, f"{label}: {filename.split('_frame_')[-1].split('.')[0]}",
        (6, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.48,
        (255, 255, 255), 1, cv2.LINE_AA
    )
    tiles.append(image)

if tiles:
    blank = np.zeros_like(tiles[0])
    while len(tiles) < 10:
        tiles.append(blank)

    rows = [
        cv2.hconcat(tiles[i:i + 5])
        for i in range(0, 10, 5)
    ]
    sheet = cv2.vconcat(rows)

    if cv2.imwrite(str(OUTPUT), sheet):
        print("Contact sheet saved:", OUTPUT)
    else:
        print("ERROR: Could not save contact sheet.")
else:
    print("ERROR: No readable frames found.")
