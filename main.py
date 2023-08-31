import cv2
import pytesseract
from googletrans import Translator
from unidecode import unidecode
import re
from PIL import Image, ImageDraw, ImageFont
import sys
import gpt
import numpy as np
from collections import Counter
import yolo_bubble_detection as yolo
import BubbleBox  as bb

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



# Read the image
def readImage(path):
    """Read image and convert it to grayscale"""
    image = cv2.imread(path)
    return image
    """
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    invert = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    gray_image = 255 - invert
    return image, gray_image
    """
    

def fillBubbles(image,bubbleBoxs:list):
    for bubbleBox in bubbleBoxs :
        if bubbleBox.shape.lower() == "elipse":
            drawElipse(image,bubbleBox)
        elif bubbleBox.shape.lower() == "sea_uchirin":
            drawElipse(image,bubbleBox)
        else:
            drawRectangle(image,bubbleBox)


def drawRectangle(image,bubbleBox:bb.BubbleBox):
    x, y, w, h = getBorderProps(bubbleBox)
    # Extract the region covered by the bubble
    bubble_region = getBubble(image,bubbleBox)
    
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


def drawElipse(image,bubbleBox:bb.BubbleBox):
    x,y,w,h = getBorderProps(bubbleBox)

    center = (x+w//2, y+h//2)

    # Elipsin eksen uzunlukları (büyük yarıçap, küçük yarıçap)
    axes = (w//2, h//2)

    # Elipsin dönme açısı
    angle = 0

    # Elipsin çizgi rengi (beyaz)
    color = (255, 255, 255)

    # Elipsin kalınlığı (-1 ise içini doldurur)
    thickness = -1

    # Elipsi çiz
    cv2.ellipse(image, center, axes, angle, 0, 360, color, thickness)


def getBubble(image,bubbleBox:bb.BubbleBox):
    return image[bubbleBox.coordinates.y1:bubbleBox.coordinates.y2,bubbleBox.coordinates.x1:bubbleBox.coordinates.x2]

def getBubbleBoxText(image,bubbleBox:bb.BubbleBox, lang="eng"):

    bubble = getBubble(image,bubbleBox)
    text = pytesseract.image_to_string(bubble,lang=lang)
    text = text.replace("\n"," ")
    return text

def getBorderProps(bubbleBox:bb.BubbleBox):
    x, y = bubbleBox.coordinates.x1, bubbleBox.coordinates.y1,
    w = abs(bubbleBox.coordinates.x1-bubbleBox.coordinates.x2)
    h = abs(bubbleBox.coordinates.y1-bubbleBox.coordinates.y2)
    return x,y,w,h


def overlayBubbleText(image_pillow, bubbleBox:bb.BubbleBox):
    """Overlay translated text on the image"""

    font_size= 30
    font_color = (0, 0, 0) 
    font_pillow = ImageFont.truetype("Tahoma", font_size)

    draw = ImageDraw.Draw(image_pillow)

    
    x,y,w,h = getBorderProps(bubbleBox)
    
    # Split translated_text into lines that fit within the text region
    lines = []
    current_line = ""
    words = bubbleBox.translated_text.split()

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
        text_height = draw.textsize(i, font=font_pillow)[1]
        totalHeight += text_height
    # Calculate total height of the lines

    # Calculate starting y-coordinate for centering the text
    y_start = y + (h-totalHeight)//2# + (h - total_text_height) // 4
    
    # Draw each line of translated text
    for line in lines:
        # Calculate text width to center it horizontally
        text_width, text_height = draw.textsize(line,font=font_pillow)

        x_centered = x + (w - text_width) // 2

        draw = ImageDraw.Draw(image_pillow)
        draw.text((x_centered,y_start), line, font=font_pillow, fill=font_color)
        y_start += int(text_height * 1.2)  # Move to the next line


def main(inputPath, outputPath, ifGPT):
    image = readImage(inputPath)

    process_img = yolo.getResizedImage(image,640)

    # Get speech bubbles
    bubbleBoxes = yolo.getBubbleBoxes(process_img)

    # Get texts in bubbles and translate them
    for bubbleBox in bubbleBoxes:

        bubbleBox: bb.BubbleBox = bubbleBox
        bubbleBox.text = getBubbleBoxText(process_img,bubbleBox)

        if ifGPT:
            bubbleBox.translated_text = translate_GPT(bubbleBox.text, "tr").capitalize()
        else:
            bubbleBox.translated_text =  translate_text(bubbleBox.text, "tr").capitalize()

    # Fill Speech Bubbles
    fillBubbles(process_img,bubbleBoxes)   

    # Write translated texts on image
    process_img_pillow = Image.fromarray(cv2.cvtColor(process_img, cv2.COLOR_BGR2RGB))
    for bubbleBox in bubbleBoxes:
        overlayBubbleText(process_img_pillow,bubbleBox)

    # Save image
    new_image = np.array(process_img_pillow)
    new_image = yolo.getResizedImage(new_image,image.shape[1])

    cv2.imwrite(outputPath,new_image)


if __name__ == "__main__":
    inputPath = sys.argv[1]
    outputPath = sys.argv[2]
    is_GPT = bool(int(sys.argv[3]))

    main(inputPath, outputPath, is_GPT)