print('Cup Recognition System Initializing...')

import sys
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

this = sys.modules[__name__]

# Create coordinate class and objects
class Coordinates():
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

# IR = Infrared (the thermal camera), ML = Machine Learning (the object detection model)
ir_coords = Coordinates()
ml_coords = Coordinates()
ml_size = Coordinates()

# Set default dimensions for IR Cam and RPI Cam
ir_dim = Coordinates(32,32)
ml_dim = Coordinates(416,320) # TODO: Maybe set this to 320x320

# Standardises the coordinates to 100
def standardizeCoords(x, y, width, height):
	coords_standardized = Coordinates()
	coords_standardized.x = int(100.0 * x / width)
	coords_standardized.y = int(100.0 * y / height)
	return coords_standardized

# Gives the center of two coordinates
def giveCenter(x1, x2):
	return (x2 - x1) / 2 + x1

def initialize():

	# Load Model with custom weights
	global model
	model = torch.hub.load('ultralytics/yolov5', 'custom', path='weights_cups.pt')

	# Initialize the camera and grab a reference to the raw camera capture
	global cap
	cap = cv2.VideoCapture(0)

	# Check if camera was opened correctly
	if not (cap.isOpened()):
		print("Could not open video device")

	# Set the resolution of the camera
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, ml_dim.x)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, ml_dim.y)

	# ML Model Settings
	model.conf = 0.2

	# Start Sensor
	global sensor
	sensor = Adafruit_AMG88xx()

	sleep(.1)
	print('Sensor, Camera and ML Model initialized!')

def detect():

	global ir_coords, ml_coords, ml_size

	# --------------------------------- Thermalcam

	# Read pixels, map them to an 8x8 grid
	pixels = sensor.readPixels()
	points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
	grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j]

	# bicubic interpolation of 8x8 grid to make a 32x32 grid
	bicubic = griddata(points, pixels, (grid_x, grid_y), method='cubic')
	img_ir_raw = np.array(bicubic)
	img_ir_raw = np.reshape(img_ir_raw, (ir_dim.x, ir_dim.y))
	#print('Thermal Image has been saved!')
	#print(image)
	plt.imsave('img_thermal.jpg', img_ir_raw, vmin=20, vmax=60, cmap=plt.cm.gist_gray)

	# Read image into OpenCV -> TODO: Make this faster/abandon the step of saving and loading img
	img_ir = cv2.imread("img_thermal.jpg", cv2.IMREAD_GRAYSCALE)

	# Setup SimpleBlobDetector parameters.
	params = cv2.SimpleBlobDetector_Params()

	# Activate filterByColor to only detect bright blobs (cups)
	params.filterByColor = True
	params.blobColor = 255

	# Change thresholds
	params.minThreshold = 100
	params.maxThreshold = 255
	params.thresholdStep = 2

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
	keypoints = detector.detect(img_ir)

	# If blobs exist, print  a message and the position TODO: kann weg
	for i in range (0, len(keypoints)):
		x = keypoints[i].pt[0]
		y = keypoints[i].pt[1]
		print('Tasse gefunden bei: ')
		print(x, y)

	# Determine successful detection
	ir_success = True
	if len(keypoints) > 1:
		print('ThermalCam detected more than one cups!')
		ir_success = False
	elif len(keypoints) < 1:
		print('ThermalCam didnt detect any cups!')
		ir_success = False
	else:
		# One cup detected - Standardize Coordinates
		ir_coords = standardizeCoords(keypoints[0].pt[0], keypoints[0].pt[1], ir_dim.x, ir_dim.y)
	print('IR - Koordinaten der Tasse: ', ir_coords.x, ir_coords.y)

	#---------------------------- Inference

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

	# Determine successful detection # TODO: Implement option to detect more than one cup and take the one with the best probability
	ml_success = True
	if len(results_numpy) > 1:
		print('Camera ML Model detected more than one cups!')
		ml_success = False
	elif len(results_numpy) < 1:
		print('Camera ML Model didnt detect any cups!')
		ml_success = False
	else:
		# One Cup detected - standardize coordinates
		ml_coords = standardizeCoords(giveCenter(results_numpy[0,0], results_numpy[0,2]), giveCenter(results_numpy[0,1], results_numpy[0,3]), ml_dim.x, ml_dim.y)
		print('ML - Koordinaten der Tasse: ', ml_coords.x, ml_coords.y)
		ml_size.x = results_numpy[0,2] - results_numpy[0,0]
		ml_size.y = results_numpy[0,3] - results_numpy[0,1]
		ml_size = standardizeCoords(ml_size.x, ml_size.y, ml_dim.x, ml_dim.y)
		print('ML - Groesse der Tasse: ', ml_size.x, ml_size.y)

def deinitialize():
	# Release Camera
	cap.release()
	print('deinitialized!')
