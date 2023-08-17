import cv2
import pytesseract
from googletrans import Translator
from unidecode import unidecode
import numpy as np

# Read the image
image = cv2.imread('Test/toontest.png')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply edge detection
edges = cv2.Canny(gray_image, threshold1=30, threshold2=100)
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Find the largest contour (assumed to be the speech balloon)
largest_contour = max(contours, key=cv2.contourArea)

# Create an elliptical mask for the speech balloon
ellipse_mask = np.zeros_like(gray_image)
cv2.drawContours(ellipse_mask, [largest_contour], -1, 255, thickness=cv2.FILLED)

# Fill the interior of the mask with white
output_image = image.copy()
output_image[ellipse_mask == 255] = 255

# Define the region of the speech balloon
x, y, w, h = cv2.boundingRect(largest_contour)
balloon_region = gray_image[y:y+h, x:x+w]

# Perform OCR on the balloon region
text = pytesseract.image_to_string(balloon_region)
text = text.replace('\n', ' ')

# Translate the text
translator = Translator()
translated_text = translator.translate(text, src='auto', dest='tr').text
translated_text = unidecode(translated_text)

# Prepare to fit the text into the speech balloon
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_color = (0, 0, 0)  # Black color
line_type = 2

# Adjust starting position for text placement
x, y = x, y + (h//2)
char_width, char_height = cv2.getTextSize("A", font, font_scale, line_type)[0]

# Wrap the translated text to fit inside the balloon
text_lines = translated_text.split(" ")
wrapped_text = []
current_line = ""
for word in text_lines:
    test_line = current_line + " " + word if current_line else word
    width, _ = cv2.getTextSize(test_line, font, font_scale, line_type)[0]

    if width + 50 <= w:
        current_line = test_line
    else:
        wrapped_text.append(current_line)
        current_line = word
wrapped_text.append(current_line)

# Place the wrapped text inside the balloon region
y_offset = 0
for line in wrapped_text:
    width, height = cv2.getTextSize(line, font, font_scale, line_type)[0]
    cv2.putText(output_image, line, (x + int((w - width) / 2), y + y_offset), font, font_scale, font_color, line_type)
    y_offset += height + 10

# Save the output image
output_path = "Test/translated_toon.png"
cv2.imwrite(output_path, output_image)
