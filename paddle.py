#from paddleocr import PaddleOCR

#import paddle
#print(paddle.__version__)

#ocr = PaddleOCR()

#results = ocr.predict('/yugioh_extract/data/cards/IMG_0518.PNG')


from paddleocr import PaddleOCR

# Initialize PaddleOCR
ocr = PaddleOCR()

# Read the image
results = ocr.predict("yugioh_extract/data/cards/IMG_0518.PNG")

# Display the extracted text
for result in results:
    result.print()