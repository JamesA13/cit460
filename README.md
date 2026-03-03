# cit460

This project is a Python program that uses Computer Vision technology to provide business support functions to a retail establishment.

Its core features will ultimately include:
 -the ability for cameras to observe the shelving units throughout the store and identify when an item is low on stock, prompting an alert that management can review at their convenience without having to send an employee to visually identify where a restock is required. 

-the ability to identify when an incorrect item has been placed on a shelf among other objects, again generating an alert for management to become aware of the need to reorganize. 

-tracking foot traffic throughout the store, providing data (likely via heatmap) about what departments are popular over time periods such as day, week, or month

The basic Computer Vision functionality is provided by OpenCV, an open-source computer vision library that has been in operation since 2000.
https://opencv.org/about/
`pip install opencv-python`

Rather than set up machine learning training on personal objects, at time of writing this project is implementing Ultralytics YOLO, another open-source library that includes some pre-trained datasets to get the project up and running quickly with the knowledge of what objects like people, chairs, and drink receptacles.
https://www.ultralytics.com/about
https://docs.ultralytics.com/
`pip install ultralytics`

At time of writing, the backend responsible for handling this information is Google Firestore, a Cloud-based, Document NoSQL platform offered by Google through the Firebase ecosystem.
https://firebase.google.com/docs/reference
`pip install google-cloud-firestore` and `pip install firebase_admin`

With experience implementing Firestore in a React application, a brief YouTube tutorial by user "Code First with Hala" was extremely helpful in establishing the syntax differences with a Python app.
https://www.youtube.com/playlist?list=PLs3IFJPw3G9LW-rGJ8EBMaCd8OxGm_qQe

Method in app.py to draw boxes around detected objects with color shamelessly 'inspired' by the implementation in this YouTube video by user "Michael Reeves":
https://youtu.be/oA85M9JHsW0?si=G7-bTp3-tkTRBJZw