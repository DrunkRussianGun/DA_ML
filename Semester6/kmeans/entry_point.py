import random
from typing import Dict, List

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


# noinspection PyShadowingNames
def get_initial_clusters(points: List[Point2D], clusters_count: int) -> List[Point2D]:
	raise NotImplementedError()


# noinspection PyShadowingNames
def group_points_by_clusters(points: List[Point2D], clusters: List[Point2D]) -> Dict[Point2D, List[Point2D]]:
	raise NotImplementedError()


# noinspection PyShadowingNames
def get_next_clusters(points: List[Point2D], current_clusters: List[Point2D]) -> List[Point2D]:
	raise NotImplementedError()


def clusters_groups_are_same(
		points: List[Point2D],
		first_clusters: List[Point2D],
		second_clusters: List[Point2D]) -> bool:
	raise NotImplementedError()


# noinspection PyShadowingNames
def clusterize(points: List[Point2D], clusters_count: int) -> Dict[Point2D, List[Point2D]]:
	previous_clusters = get_initial_clusters(points, clusters_count)
	current_clusters = get_next_clusters(points, previous_clusters)
	while not clusters_groups_are_same(points, previous_clusters, current_clusters):
		previous_clusters = current_clusters
		current_clusters = get_next_clusters(points, previous_clusters)

	return group_points_by_clusters(points, current_clusters)


points = get_random_points(points_count)
clusters = clusterize(points, 3)
