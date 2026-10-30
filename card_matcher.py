
import json
import re
import sqlite3
from pathlib import Path

from rapidfuzz import fuzz, process

file = "card_matcher.py"

ROOT = Path(file).resolve().parent

#print(ROOT)

DB_PATH = ROOT / "data" / "yugioh.sqlite3"


#DB_PATH

# "yugioh_extract/data/cards/IMG_0519.PNG"



def normalize(text):
    """Normalize text for approximate matching."""
    text = text.upper()
    text = re.sub(r"[^A-Z0-9]+", " ", text)
    return " ".join(text.split())


def extract_stats(lines):
    """Read ATK and DEF when they appear in OCR text."""
    full_text = " ".join(lines).upper()

    def read_stat(label):
        match = re.search(
            rf"\b{label}\s*[/:\s]\s*(\d{{1,5}})\b",
            full_text,
        )
        return int(match.group(1)) if match else None

    return read_stat("ATK"), read_stat("DEF")


def match_card(ocr_lines, limit=5):
    """Find likely card identities in the local catalog."""

    if not DB_PATH.is_file():
        raise FileNotFoundError(
            f"Database not found: {DB_PATH}"
        )

    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            """
            SELECT id, name, attack, defense, raw_json
            FROM cards
            """
        ).fetchall()

    if not rows:
        raise ValueError("The card catalog is empty.")

    # Catalog names used for fuzzy matching.
    names = [normalize(row[1]) for row in rows]

    # Try each OCR line, plus adjacent lines in case
    # the OCR engine split a card name.
    queries = []

    for i, line in enumerate(ocr_lines):
        queries.append(normalize(line))

        if i + 1 < len(ocr_lines):
            queries.append(
                normalize(line + " " + ocr_lines[i + 1])
            )

    queries = [
        q for q in queries
        if len(q) >= 5
    ]

    if not queries:
        return []

    # Retain each card's best matching text score.
    candidate_scores = {}

    for query in queries:
        matches = process.extract(
            query,
            names,
            scorer=fuzz.ratio,
            limit=limit,
        )

        for _, score, index in matches:
            candidate_scores[index] = max(
                score,
                candidate_scores.get(index, 0),
            )

    extracted_atk, extracted_def = extract_stats(ocr_lines)

    ranked = []

    for index, score in candidate_scores.items():
        card_id, name, atk, defense, raw_json = rows[index]

        # Cross-check gameplay statistics.
        conflicts = []

        if extracted_atk is not None and atk != extracted_atk:
            conflicts.append("ATK mismatch")

        if extracted_def is not None and defense != extracted_def:
            conflicts.append("DEF mismatch")

        raw = json.loads(raw_json) if raw_json else {}

        ranked.append({
            "card_id": card_id,
            "name": name,
            "type": raw.get("type"),
            "attack": atk,
            "defense": defense,
            "name_similarity": round(score, 2),
            "conflicts": conflicts,
        })

    ranked.sort(
        key=lambda x: (
            len(x["conflicts"]) == 0,
            x["name_similarity"],
        ),
        reverse=True,
    )

    return ranked[:limit]


if __name__ == "__main__":

    # Replace these example lines with your OCR output.
    ocr_lines = [
#        "BLUE-EYES WHITE DRAGON",
 #       "DARK HOLE",
        "SLIFER THE SKY DRAGON",
        "Dragon / Normal",
        "ATK/3000 DEF/2500",
    ]

    matches = match_card(ocr_lines)

    print("\nTop candidate cards:\n")

    for card in matches:
        print(json.dumps(card, indent=2))

    if matches:
        top = matches[0]

        # Provisional threshold, not a calibrated probability.
        if (
            top["name_similarity"] >= 90
            and not top["conflicts"]
        ):
            print("\nStrong card-name candidate:", top["name"])
        else:
            print("\nManual verification recommended.")

