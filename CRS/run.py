import argparse
from scripts.crs import initialize, detect, deinitialize

def main(args):
	initialize()

	try:
		while True:
			results = detect(args.show)
			print('\nRESULTS: ', results[0], results[1], results[2].x, results[2].y, results[3].x, results[3].y)
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
