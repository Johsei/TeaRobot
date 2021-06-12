import argparse
import serial
import datetime
from scripts.crs import initialize, detect, deinitialize
from scripts.robot import robotMove, robotInit, robotPickup, robotDispose, robotDeinit

def main(args):
	initialize()
	pickup, ser = robotInit()
	pickuptime = 0
	disposetime = 0
	disposed = True

	try:
		while True:
			results = detect(args.show)
			# results[0]: True/False - Cup with hot water detected
			# results[1].x: 0-100 - x-Coordinates of the detected cup
			# results[1].y: 0-100 - y-Coordinates of the detected cup
			# results[2].x: 0-100 - x-Size of the detected cup
			# results[2].y: 0-100 - y-Size of the detected cup
			current_time = datetime.datetime.today()
			print('\nRESULTS: ', results[0], results[1].x, results[1].y, results[2].x, results[2].y)
			if results[0] == True and pickup == False and disposed == True:
				print('\nRoboter holt Teebeutel')
				pickuptime = robotPickup(ser)
				pickup = True
			elif results[0] == True and pickup == True and disposed == True:
				robotMove(results, ser)
			if pickuptime != 0:
				time_difference = (current_time - pickuptime).total_seconds()
				if time_difference > 180:
					disposetime = robotDispose(ser)
					disposed = False
					pickup = False
					pickuptime = 0
			if disposetime != 0:
				time_difference = (current_time - disposetime).total_seconds()
				if time_difference > 120:
					disposed = True
					disposetime = 0
	except KeyboardInterrupt:
		pass

	deinitialize()
	robotDeinit(ser)
	print('\n--- CRS END ---')

if __name__ == "__main__":
	print('--------------------------------------\nCRS V1\n----------------------------------------')

        # Define show flag
	parser = argparse.ArgumentParser()
	parser.add_argument('--show', default=False, action='store_true', help='Shows the camera images on the screen')
	args = parser.parse_args()

	main(args)
