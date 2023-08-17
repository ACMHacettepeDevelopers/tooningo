import cv2
import pytesseract
from googletrans import Translator
from unidecode import unidecode

# Initialize the translator
translator = Translator()


def translate_text(text):
    """Translate text from any language to Turkish"""
    text = text.replace('\n', ' ')
    if not text.strip():
        return ""
    translated_text = translator.translate(text, src='auto', dest='tr').text
    translated_text = unidecode(translated_text)
    return translated_text


def readImage(path):
    """Read image and convert it to grayscale"""
    image = cv2.imread(path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image, gray_image


def extractData(gray_image):
    """Extract text data using OCR"""
    text_data = (pytesseract.image_to_data(gray_image, output_type=pytesseract.Output.DICT))
    return text_data


def drawRectangles(image, text_data):
    """Draw rectangles around detected text regions"""
    for i in range(len(text_data['text'])):
        if text_data['text'][i].strip():
            x, y, w, h = text_data['left'][i], text_data['top'][i], text_data['width'][i], text_data['height'][i]
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), thickness=2)


def concatText(text_data):
    """Concatenate neighboring non-blank texts"""
    # If block_num's are same, concatenate text

    for i in range(len(text_data['text'])):
        if text_data['text'][i].strip():
            for j in range(i+1, len(text_data['text'])):
                if text_data['text'][j].strip():
                    if text_data['block_num'][i] == text_data['block_num'][j]:
                        text_data['text'][i] += " " + text_data['text'][j]
                        text_data['text'][j] = ""

    
def removeBlanks(gray_image, image):
    """Remove blank regions from the image"""
    all_text_data = (pytesseract.image_to_data(gray_image, output_type=pytesseract.Output.DICT))
    for i in range(len(all_text_data['text'])):
        if all_text_data['text'][i].strip():
            x, y, w, h = all_text_data['left'][i], all_text_data['top'][i], all_text_data['width'][i], all_text_data['height'][i]
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), thickness=cv2.FILLED)

        
def overlayText(image, text_data):
    """Overlay translated text on the image"""
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = (0, 0, 0) 
    line_type = 2
    
    for i in range(len(text_data['text'])):
        if text_data['text'][i].strip():
            x, y, w, h = text_data['left'][i], text_data['top'][i], text_data['width'][i], text_data['height'][i]
            translated_text = translate_text(text_data['text'][i]).capitalize()

            # Split translated_text into lines that fit within the text region
            lines = []
            current_line = ""
            words = translated_text.split()
            for word in words:
                if cv2.getTextSize(current_line + ' ' + word, font, font_scale, line_type)[0][0] <= w+300:
                    current_line += ' ' + word if current_line else word
                else:
                    lines.append(current_line)
                    current_line = word
            lines.append(current_line)
            
            # Calculate total height of the lines
            total_text_height = len(lines) * int(h * 1.2)
            
            # Calculate starting y-coordinate for centering the text
            y_start = y + (h - total_text_height) // 4
            
            # Draw each line of translated text
            for line in lines:
                # Calculate text width to center it horizontally
                text_width = cv2.getTextSize(line, font, font_scale, line_type)[0][0]
                x_centered = x + (w - text_width) // 4
                
                cv2.putText(image, line, (x_centered, y_start), font, font_scale, font_color, line_type)
                y_start += int(h * 1.2)  # Move to the next line


def saveImage(image, path):
    """Save image to the given path"""
    cv2.imwrite(path, image)


def main():
    # Read image
    image, gray_image = readImage('Test/testfile2.png')

    print(pytesseract.image_to_data(gray_image))

    # Extract data
    text_data = extractData(gray_image)

    # Draw rectangles
    drawRectangles(image, text_data)

    # Concatenate text
    concatText(text_data)

    # Remove blanks
    removeBlanks(gray_image, image)

    # Overlay text
    overlayText(image, text_data)

    # Save image
    saveImage(image, 'Test/testfile2_tesseract.png')


if __name__ == '__main__':
    main()
