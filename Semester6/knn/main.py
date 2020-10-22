import random
from typing import Dict, List

from point2d import Point2D


def get_training_points() -> Dict[int, List[Point2D]]:
	raise NotImplementedError()


def get_random_points(count: int, min_x: int, max_x: int, min_y: int, max_y: int) -> List[Point2D]:
	points = list()
	for _ in range(0, count):
		x = random.uniform(min_x, max_x)
		y = random.uniform(min_y, max_y)
		points.append(Point2D(x, y))
	return points


def classify(
		existing_points: Dict[int, List[Point2D]],
		new_points: List[Point2D]) -> Dict[int, List[Point2D]]:
	raise NotImplementedError()


def draw(existing_points: Dict[int, List[Point2D]], classified_new_points: Dict[int, List[Point2D]]):
	raise NotImplementedError()


def main():
	existing_points = get_training_points()
	draw(existing_points, {})

	new_points = get_random_points(25, -100, 100, -100, 100)
	classified_new_points = classify(existing_points, new_points)

	draw(existing_points, classified_new_points)


if __name__ == '__main__':
	main()
