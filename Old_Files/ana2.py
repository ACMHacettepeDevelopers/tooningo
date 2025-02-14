import cv2
import pytesseract
from googletrans import Translator
from unidecode import unidecode
from TextModel import TextModel
from BaloonText import BaloonText
import re
from PIL import Image, ImageDraw, ImageFont
import sys
import gpt
import numpy as np
from collections import Counter

# Initialize the translator
translator = Translator()


def translate_text(text, dest:str):
    """Translate text from any language to Turkish"""
    text = text.replace('\n', ' ')
    if not text.strip():
        return ""
    translated_text = translator.translate(text, src='auto', dest = dest).text
    #translated_text = unidecode(translated_text)

    return translated_text


def translate_GPT(text, dest:str):
    """Translate text from any language to Turkish using GPT-3.5"""
    text = text.replace('\n', ' ')
    if not text.strip():
        return ""
    translated_text = gpt.translate(text, dest)
    return translated_text


def isEmpty(text:str) -> bool:
    if text == "":
        return True
    pattern = r'^[\s\n\t]*$'
    return re.match(pattern,text)


def getBaloonTexts(dictionary:dict) -> dict:
    baloonTexts = dict()
    for i in range(len(dictionary["text"])):
        textModel = TextModel(
                level=dictionary["level"][i],
                page_num=dictionary["page_num"][i],
                block_num=dictionary["block_num"][i],
                par_num=dictionary["par_num"][i],
                line_num=dictionary["line_num"][i],
                word_num=dictionary["word_num"][i],
                left=dictionary["left"][i],
                top=dictionary["top"][i],
                width=dictionary["width"][i],
                height=dictionary["height"][i],
                conf=dictionary["conf"][i],
                text=dictionary["text"][i].strip("\n")
            )
        if not textModel.block_num in baloonTexts:
            baloonTexts[textModel.block_num] = BaloonText(textModel)

        if(not isEmpty(textModel.text)):
            baloonTexts[textModel.block_num].text += " " + textModel.text
        baloonTexts[textModel.block_num].text_models += [textModel]

    return baloonTexts


def getNecesseryBaloons(datas:dict):
    baloonTexts:dict = getBaloonTexts(datas)
    willDeleted = []
    #print(textModels)
    for num in baloonTexts:
        baloonText: BaloonText = baloonTexts[num]
        if(isEmpty(baloonText.text)):
            willDeleted.append(num)

    for num in willDeleted:
        baloonTexts.pop(num)
    return baloonTexts


def extractData(gray_image):
    """Extract text data using OCR"""
    text_data = (pytesseract.image_to_data(gray_image, output_type=pytesseract.Output.DICT))
    return text_data


# Read the image
def readImage(path):
    """Read image and convert it to grayscale"""
    image = cv2.imread(path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    invert = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    gray_image = 255 - invert
    return image, gray_image


def removeBlanks(image, baloonTexts:dict):
    """Remove blank regions from the image"""
    for i in baloonTexts:
        drawFilledRectangle(image,baloonTexts[i].border_box)


def drawBorderRectangle(image, border_box:TextModel):
    x, y, w, h = border_box.left, border_box.top, border_box.width, border_box.height
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), thickness=2)


def drawFilledRectangle(image, border_box:TextModel):
    x, y, w, h = border_box.left, border_box.top, border_box.width, border_box.height
    # Extract the region covered by the bubble
    bubble_region = image[y:y+h, x:x+w]
    
    # Convert the bubble region to grayscale for easier color analysis
    bubble_gray = cv2.cvtColor(bubble_region, cv2.COLOR_BGR2GRAY)
    
    # Calculate the most common color value in the bubble region
    pixel_values = bubble_gray.reshape(-1)
    color_counter = Counter(pixel_values)
    most_common_color_value = color_counter.most_common(1)[0][0]
    
    # Convert the color value back to BGR format
    bubble_background_color = np.array([most_common_color_value, most_common_color_value, most_common_color_value], dtype=np.uint8)

    # Fill the bubble region with the most common color
    image[y:y+h, x:x+w] = bubble_background_color


def overlayBaloonText(image_pillow, baloonText:BaloonText):
    """Overlay translated text on the image"""

    font_size= 30
    font_color = (0, 0, 0) 
    font_pillow = ImageFont.truetype("Tahoma", font_size)

    draw = ImageDraw.Draw(image_pillow)

    
    x, y, w, h = baloonText.border_box.left, baloonText.border_box.top, baloonText.border_box.width, baloonText.border_box.height
    
    # Split translated_text into lines that fit within the text region
    lines = []
    current_line = ""
    words = baloonText.translatedText.split()

    for word in words:
        text_width = draw.textsize(current_line+word, font=font_pillow)[0]
 
        if text_width <= w +50:
            current_line += ' ' + word if current_line else word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    
    totalHeight = 0
    for i in lines:
        text_height = draw.textsize(current_line+word, font=font_pillow)[1]
        totalHeight += text_height
    # Calculate total height of the lines

    # Calculate starting y-coordinate for centering the text
    y_start = y + (h-totalHeight)//2# + (h - total_text_height) // 4
    
    # Draw each line of translated text
    for line in lines:
        print(line)
        # Calculate text width to center it horizontally
        text_width, text_height = draw.textsize(line,font=font_pillow)

        x_centered = x + (w - text_width) // 2

        draw = ImageDraw.Draw(image_pillow)
        draw.text((x_centered,y_start), line, font=font_pillow, fill=font_color)
        y_start += int(text_height * 1.2)  # Move to the next line
    print()


def main(inputPath, outputPath, ifGPT):
    image, gray_image = readImage(inputPath)
    textData = extractData(gray_image)

    baloonTexts = getNecesseryBaloons(textData);

    for i in baloonTexts:
        removeBlanks(image, baloonTexts)
        #drawBorderRectangle(image,baloonTexts[i].border_box)

    image_pillow = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    for i in baloonTexts:
        baloonText :BaloonText = baloonTexts[i]

        if ifGPT:
            baloonText.translatedText = translate_GPT(baloonText.text, "tr").capitalize()
        else:
            baloonText.translatedText =  translate_text(baloonText.text, "tr").capitalize()

        #drawBorderRectangle(image, baloonText.border_box)

        overlayBaloonText(image_pillow,baloonText)
        
        """print(baloonText.text)
        print(baloonText.translatedText)
        print()
        """

    image_pillow.save(outputPath)


if __name__ == "__main__":
    inputPath = sys.argv[1]
    outputPath = sys.argv[2]
    is_GPT = bool(int(sys.argv[3]))

    main(inputPath, outputPath, is_GPT)