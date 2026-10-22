
"""
gesture_selection.py
====================
Stage 3 of the Text/Speech-to-Sign pipeline.

Responsibilities
----------------
- Load and validate the signs.json metadata file.
- Map normalised tokens to SignEntry objects.
- Support aliases and Sinhala labels.
- Locate existing sign videos without moving or renaming them.
- Report missing video files.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

_DEFAULT_SIGNS_JSON = (
    Path(__file__).parents[2] / "dataset" / "metadata" / "signs.json"
)


@dataclass
class SignEntry:
    """A validated sign record loaded from signs.json."""

    sign_id: str
    label: str
    video_path: str
    expert: str
    language: str = "SLSL"
    sinhala_label: Optional[str] = None
    variants: list[str] = field(default_factory=list)
    aliases: list[str] = field(default_factory=list)
    context_tags: list[str] = field(default_factory=list)
    video_exists: bool = False

    @property
    def display_label(self) -> str:
        """Return the English label and Sinhala label, when available."""
        if self.sinhala_label:
            return f"{self.label} ({self.sinhala_label})"
        return self.label


class SignDatabase:
    """Load sign metadata and provide token-to-sign lookups."""

    def __init__(
        self,
        entries: list[SignEntry],
        repo_root: Path,
    ) -> None:
        self._entries = entries
        self._repo_root = repo_root
        self._index: dict[str, SignEntry] = {}

        for entry in entries:
            key = entry.label.lower().strip()
            if key not in self._index:
                self._index[key] = entry

            for alias in entry.aliases:
                alias_key = alias.lower().strip()
                if alias_key not in self._index:
                    self._index[alias_key] = entry

            if entry.sinhala_label:
                sinhala_key = entry.sinhala_label.strip()
                if sinhala_key not in self._index:
                    self._index[sinhala_key] = entry

    @classmethod
    def load(
        cls,
        path: Path | str | None = None,
        repo_root: Path | str | None = None,
    ) -> "SignDatabase":
        """Load and validate the signs.json metadata file."""

        if repo_root is None:
            repo_root = Path(__file__).parents[2]

        repo_root = Path(repo_root)

        if path is None:
            path = repo_root / "dataset" / "metadata" / "signs.json"

        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(
                f"signs.json not found at {path}"
            )

        with path.open("r", encoding="utf-8") as file:
            raw = json.load(file)

        if not isinstance(raw, dict) or not isinstance(
            raw.get("signs"), list
        ):
            raise ValueError(
                f"signs.json at {path} must contain a 'signs' list."
            )

        entries: list[SignEntry] = []

        for record in raw["signs"]:
            if not isinstance(record, dict):
                raise ValueError(
                    f"Invalid sign record: {record}"
                )

            entries.append(_parse_entry(record, repo_root))

        database = cls(entries=entries, repo_root=repo_root)

        logger.info(
            "SignDatabase loaded: %d signs, %d with video on disk.",
            len(entries),
            sum(1 for entry in entries if entry.video_exists),
        )

        return database

    def lookup(self, token: str) -> Optional[SignEntry]:
        """Find a sign by English label, alias, or Sinhala label."""
        return self._index.get(token.lower().strip())

    def all_signs(self) -> list[SignEntry]:
        """Return all sign entries."""
        return list(self._entries)

    def summary(self) -> dict:
        """Return a summary suitable for the API."""
        return {
            "total": len(self._entries),
            "with_video": sum(
                1 for entry in self._entries if entry.video_exists
            ),
            "signs": [
                {
                    "sign_id": entry.sign_id,
                    "label": entry.label,
                    "sinhala_label": entry.sinhala_label,
                    "display_label": entry.display_label,
                    "video_path": entry.video_path,
                    "video_exists": entry.video_exists,
                    "expert": entry.expert,
                    "aliases": entry.aliases,
                    "context_tags": entry.context_tags,
                }
                for entry in self._entries
            ],
        }


def _parse_entry(record: dict, repo_root: Path) -> SignEntry:
    """Parse one sign record and locate its video if it exists."""

    required = ("sign_id", "label", "video_path", "expert")

    for key in required:
        if key not in record:
            raise ValueError(
                f"signs.json entry is missing required field "
                f"'{key}': {record}"
            )

    video_path: str = record["video_path"]
    abs_video = repo_root / video_path

    # First, check the path specified in the metadata.
    if not abs_video.is_file():
        # Search the existing expert folders for the exact filename.
        filename = Path(video_path).name
        expert_root = repo_root / "expert_reference"

        if expert_root.is_dir():
            matches = sorted(
                expert_root.rglob(filename),
                key=lambda path: str(path).lower(),
            )

            if matches:
                abs_video = matches[0]
                video_path = abs_video.relative_to(
                    repo_root
                ).as_posix()

    video_exists = abs_video.is_file()

    if not video_exists:
        logger.warning(
            "Video file not found for sign '%s': %s",
            record["label"],
            abs_video,
        )

    return SignEntry(
        sign_id=record["sign_id"],
        label=record["label"],
        sinhala_label=record.get("sinhala_label"),
        video_path=video_path,
        expert=record.get("expert", "unknown"),
        language=record.get("language", "SLSL"),
        variants=record.get("variants", []),
        aliases=record.get("aliases", []),
        context_tags=record.get("context_tags", []),
        video_exists=video_exists,
    )
