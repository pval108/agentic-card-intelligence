from pathlib import Path

ROOT = Path("/yugioh_extract")
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
IMAGE_DIR = DATA_DIR / "card_images"
DB_PATH = DATA_DIR / "yugioh.sqlite3"
CATALOG_PATH = RAW_DIR / "cardinfo.json"
VERSION_PATH = RAW_DIR / "database_version.txt"