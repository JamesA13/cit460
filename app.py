import cv2
from ultralytics import YOLO

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


print("Beginning recording for " + filename)
while True:
    ret, frame = cam.read()

    # Write the frame to the output file
    # out.write(frame)

    # Display the captured frame
    cv2.imshow('Camera', frame)
    results = model.predict(source=0, show=True)
    # results[0].show()

    # Press 'q' to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

# Release the capture and writer objects
cv2.destroyAllWindows()
cam.release()
out.release()
# print(results)