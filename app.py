import cv2
from ultralytics import YOLO
from firebase import firebase
import firebase_admin

cred_obj = firebase_admin.credentials.Certificate("./adv-program-firebase-adminsdk-fbsvc-88f8cc8cbc.json")
firebase_admin.initialize_app(cred_obj)

firebase_admin.firestore()


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



# import cv2
from PIL import Image

# from ultralytics import YOLO

# model = YOLO("yolo26n.pt")
# accepts all formats - image/dir/Path/URL/video/PIL/ndarray. 0 for webcam
# results = model.predict(source="0", show=True)
# results = model.predict(source="folder", show=True)  # Display preds. Accepts all YOLO predict arguments

# from PIL
# im1 = Image.open("bus.jpg")
# results = model.predict(source=im1, save=True)  # save plotted images

# # from ndarray
# im2 = cv2.imread("bus.jpg")
# results = model.predict(source=im2, save=True, save_txt=True)  # save predictions as labels

# # from list of PIL/ndarray
# results = model.predict(source=[im1, im2])