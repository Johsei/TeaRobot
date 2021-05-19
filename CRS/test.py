# Create coordinate objects
class Coordinates:
	x = 0
	y = 0

ir_coords = Coordinates()
ml_coords = Coordinates()


# Standardises the coordinates to 100
def standardize_coords(coords, width, height):
	coords_standardized = Coordinates()
	coords_standardized.x = int(100.0 * coords.x / width)
	coords_standardized.y = int(100.0 * coords.y / height)
	return coords_standardized

ir_coords.x = 12
ir_coords.y = 21

coords_s = standardize_coords(ir_coords, 32, 32)

print(coords_s.x, coords_s.y)
