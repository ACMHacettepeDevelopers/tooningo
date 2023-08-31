from PIL import Image
from ultralytics import YOLO
import torch
import cv2
import numpy as np
import torchvision.transforms as transforms
import pytesseract
import BubbleBox as bb

def getProcessableImage(image,new_width):

    height = image.shape[0]
    width = image.shape[1]

    new_height = int((height/width) * new_width)

    image = cv2.resize(image, (new_width,new_height))
    return image

def getTensor(image):
    image = image / 255.0  # Piksel değerlerini 0-1 aralığında normalize et
    preprocess = transforms.ToTensor()
    image_tensor = preprocess(image)
    return image_tensor

def getBubbles(image):

    height = processImage.shape[0]

    abs_coordinates= []
    bubbles = []
    new_width = 640
    new_height = 640

    start_line = 0
    while not (start_line >= height):

        curr_img = processImage[start_line:start_line+new_height,:]
        """
        cv2.imshow("Window",curr_img)
        cv2.waitKey(0)
        """
        # Yeni boyutta bir siyah görüntü oluşturun
        new_image = np.zeros((new_height, new_width, 3), dtype=np.uint8)

        # Orjinal resmi yeni görüntünün sol üst köşesine yerleştirin
        new_image[:curr_img.shape[0], :curr_img.shape[1], :] = curr_img
        
        # Perform object detection
        results = model(getTensor(new_image))

        for r in results:
            for box in r.boxes:
                coordinates = box.xyxy[0].tolist()
                print(coordinates)
                for i in range(len(coordinates)):
                    coordinates[i] = int(coordinates[i])
                    if coordinates[i] <0:
                        coordinates[i]= 0    

                # Add Bubble Coordinates
                
                abs_coordinate = bb.Coordinates(
                        x1= coordinates[0],
                        x2 = coordinates[2],
                        y1 = coordinates[1] + start_line,
                        y2 = coordinates[3] + start_line,

                    )
                

                # Add Bubble image
                #bubble = new_image[coordinates[1]:coordinates[3],coordinates[0]:coordinates[2]]

                bubbleBox = bb.BubbleBox(box,start_line,abs_coordinate)
                bubbles.append(bubbleBox)
                """
                cv2.imshow("Window",bubble)
                cv2.waitKey(0)
                """
            #processImage[start_line:start_line+new_height,:] = r.plot()[:curr_img.shape[0], :curr_img.shape[1]]
                
        start_line += new_height
    
    return bubbles

# Load the YOLO model
model = YOLO('YOLO/best.pt')

image_path = 'Test/toontest3.jpg'

# Load and preprocess the image
image = cv2.imread(image_path)

processImage = getProcessableImage(image,640)

bubbles = getBubbles(processImage)


for bubbleBox in bubbles:
    bubbleBox :(bb.BubbleBox) =bubbleBox
    bubble = processImage[bubbleBox.coordinates.y1: bubbleBox.coordinates.y2,bubbleBox.coordinates.x1:bubbleBox.coordinates.x2]
    grey_bubble = cv2.cvtColor(bubble,cv2.COLOR_BGR2GRAY)
    print(pytesseract.image_to_string(grey_bubble))
    
    bubble[:,:,0] = 255
    bubble[:,:,1] = 0
    bubble[:,:,2] = 0
    
img_width = image.shape[1]
new_image = getProcessableImage(processImage,img_width)
    
cv2.imwrite("output.png",new_image) 
    
    


"""
print(coordinates)
for coord in coordinates:
    cv2.rectangle(new_image, (coord[0], coord[1]), (coord[2], coord[3]), (255, 0, 0), thickness=-1)
"""

#combined_image = cv2.vconcat(new_images)
#combined_image = combined_image[:height,:]

"""

# Perform object detection
results = model(image_tensor)

for r in results:
    im_array = r.plot()
    #im = Image.fromarray(im_array)
    #im.save('output.png')
    cv2.imwrite("output.png",image)

def bubbleFinder(image):
    results = model(image)
    
    # Return a list of coordinates of the bubbles in the image
    bubble_coordinates = []

    for r in results:
        for box in r.boxes:
            # Get xyxy coordinates
            coordts = box.xyxy
            coordinates = coordts[0].tolist()
            bubble_coordinates.append(coordinates)

    return bubble_coordinates


print(bubbleFinder(image_path))

"""