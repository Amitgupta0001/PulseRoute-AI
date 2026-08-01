import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
CODE_DIR = Path(__file__).resolve().parent

if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

DATASET_DIR = ROOT_DIR / "dataset"

IMAGE_DIR = DATASET_DIR / "media" / "images"
VOICE_DIR = DATASET_DIR / "media" / "audio"

OUTPUT_DIR = ROOT_DIR / "code" / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "output.csv"