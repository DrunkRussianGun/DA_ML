import random
from typing import Dict, Iterable, List, Set

import matplotlib.pyplot as plot
import numpy
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

	for point in yellow_points:
		neighbors = list(get_neighbors(green_points, point, max_neighbor_distance))
		nearest_neighbor = neighbors[min(
			range(len(neighbors)),
			key = lambda i: (neighbors[i] - point).r)]
		point_to_cluster_map[point] = point_to_cluster_map[nearest_neighbor]

	return point_to_cluster_map


def draw(
		clusters: Dict[int, List[Point2D]],
		green_points: Set[Point2D],
		yellow_points: Set[Point2D],
		red_points: Set[Point2D],
		min_x: int,
		max_x: int,
		min_y: int,
		max_y: int):
	figure, axis = plot.subplots()
	axis.set_xlim([min_x, max_x])
	axis.set_ylim([min_y, max_y])

	colors = plot.rcParams["axes.prop_cycle"].by_key()["color"]
	for i, (cluster_id, points) in enumerate(clusters.items()):
		cluster_color = colors[i % len(colors)]
		cluster_center = Point2D(
			numpy.mean(numpy.array([point.x for point in points])),
			numpy.mean(numpy.array([point.y for point in points])))
		cluster_radius = numpy.max([(point - cluster_center).r for point in points])
		cluster = plot.Circle(
			(cluster_center.x, cluster_center.y),
			cluster_radius,
			color = cluster_color,
			fill = False)
		axis.add_artist(cluster)

	def draw_points(points: Set[Point2D], color: str):
		axis.scatter([point.x for point in points], [point.y for point in points], color = color)

	draw_points(green_points, "g")
	draw_points(yellow_points, "y")
	draw_points(red_points, "r")

	plot.show()


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

	cluster_to_points_map = {}
	for point, cluster in point_to_cluster_map.items():
		cluster_to_points_map.setdefault(cluster, []).append(point)
	draw(
		cluster_to_points_map,
		green_points,
		yellow_points,
		red_points,
		min_x,
		max_x,
		min_y,
		max_y)


if __name__ == '__main__':
	main(100, -100, 100, -100, 100, 15, 2)
