import cv2
import pytesseract
from googletrans import Translator
from unidecode import unidecode
import numpy as np

# Read the image
image = cv2.imread('test.jpg')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#box = pytesseract.image_to_boxes(gray_image)
#print(box)

datas = pytesseract.image_to_data(gray_image, output_type=Output.STRING)

lines  = box.replace("\t", " ")
lines = lines.split("\n")
print(lines)

text = pytesseract.image_to_string(gray_image)

texts = text.split("\n\n")
texts.pop(len(texts)-1)

def connectText(i:int,texts:list):
    text:str = texts[i]
    isContinue =  text.find("...")
    if isContinue != -1:
        text = text.replace("..."," ")
        text += texts[i+1]
        texts[i] = text
        texts[i+1] = "" # Rather reöove the item, make empty because we have to know item count

willConnectTexts:list = []

for i in range(len(texts)) :
    isContinue =  text.find("...")
    if(isContinue != -1):
        willConnectTexts.insert(0,i)

for ind in willConnectTexts:
    connectText(ind,texts)

translator = Translator()
for text in texts:
    if text != "":
        text = text.replace('\n', ' ')
        print(text)
        translated_text = translator.translate(text, src='auto', dest='tr').text
        print(translated_text + "\n")
