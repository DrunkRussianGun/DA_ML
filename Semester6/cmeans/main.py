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
	draw

points_count = 100


# Возвращает матрицу вероятностей, в которой точки расположены по строкам, а кластеры — по столбцам
def get_probabilities_matrix(points: List[Point2D], clusters: List[Point2D])\
		-> Dict[Tuple[Point2D, Point2D], float]:
	raise NotImplementedError()


def get_clusters(probabilities_matrix: Dict[Tuple[Point2D, Point2D], float]) -> List[Point2D]:
	raise NotImplementedError()


def group_points_by_clusters(probabilities_matrix: Dict[Tuple[Point2D, Point2D], float])\
		-> Dict[Point2D, List[Point2D]]:
	raise NotImplementedError()


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


def main():
	points = get_random_points(points_count)
	clusters = clusterize(points, 3)
	draw(clusters)


if __name__ == '__main__':
	main()
