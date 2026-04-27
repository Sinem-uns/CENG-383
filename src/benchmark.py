"""Benchmark helpers for SSSP algorithms."""

from __future__ import annotations

import csv
import gc
import time
import tracemalloc
from pathlib import Path

from bellman_ford import bellman_ford
from dijkstra import dijkstra
from bmssp_like import bmssp_like
from graph_utils import generate_random_graph


ALGORITHMS = [
    ("Dijkstra", dijkstra),
    ("Bellman-Ford", bellman_ford),
    ("BMSSP-like", bmssp_like),
]


def measure_runtime(algorithm, graph, start, repeats=7):
    """
    Return the median runtime over `repeats` runs.

    BUG FIX 1 — separated runtime and memory passes:
      Running tracemalloc during timing adds disproportionate per-allocation
      overhead that is larger for small graphs than large ones, producing
      non-monotone runtime curves. Runtime and memory are now measured in
      separate passes.

    BUG FIX 2 — warmup run:
      The first call on a new graph is slower due to Python bytecode
      interpretation and CPU cache cold-start. One warmup run before timing
      ensures steady-state performance is measured.

    BUG FIX 3 — median instead of mean:
      The mean is skewed by occasional OS scheduler interruptions (seen as
      10-15ms spikes in otherwise sub-1ms measurements). The median is robust
      to these outliers and produces a smooth, monotone curve.
    """
    # Warmup
    gc.collect()
    result = algorithm(graph, start)

    # Timed runs
    times = []
    for _ in range(repeats):
        gc.collect()
        t0 = time.perf_counter()
        algorithm(graph, start)
        times.append(time.perf_counter() - t0)

    times.sort()
    median = times[repeats // 2]
    return max(median, 1e-7), result


def measure_memory(algorithm, graph, start):
    """Return peak heap memory via tracemalloc (separate from timing)."""
    gc.collect()
    tracemalloc.start()
    algorithm(graph, start)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak


def average_measurement(algorithm, graph, start, repeats=3):
    """
    Public interface used by main.py and benchmark tests.
    Returns (median_runtime, peak_memory, last_result).
    The `repeats` parameter is kept for API compatibility but the internal
    timing already runs 7 sub-repetitions and takes the median.
    """
    runtime, result = measure_runtime(algorithm, graph, start)
    memory = measure_memory(algorithm, graph, start)
    return runtime, memory, result


def count_edges(graph):
    return sum(len(neighbors) for neighbors in graph.values())


def verify_against_reference(graph, start, algorithms=ALGORITHMS):
    reference = dijkstra(graph, start)
    for name, algorithm in algorithms:
        if name == "Dijkstra":
            continue
        result = algorithm(graph, start)
        if result != reference:
            raise AssertionError(f"{name} result does not match Dijkstra reference")
    return True


def run_random_benchmarks():
    graph_sizes = [10, 50, 100, 200, 400]
    results = []
    for size in graph_sizes:
        graph = generate_random_graph(size, edge_probability=0.1)
        start_node = 0
        verify_against_reference(graph, start_node)
        for name, algorithm in ALGORITHMS:
            runtime, memory, _ = average_measurement(algorithm, graph, start_node)
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
    parent = Path(filename).parent
    if str(parent) not in ("", "."):
        parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "graph_type", "nodes", "edges", "algorithm",
            "time_seconds", "memory_bytes",
        ])
        writer.writeheader()
        writer.writerows(results)
