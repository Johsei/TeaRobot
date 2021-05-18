print('Cup Recognition System Initializing...')

import cv2
import torch
from PIL import Image
import torch.backends.cudnn as cudnn

# Load Model with custom weights
model = torch.hub.load('ultralytics/yolov5', 'custom', path='weights_cups.pt')

# initialize the camera and grab a reference to the raw camera capture
cap = cv2.VideoCapture(0)

#Check if camera was opened correctly
if not (cap.isOpened()):
    print("Could not open video device")

#Set the resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

img = cap.read()

# Model Settings
model.conf = 0.3
# more to come?

# Inference
results = model(img, size=416)  # includes NMS

# Results
results.print()
results.save()  # or .show()

results.xyxy[0]  # img1 predictions (tensor)
results.pandas().xyxy[0]  # img1 predictions (pandas)


# Release Camera
cap.release()
