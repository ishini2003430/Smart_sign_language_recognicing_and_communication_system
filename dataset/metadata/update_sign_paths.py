
import json
from pathlib import Path
from datetime import datetime
import shutil

root = Path(__file__).resolve().parents[2]
metadata = root / "dataset" / "metadata" / "signs.json"
video_root = root / "expert_reference"

# Stop safely if required folders are missing.
if not metadata.is_file():
    raise FileNotFoundError(f"Metadata not found: {metadata}")
if not video_root.is_dir():
    raise FileNotFoundError(f"Video folder not found: {video_root}")

# Create a backup before changing anything.
stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup = metadata.with_name(f"signs_backup_{stamp}.json")
shutil.copy2(metadata, backup)

matches = {
    "i": "S16_I.mp4",
    "you": "S17_You.mp4",
    "mother": "S01_amma.mp4",
    "father": "S02_father.mp4",
    "home": "S12_home.mp4",
    "school": "S07_school.mp4",
    "water": "S19_water.mp4",
    "eat": "S15_eat.mp4",
    "drink": "S27_drink.mp4",
    "go": "S04_go.mp4",
    "come": "S05_come.mp4",
    "want": "S18_want.mp4",
}

data = json.loads(metadata.read_text(encoding="utf-8"))
updated = []

for sign in data["signs"]:
    label = sign.get("label", "").strip().lower()
    filename = matches.get(label)

    if not filename:
        continue

    candidates = list(video_root.rglob(filename))
    if not candidates:
        print(f"NOT FOUND: {label} / {filename}")
        continue

    # Prefer expert_03 when the same recording label exists there.
    candidates.sort(
        key=lambda p: ("expert_03" not in p.parts, str(p).lower())
    )

    video = candidates[0]
    relative_path = video.relative_to(root).as_posix()
parts = relative_path.split("/")

# Remove duplicated folder names if present.
clean_parts = []
for part in parts:
    if not clean_parts or clean_parts[-1].lower() != part.lower():
        clean_parts.append(part)

sign["video_path"] = "/".join(clean_parts)
    sign["expert"] = video.parent.name
    sign["video_ready"] = True
    updated.append(label)

if updated:
    data["status"] = "partially_ready"
    metadata.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

print(f"Backup: {backup}")
print(f"Updated {len(updated)} signs: {', '.join(updated)}")
print("Original video files were not moved or renamed.")
