import json
import sqlite3
from pathlib import Path

import requests

# Project directory
ROOT = Path(__file__).resolve().parent

# Output directories
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"

DATA_DIR.mkdir(exist_ok=True)
RAW_DIR.mkdir(exist_ok=True)

API_URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php"

JSON_PATH = RAW_DIR / "cardinfo.json"
DB_PATH = DATA_DIR / "yugioh.sqlite3"


def download_catalog():
    print("Downloading Yu-Gi-Oh! card catalog...")

    response = requests.get(API_URL, timeout=120)
    response.raise_for_status()

    data = response.json()
    cards = data["data"]

    with open(JSON_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    print(f"Downloaded {len(cards)} cards")
    return cards


def save_to_database(cards):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY,
                name TEXT,
                type TEXT,
                description TEXT,
                attack INTEGER,
                defense INTEGER,
                race TEXT,
                attribute TEXT,
                raw_json TEXT
            )
        """)

        for card in cards:
            conn.execute("""
                INSERT OR REPLACE INTO cards (
                    id, name, type, description,
                    attack, defense, race, attribute, raw_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                card.get("id"),
                card.get("name"),
                card.get("type"),
                card.get("desc"),
                card.get("atk"),
                card.get("def"),
                card.get("race"),
                card.get("attribute"),
                json.dumps(card)
            ))

        conn.commit()

    print(f"Database saved to: {DB_PATH}")


if __name__ == "__main__":
    if JSON_PATH.exists():
        print("Loading previously downloaded catalog...")
        with open(JSON_PATH, encoding="utf-8") as file:
            cards = json.load(file)["data"]
    else:
        cards = download_catalog()

    save_to_database(cards)
    print("Catalog import complete!")