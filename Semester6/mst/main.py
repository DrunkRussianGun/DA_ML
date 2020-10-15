import random

import numpy
from numpy import ndarray


def main():
	vertices_count = 20
	clusters_count = 3
	graph = get_random_graph(vertices_count)
	spanning_tree = get_minimum_spanning_tree(graph)
	clusters = clusterize(spanning_tree, clusters_count)
	draw(clusters)


def get_random_graph(vertices_count: int) -> ndarray:
	graph = numpy.zeros((vertices_count, vertices_count))
	for i in range(vertices_count):
		for j in range(i + 1, vertices_count):
			graph[i, j] = random.uniform(0, 100)
	return graph


def get_minimum_spanning_tree(graph: ndarray) -> ndarray:
	raise NotImplementedError()


def clusterize(minimum_spanning_tree: ndarray, clusters_count: int) -> ndarray:
	raise NotImplementedError()


def draw(graph: ndarray):
	raise NotImplementedError()


if __name__ == '__main__':
	main()
