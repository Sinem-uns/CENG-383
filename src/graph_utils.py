import random


def create_test_graph():
    return {
        0: [(1, 4), (2, 1)],
        1: [(3, 1)],
        2: [(1, 2), (3, 5)],
        3: []
    }


def generate_random_graph(num_nodes, edge_probability=0.1, min_weight=1, max_weight=10):
    # BUG FIX 1: Default edge_probability was 0.2 in the function signature but
    # benchmark.py always passed 0.1 explicitly. Using 0.2 by default produced
    # significantly denser graphs than what was benchmarked, making the default
    # misleading. Unified to 0.1.

    # BUG FIX 2: The original generator could produce completely disconnected
    # graphs at low edge_probability (e.g. 7 out of 10 nodes unreachable at
    # probability 0.05). This makes benchmarks meaningless because most
    # shortest-path distances are inf. We now guarantee a spanning path
    # 0->1->2->...->n-1 so every node is reachable from node 0.
    graph = {i: [] for i in range(num_nodes)}

    # Guarantee connectivity: add a directed spanning chain first.
    for i in range(num_nodes - 1):
        weight = random.randint(min_weight, max_weight)
        graph[i].append((i + 1, weight))

    # Add random additional edges (skip if already covered by the chain).
    existing = {(i, i + 1) for i in range(num_nodes - 1)}
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j and (i, j) not in existing and random.random() < edge_probability:
                weight = random.randint(min_weight, max_weight)
                graph[i].append((j, weight))

    return graph
