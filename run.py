import argparse
from scripts.crs import initialize, detect, deinitialize
from scripts.robot import robotControl

def main(args):
	initialize()

	try:
		while True:
			results = detect(args.show)
			# results[0]: True/False - Cup with hot water detected
			# results[1].x: 0-100 - x-Coordinates of the detected cup
			# results[1].y: 0-100 - y-Coordinates of the detected cup
			# results[2].x: 0-100 - x-Size of the detected cup
			# results[2].y: 0-100 - y-Size of the detected cup
			print('\nRESULTS: ', results[0], results[1].x, results[1].y, results[2].x, results[2].y)
			robotControl(results)
	except KeyboardInterrupt:
		pass

	deinitialize()

	print('\n--- CRS END ---')

if __name__ == "__main__":
	print('--------------------------------------\nCRS V1\n----------------------------------------')

        # Define show flag
	parser = argparse.ArgumentParser()
	parser.add_argument('--show', default=False, action='store_true', help='Shows the camera images on the screen')
	args = parser.parse_args()

	main(args)
