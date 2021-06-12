import numpy as np
import math
import time
from matplotlib import pyplot as plt
from Adafruit_AMG88xx import Adafruit_AMG88xx
from scipy.interpolate import griddata
import cv2
from time import sleep
from PIL import Image

# Start sensor
sensor = Adafruit_AMG88xx()

sleep(.1)

# Read pixels, convert them to values between 0 and 1, map them to an 8x8 grid
pixels = sensor.readPixels()
points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
grid_x, grid_y = np.mgrid[0:7:8j, 0:7:8j]

bicubic = griddata(points, pixels, (grid_x, grid_y), method='cubic')
image = np.array(bicubic)
print(image)
plt.imsave('color_img8x8.jpg', image)
