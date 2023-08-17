import cv2
import pytesseract
from googletrans import Translator
from unidecode import unidecode
import numpy as np


translator = Translator()

# Translate function
def translate_text(text):
    text = text.replace('\n', ' ')
    if not text.strip():
        return ""
    translated_text = translator.translate(text, src='auto', dest='tr').text
    translated_text = unidecode(translated_text)
    return translated_text

# Read the image
image = cv2.imread('Test/testfile2.png')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

text_data = (pytesseract.image_to_data(gray_image, output_type=pytesseract.Output.DICT))
all_text_data = (pytesseract.image_to_data(gray_image, output_type=pytesseract.Output.DICT))

print(text_data['text'])

# Iterate over each detected text region and draw rectangles if confidence > 80% and text is not blank (OCR failed)
for i in range(len(text_data['text'])):
    if text_data['text'][i].strip():
        x, y, w, h = text_data['left'][i], text_data['top'][i], text_data['width'][i], text_data['height'][i]
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), thickness=2)


# Iterate over each text and if there are no more than 10 blank lines between two texts, concatenate them
while True:
    concatted = False
    for i in range(len(text_data['text']) - 1):
        if text_data['text'][i].strip():
            blanks = 0
            nextLine = ""
            for j in range(i + 1, len(text_data['text'])):
                if text_data['text'][j].strip():
                    nextLine = text_data['text'][j] 
                    break
                else:
                    blanks += 1
            if blanks <= 10:
                text_data['text'][i] += " " + nextLine
                text_data['text'][j] = ""
                concatted = True
    if not concatted:
        break

print(text_data['text'])

# Iterate over each text in the image and fill the text region with the white if text is not blank
for i in range(len(all_text_data['text'])):
    if all_text_data['text'][i].strip():
        x, y, w, h = all_text_data['left'][i], all_text_data['top'][i], all_text_data['width'][i], all_text_data['height'][i]
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), thickness=cv2.FILLED)

cv2.imwrite('Test/testfile2_ocr.png', image)
