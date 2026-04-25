import random


def create_test_graph():
    return {
        0: [(1, 4), (2, 1)],
        1: [(3, 1)],
        2: [(1, 2), (3, 5)],
        3: []
    }


def generate_random_graph(num_nodes, edge_probability=0.2, min_weight=1, max_weight=10):
    graph = {i: [] for i in range(num_nodes)}

    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j and random.random() < edge_probability:
                weight = random.randint(min_weight, max_weight)
                graph[i].append((j, weight))

    return graph