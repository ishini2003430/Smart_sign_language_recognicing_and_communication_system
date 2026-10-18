"""Run all three recognition models from the project root: python scripts/train_recognizer.py ..."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.recognition.train import cli
if __name__ == '__main__':
    cli()
