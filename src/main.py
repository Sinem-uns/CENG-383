"""Run fair DIMACS benchmarks for the SSSP assignment."""

from __future__ import annotations

from pathlib import Path

from benchmark import ALGORITHMS, average_measurement, count_edges, save_results_to_csv, verify_against_reference
from dimacs_parser import create_induced_subgraph, load_dimacs_graph


def main():
    base_dir = Path(__file__).resolve().parents[1]
    data_file = base_dir / "data" / "USA-road-d.NY.gr"
    if not data_file.exists():
        data_file = base_dir / "data" / "USA-road-d.NY.gr.gz"

    graph = load_dimacs_graph(data_file)
    start_node = 1

    # Bellman-Ford is intentionally limited to moderate sizes because O(VE)
    # becomes impractical on road-network graphs. Dijkstra and Bucket-SSSP are
    # additionally measured on larger inputs for scalability.
    graph_sizes = [100, 300, 500, 1000, 2000, 5000, 10000]
    bellman_ford_limit = 1000
    repeats = 3
    results = []

    for size in graph_sizes:
        subgraph = create_induced_subgraph(graph, size)
        edge_count = count_edges(subgraph)
        print(f"\nGraph size: {size} nodes, {edge_count} edges")

        verification_algorithms = [item for item in ALGORITHMS if item[0] != "Bellman-Ford" or size <= bellman_ford_limit]
        verify_against_reference(subgraph, start_node, verification_algorithms)

        for name, algorithm in ALGORITHMS:
            if name == "Bellman-Ford" and size > bellman_ford_limit:
                results.append({
                    "graph_type": "DIMACS-NY",
                    "nodes": size,
                    "edges": edge_count,
                    "algorithm": name,
                    "time_seconds": "NA",
                    "memory_bytes": "NA",
                })
                print(f"{name}: skipped beyond {bellman_ford_limit} nodes due to O(VE) cost")
                continue

            runtime, memory, _ = average_measurement(algorithm, subgraph, start_node, repeats)
            print(f"{name}: {runtime:.6f}s, {int(memory)} bytes")
            results.append({
                "graph_type": "DIMACS-NY",
                "nodes": size,
                "edges": edge_count,
                "algorithm": name,
                "time_seconds": runtime,
                "memory_bytes": int(memory),
            })

    save_results_to_csv(results, base_dir / "results" / "fair_dimacs_results.csv")


if __name__ == "__main__":
    main()