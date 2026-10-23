#from paddleocr import PaddleOCR

#import paddle
#print(paddle.__version__)

#ocr = PaddleOCR()

#results = ocr.predict('/yugioh_extract/data/cards/IMG_0518.PNG')




from paddleocr import PaddleOCR
import cv2
from matplotlib import pyplot as plt

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Read the image
#results = ocr.predict("yugioh_extract/data/cards/IMG_0518.PNG") #dark magician

results = ocr.predict("yugioh_extract/data/cards/IMG_0519.PNG") #blue eyes

# Display the extracted text
#for result in results:
 #   result.print()

for result in results:
    texts = result["rec_texts"]
    scores = result["rec_scores"]

    for text, score in zip(texts, scores):
        print(f"{text} | OCR confidence: {score:.2f}")












image_path = "yugioh_extract/data/cards/IMG_0518.PNG"
img = cv2.imread(image_path)


plt.figure()
plt.imshow(img)
plt.show()
result = ocr.ocr(img,cls=True)
print(result[0][1][1])

from matplotlib import pyplot as plt



print("Matplotlib imported successfully!")




import sys

print(sys.version)
print(sys.executable)