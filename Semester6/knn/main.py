import math
import random
from itertools import islice
from typing import Dict, List, Tuple

import matplotlib.pyplot as plot
import numpy
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


def get_best_matching_cluster(nearest_neighbors: List[Tuple[int, float]]) -> int:
	cluster_to_neighbors_count_map = {}
	best_matching_cluster = None
	for cluster, _ in nearest_neighbors:
		if cluster not in cluster_to_neighbors_count_map:
			cluster_to_neighbors_count_map[cluster] = 0
		cluster_to_neighbors_count_map[cluster] += 1

		if best_matching_cluster is None:
			best_matching_cluster = cluster
		else:
			best_matching_cluster = cluster \
				if cluster_to_neighbors_count_map[cluster] > cluster_to_neighbors_count_map[best_matching_cluster] \
				else best_matching_cluster
	return best_matching_cluster


def classify(
		existing_points: Dict[int, List[Point2D]],
		new_points: List[Point2D]) -> Dict[int, List[Point2D]]:
	existing_points_count = sum(len(cluster) for cluster in existing_points.values())
	neighbors_count = int(math.floor(math.sqrt(existing_points_count)))

	classified_points = {}
	all_neighbors = [(cluster[0], point) for cluster in existing_points.items() for point in cluster[1]]
	for point in new_points:
		distances_to_existing_points = sorted(
			[(neighbor[0], (neighbor[1] - point).r) for neighbor in all_neighbors],
			key = lambda neighbor: neighbor[1])
		nearest_neighbors = list(islice(distances_to_existing_points, neighbors_count))

		best_matching_cluster = get_best_matching_cluster(nearest_neighbors)

		if best_matching_cluster not in classified_points:
			classified_points[best_matching_cluster] = []
		classified_points[best_matching_cluster].append(point)

	return classified_points


def draw(
		existing_points: Dict[int, List[Point2D]],
		classified_new_points: Dict[int, List[Point2D]],
		min_x: int,
		max_x: int,
		min_y: int,
		max_y: int):
	figure, axis = plot.subplots()
	axis.set_xlim([min_x, max_x])
	axis.set_ylim([min_y, max_y])

	colors = plot.rcParams["axes.prop_cycle"].by_key()["color"]
	for i, cluster in enumerate(existing_points.keys()):
		color = colors[i % len(colors)]
		points = existing_points[cluster] + classified_new_points.get(cluster, [])
		axis.scatter([point.x for point in points], [point.y for point in points], color = color)

		cluster_center = Point2D(
			numpy.mean(numpy.array([point.x for point in points])),
			numpy.mean(numpy.array([point.y for point in points])))
		cluster_radius = numpy.max([(point - cluster_center).r for point in points])
		circle = plot.Circle((cluster_center.x, cluster_center.y), cluster_radius, color = color, fill = False)
		axis.add_artist(circle)

	plot.show()


def main():
	existing_points = get_training_points()
	draw(existing_points, {}, -110, 110, -110, 110)

	new_points = get_random_points(25, -100, 100, -100, 100)
	classified_new_points = classify(existing_points, new_points)

	draw(existing_points, classified_new_points, -110, 110, -110, 110)


if __name__ == '__main__':
	main()
