import random
from typing import List

from point2d import Point2D

points_count = 250
min_x = -100
max_x = 100
min_y = -100
max_y = 100


def read_points_from_file(file: str) -> List[Point2D]:
	raise NotImplementedError()


# noinspection PyShadowingNames
def get_random_points(count: int) -> List[Point2D]:
	points = list()
	for _ in range(0, count):
		x = random.uniform(min_x, max_x)
		y = random.uniform(min_y, max_y)
		points.append(Point2D(x, y))
	return points


points = get_random_points(points_count)
