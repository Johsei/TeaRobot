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

ret, img = cap.read()

if not ret:
    print('Camera didnt return an image! ERROR')
else:
    print('Camera image sucessfully received.')

# Model Settings
model.conf = 0.3
# more to come?

# Inference
results = model(img, size=416)  # includes NMS

# Results
print('RESULTS:')
results.print()
#results.save()

print(results.pandas().xyxy[0])  # img1 predictions (pandas)

results_numpy = results.xyxy[0].numpy()[:,:]

#print(results_numpy)
print('Anzahl Tassen:', len(results_numpy))

# Release Camera
cap.release()
