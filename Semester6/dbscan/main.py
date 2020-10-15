import random
from typing import Dict, Iterable, List, Set

from point2d import Point2D


def get_random_points(count: int, min_x: int, max_x: int, min_y: int, max_y: int) -> List[Point2D]:
	points = list()
	for _ in range(0, count):
		x = random.uniform(min_x, max_x)
		y = random.uniform(min_y, max_y)
		points.append(Point2D(x, y))
	return points


def get_neighbors(
		points: Iterable[Point2D],
		point: Point2D,
		max_neighbor_distance: float) -> Iterable[Point2D]:
	return filter(
		lambda neighbor: (neighbor - point).r < max_neighbor_distance,
		points)


def color_green_points(
		points: Iterable[Point2D],
		max_neighbor_distance: float,
		min_neighbor_count_in_cluster: int) -> Set[Point2D]:
	green_points = set()
	points_list = list(points)

	for point in points_list:
		neighbors = list(get_neighbors(points_list, point, max_neighbor_distance))
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


def clusterize(
		points: Iterable[Point2D],
		green_points: Set[Point2D],
		yellow_points: Set[Point2D],
		max_neighbor_distance: float) -> Dict[Point2D, int]:
	def get_new_cluster_id() -> int:
		return last_cluster_id + 1 if last_cluster_id is not None else 0

	last_cluster_id = None
	point_to_cluster_map = {}

	for point in points:
		if point not in point_to_cluster_map:
			last_cluster_id = get_new_cluster_id()
			point_to_cluster_map[point] = last_cluster_id

		if point not in green_points:
			continue

		current_cluster_id = point_to_cluster_map[point]
		neighbors = get_neighbors(points, point, max_neighbor_distance)
		neighbors_clusters_ids = set(filter(
			lambda x: x is not None,
			(point_to_cluster_map.get(neighbor) for neighbor in neighbors)))
		neighbors_clusters_points = list(filter(
			lambda neighbor: point_to_cluster_map.get(neighbor) in neighbors_clusters_ids,
			points))
		for neighbor in neighbors_clusters_points:
			point_to_cluster_map[neighbor] = current_cluster_id

	return point_to_cluster_map


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

	point_to_cluster_map = clusterize(
		points,
		green_points,
		yellow_points,
		max_neighbor_distance)


if __name__ == '__main__':
	main(100, -100, 100, -100, 100, 15, 2)
