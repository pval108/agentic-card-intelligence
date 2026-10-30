
from pathlib import Path
from paddleocr import PaddleOCR

# Initialize PaddleOCR for CPU
ocr = PaddleOCR(
    lang="en",
    device="cpu",
    enable_mkldnn=False,
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
)

# Image path
image_path = "data/cards/IMG_0519.PNG"

# Verify image exists
if not Path(image_path).is_file():
    raise FileNotFoundError(f"Image not found: {image_path}")

# Run OCR
results = ocr.predict(image_path)

# Display recognized text and confidence
for result in results:
    texts = result["rec_texts"]
    scores = result["rec_scores"]

    for text, score in zip(texts, scores):
        print(f"{text} | OCR confidence: {float(score):.2f}")

print("OCR processing completed!")
