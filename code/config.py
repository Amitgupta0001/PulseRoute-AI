from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent

DATASET_DIR = ROOT_DIR / "dataset"

IMAGE_DIR = DATASET_DIR / "media" / "images"
VOICE_DIR = DATASET_DIR / "media" / "audio"

OUTPUT_DIR = ROOT_DIR / "code" / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "output.csv"