import random

import matplotlib.pyplot as plot
import networkx
import numpy
from numpy import ndarray


def main():
	vertices_count = 10
	clusters_count = 3
	graph = get_random_graph(vertices_count)
	clustered_graph = clusterize(graph, clusters_count)
	draw(clustered_graph)


def get_random_graph(vertices_count: int) -> ndarray:
	graph = numpy.zeros((vertices_count, vertices_count))
	for i in range(vertices_count):
		for j in range(i + 1, vertices_count):
			graph[i, j] = random.uniform(0, 100)
	return graph


def clusterize(graph: ndarray, clusters_count: int) -> ndarray:
	# Возьмём отсортированный по невозрастанию список рёбер
	vertices_count = graph.shape[0]
	edges = list(filter(
		lambda edge: graph[edge[0], edge[1]] > 0,
		((i, j)
		for i in range(vertices_count)
		for j in range(i + 1, vertices_count))))
	edges.sort(key = lambda edge: graph[edge[0], edge[1]])

	# Начнём строить минимальное остовное дерево алгоритмом Краскала
	vertix_to_connectivity_component_map = dict(
		(vertix_index, {vertix_index}) for vertix_index in range(vertices_count))
	connectivity_components_count = vertices_count
	tree = numpy.zeros((vertices_count, vertices_count))
	for edge in edges:
		# Если количество компонент связности равно требуемому количеству кластеров,
		# то кластеризация завершена
		if connectivity_components_count == clusters_count:
			break
		from_vertix, to_vertix = edge
		if vertix_to_connectivity_component_map[from_vertix] == vertix_to_connectivity_component_map[to_vertix]:
			break

		tree[from_vertix, to_vertix] = graph[from_vertix, to_vertix]
		vertix_to_connectivity_component_map[from_vertix] = vertix_to_connectivity_component_map[from_vertix]\
			.union(vertix_to_connectivity_component_map[to_vertix])
		vertix_to_connectivity_component_map[to_vertix] = vertix_to_connectivity_component_map[from_vertix]
		connectivity_components_count -= 1

	return tree


def draw(graph: ndarray):
	graph_view = networkx.Graph(strict = False)

	vertices_count = graph.shape[0]
	for i in range(vertices_count):
		graph_view.add_node(i)
	for i in range(vertices_count):
		for j in range(i + 1, vertices_count):
			if graph[i, j] > 0:
				graph_view.add_edge(i, j, weight = "{:.1f}".format(graph[i, j]))

	graph_view_position = networkx.random_layout(graph_view)
	networkx.draw_networkx(graph_view, graph_view_position, with_labels = True)
	edge_labels = networkx.get_edge_attributes(graph_view, "weight")
	networkx.draw_networkx_edge_labels(graph_view, pos = graph_view_position, edge_labels = edge_labels)
	plot.show()


if __name__ == '__main__':
	main()
