
from pathlib import Path

from paddleocr import PaddleOCR
from card_matcher_test import match_card

# Initialize PaddleOCR
#ocr = PaddleOCR(
 #   use_angle_cls=True,
  #  lang="en"
#)


from paddleocr import PaddleOCR

ocr = PaddleOCR(
    lang="en",
    enable_mkldnn=False,
)


def read_card(image_path):
    """Extract text from an image."""
    results = ocr.predict(str(image_path))

    extracted_text = []

    for result in results:
        extracted_text.extend(result["rec_texts"])

    return extracted_text


def process_card(image_path):
    """Read a card and search the local database."""

    # Step 1: Extract text
    text_lines = read_card(image_path)

    print("\nEXTRACTED TEXT:")
    for line in text_lines:
        print(line)

    # Step 2: Pass OCR text to the matcher
    matches = match_card(text_lines)

    # Step 3: Display database results
    if not matches:
        print("\nNo matching card found.")
        return None

    best_match = matches[0]

    print("\nBEST DATABASE MATCH:")
    print("Card ID:", best_match["card_id"])
    print("Name:", best_match["name"])
    print("ATK:", best_match["attack"])
    print("DEF:", best_match["defense"])
    print("Similarity:", best_match["name_similarity"])

    if best_match["conflicts"]:
        print("Validation conflicts:", best_match["conflicts"])

    return best_match


if __name__ == "__main__":
    root = Path(__file__).resolve().parent

    image_path = root / "data" / "cards" / "IMG_0518.PNG"

    process_card(image_path)
