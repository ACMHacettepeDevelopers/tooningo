from PIL import Image
from ultralytics import YOLO

# Load the YOLO model
model = YOLO('best.pt')

# Path to the input image
image_path = '../Test/testfile2.png'

# Perform object detection
results = model(image_path)

for r in results:
    im_array = r.plot()
    im = Image.fromarray(im_array)
    im.save('output.png')


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