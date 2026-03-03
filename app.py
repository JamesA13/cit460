import cv2
from ultralytics import YOLO
import random

model = YOLO('yolo26n.pt')

# Open the default camera
cam = cv2.VideoCapture(0)

# Get the default frame width and height
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter object
print("Please enter a filename for the next recording:")
filename = input()
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(filename + '.mp4', fourcc, 20.0, (frame_width, frame_height))

knownObjects = dict()
def showDetections(img, detections, threshold): #frame, results[list] from model, confidence value: what percent confidence to discard detections
    boxes = detections.boxes

    for box in boxes:

        if float(box.conf[0]) > threshold: #confidence percent for object > set threshold
            objClass = int(box.cls[0])
            if objClass not in knownObjects.keys():
                knownObjects[objClass] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            boxLabel = f'{detections.names[objClass]} {round(float(box.conf[0]))}'
            boxColor = knownObjects[objClass]

            cv2.rectangle(img, (x1, y1), (x2, y2), boxColor, 2)
            (fontW, fontH), baseline = cv2.getTextSize(boxLabel, cv2.FONT_HERSHEY_SIMPLEX, 1, 1)

            cv2.putText(img, boxLabel, (x1 + 10, y1 - baseline + 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 1)

print("Beginning recording for " + filename)
while True:
    ret, frame = cam.read()

    results = model(frame)[0]
    showDetections(frame, results, .6)

    # Write the frame to the output file
    # out.write(frame)

    # Display the captured frame
    cv2.imshow('Camera', frame)
    
    # for r in results:
    #     print(r.boxes)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and writer objects
cv2.destroyAllWindows()
cam.release()
out.release()
# print(results)