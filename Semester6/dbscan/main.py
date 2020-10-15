import random
from typing import Iterable, List, Set

from point2d import Point2D


def get_random_points(count: int, min_x: int, max_x: int, min_y: int, max_y: int) -> List[Point2D]:
	points = list()
	for _ in range(0, count):
		x = random.uniform(min_x, max_x)
		y = random.uniform(min_y, max_y)
		points.append(Point2D(x, y))
	return points


def color_green_points(
		points: Iterable[Point2D],
		max_neighbor_distance: float,
		min_neighbor_count_in_cluster: int) -> Set[Point2D]:
	green_points = set()

	for point in points:
		neighbors = list(filter(
			lambda neighbor: (neighbor - point).r < max_neighbor_distance,
			points))
		if len(neighbors) - 1 >= min_neighbor_count_in_cluster:
			green_points.add(point)

	return green_points


def color_yellow_points(
		points: Iterable[Point2D],
		green_points: Set[Point2D],
		max_neighbor_distance: float) -> Set[Point2D]:
	yellow_points = set()

	for point in points:
		if any(filter(
				lambda green_point: (green_point - point).r < max_neighbor_distance,
				green_points)):
			yellow_points.add(point)

	return yellow_points


def main(
		points_count: int,
		min_x: int,
		max_x: int,
		min_y: int,
		max_y: int,
		max_neighbor_distance: float,
		min_neighbor_count_in_cluster: int):
	points = get_random_points(points_count, min_x, max_x, min_y, max_y)
	points_set = set(points)

	green_points = color_green_points(points, max_neighbor_distance, min_neighbor_count_in_cluster)
	yellow_points = color_yellow_points(
		points_set.difference(green_points),
		green_points,
		max_neighbor_distance)
	red_points = points_set.difference(green_points).difference(yellow_points)


if __name__ == '__main__':
	main(100, -100, 100, -100, 100, 15, 2)
