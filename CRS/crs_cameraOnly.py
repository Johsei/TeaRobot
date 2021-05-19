print('Cup Recognition System Initializing...')

import cv2
import torch
from PIL import Image
import torch.backends.cudnn as cudnn
import numpy as np
import math
import time
from matplotlib import pyplot as plt
from Adafruit_AMG88xx import Adafruit_AMG88xx
from scipy.interpolate import griddata
from time import sleep

# Load Model with custom weights
model = torch.hub.load('ultralytics/yolov5', 'custom', path='weights_cups.pt')

# Initialize the camera and grab a reference to the raw camera capture
cap = cv2.VideoCapture(0)

# Check if camera was opened correctly
if not (cap.isOpened()):
    print("Could not open video device")

# Set the resolution of the camera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 416)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)

# ML Model Settings
model.conf = 0.2

# Start IR Sensor
sensor = Adafruit_AMG88xx()

sleep(.1)

ret, img = cap.read()

if not ret:
    print('Camera didnt return an image! ERROR')
else:
    print('Camera image sucessfully received.')

# Inference
results = model(img, size=416)  # includes NMS

# Results
print('RESULTS:')
results.print()
results.save()

print(results.pandas().xyxy[0])  # img1 predictions (pandas)

results_numpy = results.xyxy[0].numpy()[:,:]

#print(results_numpy)
print('Anzahl Tassen:', len(results_numpy))

# Release Camera
cap.release()
