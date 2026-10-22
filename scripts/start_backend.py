"""
scripts/start_backend.py
========================
Convenience script to start the FastAPI backend for the sign animation component.

Usage (from repository root):
    python scripts/start_backend.py

The backend will be available at:
    http://localhost:8000/api/docs    (interactive API documentation)
    http://localhost:8000/api/health  (health check)
"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent


def main() -> None:
    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "backend.app:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8000",
        "--reload",
    ]
    print("Starting SLSL Sign Animation backend …")
    print("API docs: http://localhost:8000/api/docs")
    print("Health:   http://localhost:8000/api/health")
    print("Press Ctrl+C to stop.\n")
    subprocess.run(cmd, cwd=str(REPO_ROOT), check=True)


if __name__ == "__main__":
    main()
