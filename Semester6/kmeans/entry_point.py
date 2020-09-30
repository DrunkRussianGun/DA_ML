import random
from math import pi
from typing import Dict, List

import matplotlib.pyplot as plot
import numpy
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
def get_mean_point(points: List[Point2D]) -> Point2D:
	return Point2D(
		numpy.mean(numpy.array([point.x for point in points])),
		numpy.mean(numpy.array([point.y for point in points])))


# noinspection PyShadowingNames
def get_initial_clusters(points: List[Point2D], clusters_count: int) -> List[Point2D]:
	circle_center = get_mean_point(points)
	circle_radius = numpy.max([(point - circle_center).r for point in points])

	angle_step = pi * 2 / clusters_count
	return list(
		circle_center + Point2D(r = circle_radius, a = angle_step * i)
		for i in range(0, clusters_count))


# noinspection PyShadowingNames
def group_points_by_clusters(points: List[Point2D], clusters: List[Point2D]) -> Dict[Point2D, List[Point2D]]:
	cluster_to_points_map = {}
	for point in points:
		cluster = min(clusters, key = lambda cluster: (cluster - point).r)
		if cluster not in cluster_to_points_map:
			cluster_to_points_map[cluster] = [point]
		else:
			cluster_to_points_map[cluster].append(point)
	return cluster_to_points_map


# noinspection PyShadowingNames
def get_next_clusters(points: List[Point2D], current_clusters: List[Point2D]) -> List[Point2D]:
	current_points_groups = group_points_by_clusters(points, current_clusters)
	return list(
		get_mean_point(points_group)
		for points_group in current_points_groups.values())


# noinspection PyShadowingNames
def clusters_groups_are_same(
		points: List[Point2D],
		first_clusters: List[Point2D],
		second_clusters: List[Point2D]) -> bool:
	first_groups_of_points = list(
		set(points) for points in group_points_by_clusters(points, first_clusters).values())
	second_groups_of_points = list(
		set(points) for points in group_points_by_clusters(points, second_clusters).values())
	for first_group in first_groups_of_points:
		group_is_deleted = False
		for second_group in second_groups_of_points:
			if first_group == second_group:
				first_groups_of_points.remove(first_group)
				second_groups_of_points.remove(second_group)
				group_is_deleted = True
				break

		if not group_is_deleted:
			return False

	return True


# noinspection PyShadowingNames
def clusterize(points: List[Point2D], clusters_count: int) -> Dict[Point2D, List[Point2D]]:
	previous_clusters = get_initial_clusters(points, clusters_count)
	current_clusters = get_next_clusters(points, previous_clusters)
	while not clusters_groups_are_same(points, previous_clusters, current_clusters):
		previous_clusters = current_clusters
		current_clusters = get_next_clusters(points, previous_clusters)

	return group_points_by_clusters(points, current_clusters)


# noinspection PyShadowingNames
def sum_distances_from_points_to_clusters_centers(clusters: Dict[Point2D, List[Point2D]]) -> float:
	return sum(
		sum((point - cluster_center).r for point in points)
		for cluster_center, points in clusters.items())


# noinspection PyShadowingNames
def clusterize_optimally(points: List[Point2D]) -> Dict[Point2D, List[Point2D]]:
	# noinspection PyShadowingNames
	def clusterize_and_sum_distances(clusters_count: int) -> (Dict[Point2D, List[Point2D]], float):
		clusters = clusterize(points, clusters_count)
		return clusters, sum_distances_from_points_to_clusters_centers(clusters)

	# Оптимизируем функцию (sum(x) - sum(x + 1)) / (sum(x - 1) - sum(x)), где
	# sum(x) — сумма расстояний от каждой из точек до соответствующего ей кластера при количестве кластеров x
	# noinspection PyShadowingNames
	def calculate_optimizing_function(previous_sum: float, current_sum: float, next_sum: float) -> float:
		return (current_sum - next_sum) / (previous_sum - current_sum)

	clusters_count = 2
	previous_clusters, previous_sum = clusterize_and_sum_distances(clusters_count - 1)
	current_clusters, current_sum = clusterize_and_sum_distances(clusters_count)
	next_clusters, next_sum = clusterize_and_sum_distances(clusters_count + 1)
	optimizing_function_value = calculate_optimizing_function(previous_sum, current_sum, next_sum)
	next_optimizing_function_value = -1
	while optimizing_function_value > next_optimizing_function_value:
		if next_optimizing_function_value > 0:
			optimizing_function_value = next_optimizing_function_value

		next_next_clusters, next_next_sum = clusterize_and_sum_distances(clusters_count + 2)
		next_optimizing_function_value = calculate_optimizing_function(current_sum, next_sum, next_next_sum)

		previous_clusters, previous_sum = current_clusters, current_sum
		current_clusters, current_sum = next_clusters, next_sum
		next_clusters, next_sum = next_next_clusters, next_next_sum
		clusters_count += 1

	return previous_clusters


# noinspection PyShadowingNames
def draw(clusters: Dict[Point2D, List[Point2D]]):
	figure, axis = plot.subplots()
	x_range = max_x - min_x
	axis.set_xlim([min_x - x_range, max_x + x_range])
	y_range = max_y - min_y
	axis.set_ylim([min_y - y_range, max_y + y_range])

	colors = plot.rcParams["axes.prop_cycle"].by_key()["color"]
	for i, (cluster_center, points) in enumerate(clusters.items()):
		color = colors[i % len(colors)]
		axis.scatter([point.x for point in points], [point.y for point in points], color = color)

		cluster_radius = numpy.max([(point - cluster_center).r for point in points])
		circle = plot.Circle((cluster_center.x, cluster_center.y), cluster_radius, color = color, fill = False)
		axis.add_artist(circle)

	plot.show()


points = get_random_points(points_count)
clusters = clusterize_optimally(points)
draw(clusters)
