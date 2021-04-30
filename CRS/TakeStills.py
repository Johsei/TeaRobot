import numpy as np
import math
import time
from matplotlib import pyplot as plt
from Adafruit_AMG88xx import Adafruit_AMG88xx
from scipy.interpolate import griddata
import cv2
from time import sleep
from picamera import PiCamera
from picamera.array import PiRGBArray

# Initialize Camera and grab reference
camera = PiCamera()
rawCapture = PiRGBArray(camera)

# Start sensor
sensor = Adafruit_AMG88xx()
sleep(.1)

# Read pixels, map them to an 8x8 grid
pixels = sensor.readPixels()
points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j]

# bicubic interpolation of 8x8 grid to make a 32x32 grid
bicubic = griddata(points, pixels, (grid_x, grid_y), method='cubic')
image = np.array(bicubic)
image = np.reshape(image, (32, 32))
#print('Thermal Image has been saved!')
#print(image)
plt.imsave('color_img.jpg', image, vmin=20, vmax=60, cmap=plt.cm.gist_gray)

# Read image into OpenCV
img = cv2.imread("color_img.jpg", cv2.IMREAD_GRAYSCALE)

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Activate filterByColor to only detect bright blobs (cups)
params.filterByColor = True
params.blobColor = 255

# Change thresholds
params.minThreshold = 155
params.maxThreshold = 255
params.thresholdStep = 5

# Filter by Area.
params.filterByArea = False
params.minArea = 4

# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.1

# Filter by Convexity
params.filterByConvexity = False

# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.55
params.maxInertiaRatio = 3.4028234663852886e+38 # infinity

# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector_create(params)

# Detect blobs.
keypoints = detector.detect(img)

# If blobs exist, print  a message and the position
for i in range (0, len(keypoints)):
	x = keypoints[i].pt[0]
	y = keypoints[i].pt[1]
	print('Tasse gefunden bei: ')
	print(x, y)

print('ThermalCam still has been taken!')

# Grab an image from the camera
camera.capture(rawCapture, format="bgr")
img_cam = rawCapture.array
cv2.imwrite("pycam_img.jpg", img_cam)

print('PyCamera still has been taken!')
