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

# Create coordinate class and objects
class Coordinates():
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

# IR = Infrared (the thermal camera), ML = Machine Learning (the object detection model) TODO: global variables necessary?
ir_coords = Coordinates()
ml_coords = Coordinates()
ml_size = Coordinates()

# Set default dimensions for IR Cam and RPI Cam
ir_dim = Coordinates(32,32)
ml_dim = Coordinates(416,320) # TODO: Maybe set this to 320x320

def initialize():
	# Load Model with custom weights
	global model
	model = torch.hub.load('ultralytics/yolov5', 'custom', path='weights_cups.pt')

	# Initialize the camera and grab a reference to the raw camera capture
	global rpiCam
	rpiCam = cv2.VideoCapture(0)

	# Check if camera was opened correctly
	if not (rpiCam.isOpened()):
		print("Could not open video device")

	# Set the resolution of the camera
	rpiCam.set(cv2.CAP_PROP_FRAME_WIDTH, ml_dim.x)
	rpiCam.set(cv2.CAP_PROP_FRAME_HEIGHT, ml_dim.y)

	# ML Model Settings
	model.conf = 0.2

	# Start ThermalCam Sensor
	global thermalCam
	thermalCam = Adafruit_AMG88xx()

	# Initialize hotspot detector for ThermalCam
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
	global detector
	detector = cv2.SimpleBlobDetector_create(params)

	sleep(.1)
	print('ThermalCam, hotspot detector, camera and ML model initialized!')

# Standardises the coordinates to 100
def standardizeCoords(x, y, width, height):
	coords_standardized = Coordinates()
	coords_standardized.x = int(100.0 * x / width)
	coords_standardized.y = int(100.0 * y / height)
	return coords_standardized

# Gives the center of two coordinates or the median of two values
def giveCenter(x1, x2):
	if x2 > x1:
		return (x2 - x1) / 2 + x1
	elif x1 > x2:
		return (x1 - x2) / 2 + x2
	else:
		return x1

# Checks if the deviation between two values is bigger than a certain threshold, returns true if not
def checkDeviation(x1, x2):
	threshold = 12
	if x1 > x2:
		if x1 - x2 > threshold:
			return false
		else:
			return true
	elif x2 > x1:
		if x2 - x1 > threshold:
			return false
		else:
			return true
	else:
		return true

def detect(flag_show):
	global ir_coords, ml_coords, ml_size # TODO: Make this non-global

	# --------------------------------- Thermalcam (IR Sensor) detection

	print('\n-- Thermal Camera Detection --')

	# Read pixels, map them to an 8x8 grid
	pixels = thermalCam.readPixels()
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

	# Show window if show flag is set
	if flag_show:
		cv2.imshow("ThermalCam", img_ir)
		cv2.waitKey(0)

	# Detect hotspots
	keypoints = detector.detect(img_ir)

	# Determine successful detection
	ir_success = True
	if len(keypoints) > 1:
			# If multiple hotspots are detected only take the biggest (-> hottest/nearest) one
			tmp = keypoints[0]
			for i in range (1, len(keypoints)):
				if keypoints[i].size > tmp.size:
					tmp = keypoints[i]
				keypoints[0] = tmp
	elif len(keypoints) < 1:
		# No significant hotspots detected
		print('ThermalCam didnt detect any cups!')
		ir_success = False

	if ir_success:
		# Detection successful - Standardize Coordinates
		ir_coords = standardizeCoords(keypoints[0].pt[0], keypoints[0].pt[1], ir_dim.x, ir_dim.y)
		#print('Koordinaten der Tasse: ', ir_coords.x, ir_coords.y)

	#---------------------------- ML model inference

	print('\n-- Machine Learning Inference --')

	ret, img_ml = rpiCam.read()

	if not ret:
		print('Camera didnt return an image! ERROR')

	 # Show Image if flag ist set
	if flag_show:
		cv2.imshow("Raspberry Cam", img_ml)
		cv2.waitKey(0)

	# Inference
	results = model(img_ml, size=416)  # includes NMS

	if flag_show:
		results.render()
		cv2.imshow("Inference Results", results.imgs[0])
		cv2.waitKey(0)

	results_numpy = results.xyxy[0].numpy()[:,:]

	#print(results_numpy)
	#print('Anzahl Tassen:', len(results_numpy))

	# Determine successful detection # TODO: Implement option to detect more than one cup and take the one with the best probability or the one with the IR Hotspot
	ml_success = True
	if len(results_numpy) > 1:
		print('Camera ML Model detected more than one cups!')
		ml_success = False
	elif len(results_numpy) < 1:
		print('Camera ML Model didnt detect any cups!')
		ml_success = False
	else:
		# This checks that the cup is inside the rectangle of the camera and fails if its not TODO: Shouldnt fail when not
		if results_numpy[0,1] > 48 and results_numpy[0,3] > 48 and results_numpy[0,1] < 368 and results_numpy[0,3] < 368:
			results_numpy[0,1] -= 48
			results_numpy[0,3] -= 48
		else:
			ml_success = False

		# One Cup detected - standardize coordinates
		ml_coords = standardizeCoords(giveCenter(results_numpy[0,0], results_numpy[0,2]), giveCenter(results_numpy[0,1], results_numpy[0,3]), 320, 320)
		#print('Koordinaten der Tasse: ', ml_coords.x, ml_coords.y)
		ml_size.x = results_numpy[0,2] - results_numpy[0,0]
		ml_size.y = results_numpy[0,3] - results_numpy[0,1]
		ml_size = standardizeCoords(ml_size.x, ml_size.y, ml_dim.x, ml_dim.y)
		#print('Groesse der Tasse: ', ml_size.x, ml_size.y)

	#--------------------- Combine coordinates, check for deviation
	cup_detected = False
	if ir_success and ml_success:
		if checkDeviation(ir_coords.x, ml_coords.x) and checkDeviation(ir_coords.y, ml_coords.y):
			cup_detected = True
			coords = Coordinates()
			coords.x = giveCenter(ir_coords.x, ml_coords.x)
			coords.y = giveCenter(ir_coords.y, ml_coords.y)
			return cup_detected, coords, ml_size
	else:
		zero = Coordinates()
		return False, zero, zero

def deinitialize():
	# Release camera, close windows
	rpiCam.release()
	cv2.destroyAllWindows()
