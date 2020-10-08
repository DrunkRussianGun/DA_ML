from math import inf
from typing import Dict, List, Tuple

from point2d import Point2D


def import_module(name: str, file_path: str):
	import importlib.util
	spec = importlib.util.spec_from_file_location(name, file_path)
	return spec.loader.load_module(name)


kmeans = import_module("kmeans", "../kmeans/entry_point.py")
# noinspection PyUnresolvedReferences
from kmeans import\
	get_random_points,\
	get_initial_clusters,\
	clusters_groups_are_same,\
	sum_distances_from_points_to_clusters_centers,\
	draw

points_count = 100
fuzzy_coefficient = 1.5 # должен быть больше 1


# Возвращает матрицу вероятностей, в которой точки расположены по строкам, а кластеры — по столбцам
def get_probabilities_matrix(points: List[Point2D], clusters: List[Point2D])\
		-> Dict[Tuple[Point2D, Point2D], float]:
	matrix = {}
	for point in points:
		for cluster in clusters:
			numerator = (point - cluster).r
			exponent = 2 / (1 - fuzzy_coefficient)
			matrix[(point, cluster)] = sum(
				(numerator / (point - cluster_to_sum).r) ** exponent
				for cluster_to_sum in clusters)
	return matrix


def get_clusters(probabilities_matrix: Dict[Tuple[Point2D, Point2D], float]) -> List[Point2D]:
	cluster_to_points_map = {}
	for (point, cluster), probability in probabilities_matrix.items():
		cluster_to_points_map.setdefault(cluster, []).append((point, probability ** fuzzy_coefficient))
	return list(
		sum((point[1] * point[0] for point in points), start = Point2D())
		* (1 / sum(point[1] for point in points))
		for cluster, points in cluster_to_points_map.items())


# noinspection PyShadowingNames
def group_points_by_clusters(probabilities_matrix: Dict[Tuple[Point2D, Point2D], float])\
		-> Dict[Point2D, List[Point2D]]:
	point_to_cluster_map = {}
	for (point, cluster), probability in probabilities_matrix.items():
		if point not in point_to_cluster_map:
			point_to_cluster_map[point] = cluster
			continue

		most_matching_cluster = point_to_cluster_map[point]
		if probabilities_matrix[(point, most_matching_cluster)] < probability:
			point_to_cluster_map[point] = cluster

	cluster_to_points_map = {}
	for point, cluster in point_to_cluster_map.items():
		cluster_to_points_map.setdefault(cluster, []).append(point)
	return cluster_to_points_map


def clusterize(points: List[Point2D], clusters_count: int) -> Dict[Point2D, List[Point2D]]:
	iterations_count = 1
	previous_clusters = get_initial_clusters(points, clusters_count)
	probabilities_matrix = get_probabilities_matrix(points, previous_clusters)
	current_clusters = get_clusters(probabilities_matrix)
	while not clusters_groups_are_same(points, previous_clusters, current_clusters):
		previous_clusters = current_clusters
		probabilities_matrix = get_probabilities_matrix(points, current_clusters)
		current_clusters = get_clusters(probabilities_matrix)
		iterations_count += 1

	print(f"{clusters_count} clusters, {iterations_count} iterations")
	return group_points_by_clusters(probabilities_matrix)


def clusterize_optimally(points: List[Point2D]) -> Dict[Point2D, List[Point2D]]:
	# noinspection PyShadowingNames
	def clusterize_and_sum_distances(clusters_count: int) -> (Dict[Point2D, List[Point2D]], float):
		clusters = clusterize(points, clusters_count)
		return clusters, sum_distances_from_points_to_clusters_centers(clusters)

	# Оптимизируем функцию (sum(x) - sum(x + 1)) / (sum(x - 1) - sum(x)), где
	# sum(x) — сумма расстояний от каждой из точек до соответствующего ей кластера при количестве кластеров x
	# noinspection PyShadowingNames
	def calculate_optimizing_function(previous_sum: float, current_sum: float, next_sum: float) -> float:
		if previous_sum == current_sum:
			return inf
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


def main():
	points = get_random_points(points_count)
	clusters = clusterize_optimally(points)
	draw(clusters)


if __name__ == '__main__':
	main()
