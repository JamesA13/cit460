import cv2
from ultralytics import YOLO
import random
from firebase_use import *
from outputs import outputs

model = YOLO('yolo26n.pt')

# Open the default camera
cam = cv2.VideoCapture(0)

# Get the default frame width and height
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter object
# print("Please enter a filename for the next recording:")
# filename = input()
filename = 'test'
print("Please enter the desired object code:")
currentCls = input()
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

def validateInput(input):
    try:
        if int(input) in range(0, 80):
            return True
        else:
            return False
    except:
        return False

#Provide the list output of the model detection method and tally a count of the specified object detected in a given frame
#Method accepts targetCls argument, an integer value corresponding to one of the possible outputs from the detection model
#For brevity, possible outputs are stored in outputs.txt
def trackQuantity(detections, targetCls):
    # targetCls = 39 Class value of 'bottle' detection by Ultralytics
    currentCount = 0

    boxes = detections.boxes
    for box in boxes:
        if int(box.cls[0]) == int(targetCls):
            currentCount += 1

    return currentCount

targetMin = 2

def checkLowQty(detections, minQty, targetCls):
    qoh = trackQuantity(detections, targetCls)
    if qoh <= minQty:
        #generate log
        try:
            update_doc_with_id("qoh_logs", str(targetCls), "qoh", qoh)
            update_doc_with_id("qoh_logs", str(targetCls), "timestamp", datetime.datetime.now())
        except:
            create_doc_with_id("qoh_logs", str(targetCls), {"qoh": qoh, "timestamp": datetime.datetime.now()})
    return
    
def checkIncorrectItem(detections, targetCls):
    boxes = detections.boxes
    for box in boxes:
        if int(box.cls[0]) != targetCls:
            try:
                update_doc_with_id("placement_error_logs", str(targetCls), "timestamp", datetime.datetime.now())
            except:
                create_doc_with_id("placement_error_logs", str(targetCls), {"timestamp": datetime.datetime.now()})
    return

def updateTimestamp():
    try:
        update_doc_with_id("test", "timestamps", "last_check", datetime.datetime.now())
    except:
        create_doc_with_id("test", "timestamps", {"last_check": datetime.datetime.now()})

def updateTimestampCache():
    return read_doc_with_id("test", "timestamps")

last_time = updateTimestampCache()

def runInventoryChecks(detections, minQty, targetCls):
    global last_time
    a = datetime.datetime.now(datetime.timezone.utc)
    b = last_time["last_check"]
    print((datetime.datetime.now(datetime.timezone.utc)).second)
    print(last_time["last_check"].second)

    if (a - b).total_seconds() > (60 * 15): # 15 minutes x 60 seconds = 900 seconds
        update_doc_with_id("test", "timestamps", "last_check", datetime.datetime.now(datetime.timezone.utc))
        last_time = updateTimestampCache()
        print(last_time["last_check"])
        print(last_time["last_check"].second)
        checkLowQty(detections, minQty, targetCls)
        checkIncorrectItem(detections, targetCls)
    else:
        print("False")


while validateInput(currentCls) == False:
    print("Please enter an integer between 0-79")
    currentCls = input()

print("Beginning recording for " + filename)
while True:
    ret, frame = cam.read()

    results = model(frame)[0]
    showDetections(frame, results, .6)

    # Write the frame to the output file
    # out.write(frame)

    # Display the captured frame
    cv2.imshow('Camera', frame)

    runInventoryChecks(results, targetMin, currentCls)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and writer objects
cv2.destroyAllWindows()
cam.release()
out.release()