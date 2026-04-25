"""Benchmark helpers for SSSP algorithms."""

from __future__ import annotations

import csv
import gc
import os
import time
import tracemalloc

from bellman_ford import bellman_ford
from dijkstra import dijkstra
from bmssp_like import bmssp_like
from graph_utils import generate_random_graph


ALGORITHMS = [
    ("Dijkstra", dijkstra),
    ("Bellman-Ford", bellman_ford),
    ("BMSSP-like", bmssp_like),
]


def measure_algorithm(algorithm, graph, start):
    gc.collect()
    tracemalloc.start()

    start_time = time.perf_counter()
    result = algorithm(graph, start)
    runtime = time.perf_counter() - start_time

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return max(runtime, 1e-7), peak, result


def average_measurement(algorithm, graph, start, repeats=3):
    times = []
    memories = []
    last_result = None

    for _ in range(repeats):
        runtime, memory, last_result = measure_algorithm(algorithm, graph, start)
        times.append(runtime)
        memories.append(memory)

    avg_time = sum(times) / len(times)
    avg_memory = sum(memories) / len(memories)

    return avg_time, avg_memory, last_result


def count_edges(graph):
    return sum(len(neighbors) for neighbors in graph.values())


def verify_against_reference(graph, start, algorithms=ALGORITHMS):
    reference = dijkstra(graph, start)

    for name, algorithm in algorithms:
        result = algorithm(graph, start)

        if result != reference:
            raise AssertionError(f"{name} result does not match Dijkstra")

    return True


def run_random_benchmarks():
    graph_sizes = [10, 50, 100, 200, 400]
    results = []

    for size in graph_sizes:
        graph = generate_random_graph(size, edge_probability=0.1)
        start_node = 0

        verify_against_reference(graph, start_node)

        for name, algorithm in ALGORITHMS:
            runtime, memory, _ = average_measurement(
                algorithm,
                graph,
                start_node
            )

            results.append({
                "graph_type": "Random",
                "nodes": size,
                "edges": count_edges(graph),
                "algorithm": name,
                "time_seconds": runtime,
                "memory_bytes": int(memory),
            })

    return results


def save_results_to_csv(results, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "graph_type",
                "nodes",
                "edges",
                "algorithm",
                "time_seconds",
                "memory_bytes",
            ],
        )

        writer.writeheader()
        writer.writerows(results)