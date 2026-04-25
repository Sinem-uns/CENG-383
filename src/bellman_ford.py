"""Bellman-Ford single-source shortest path algorithm."""

from __future__ import annotations

import math


def bellman_ford(graph, start):
    distances = {node: math.inf for node in graph}
    distances[start] = 0

    edges = [(u, v, w) for u, neighbors in graph.items() for v, w in neighbors]

    # Relax edges up to |V|-1 times. Stop early if a full pass changes nothing.
    for _ in range(len(graph) - 1):
        changed = False
        for u, v, w in edges:
            if distances[u] != math.inf and distances[u] + w < distances[v]:
                distances[v] = distances[u] + w
                changed = True
        if not changed:
            break

    # DIMACS road networks are non-negative, but this keeps the implementation general.
    for u, v, w in edges:
        if distances[u] != math.inf and distances[u] + w < distances[v]:
            raise ValueError("Graph contains a negative-weight cycle")

    return distances