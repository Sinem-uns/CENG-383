"""Run fair DIMACS benchmarks for the SSSP assignment (NY + BAY datasets)."""

from __future__ import annotations

from pathlib import Path

from benchmark import ALGORITHMS, average_measurement, count_edges, save_results_to_csv, verify_against_reference
from dimacs_parser import create_induced_subgraph, load_dimacs_graph
import math


DATASETS = [
    ("DIMACS-NY",  "USA-road-d.NY.gr",  "USA-road-d.NY.gr.gz"),
    ("DIMACS-BAY", "USA-road-d.BAY.gr", "USA-road-d.BAY.gr.gz"),
]

GRAPH_SIZES = [100, 300, 500, 1000, 2000, 5000, 10000]
BELLMAN_FORD_LIMIT = 1000
REPEATS = 3


def find_consistent_start_node(graph, sizes, max_candidate_id=100):
    """
    Find a single start node (ID <= max_candidate_id) that gives the best
    geometric-mean reachability across ALL subgraph sizes. Using the same
    start node for every size ensures the runtime curve is monotonically
    increasing — different start nodes cause artificial dips because each
    one explores a different portion of the graph.
    """
    best_score, best_node = -1.0, 1

    for candidate in range(1, max_candidate_id + 1):
        scores = []
        for size in sizes:
            sub = create_induced_subgraph(graph, size)
            if candidate not in sub:
                scores.append(0.0)
                continue
            # BFS reachability (unweighted — weights don't matter here)
            stack, visited = [candidate], set()
            while stack:
                u = stack.pop()
                if u in visited:
                    continue
                visited.add(u)
                for v, _ in sub.get(u, []):
                    if v not in visited:
                        stack.append(v)
            scores.append(len(visited) / size)

        # Geometric mean — penalises any size where reachability is near-zero
        geo = math.exp(sum(math.log(max(s, 1e-9)) for s in scores) / len(scores))
        if geo > best_score:
            best_score, best_node = geo, candidate

    return best_node


def run_dataset(dataset_name, data_file, base_dir):
    print(f"\n{'='*60}")
    print(f"Dataset: {dataset_name}")
    print(f"{'='*60}")

    graph = load_dimacs_graph(data_file)

    # One consistent start node for all subgraph sizes
    print("Finding best start node (this may take a moment)...")
    start_node = find_consistent_start_node(graph, GRAPH_SIZES)
    print(f"Using start_node={start_node} for all sizes")

    results = []

    for size in GRAPH_SIZES:
        subgraph = create_induced_subgraph(graph, size)
        edge_count = count_edges(subgraph)

        verification_algorithms = [
            item for item in ALGORITHMS
            if item[0] != "Bellman-Ford" or size <= BELLMAN_FORD_LIMIT
        ]
        verify_against_reference(subgraph, start_node, verification_algorithms)

        print(f"\nGraph size: {size} nodes, {edge_count} edges")
        for name, algorithm in ALGORITHMS:
            if name == "Bellman-Ford" and size > BELLMAN_FORD_LIMIT:
                results.append({
                    "graph_type": dataset_name,
                    "nodes": size,
                    "edges": edge_count,
                    "algorithm": name,
                    "time_seconds": "NA",
                    "memory_bytes": "NA",
                })
                print(f"  {name}: skipped beyond {BELLMAN_FORD_LIMIT} nodes (O(VE) cost)")
                continue

            runtime, memory, _ = average_measurement(algorithm, subgraph, start_node, REPEATS)
            print(f"  {name}: {runtime*1000:.3f}ms, {int(memory / 1024)} KB")
            results.append({
                "graph_type": dataset_name,
                "nodes": size,
                "edges": edge_count,
                "algorithm": name,
                "time_seconds": runtime,
                "memory_bytes": int(memory),
            })

    return results


def main():
    base_dir = Path(__file__).resolve().parents[1]
    all_results = []

    for dataset_name, filename, filename_gz in DATASETS:
        data_file = base_dir / "data" / filename
        if not data_file.exists():
            data_file = base_dir / "data" / filename_gz
        if not data_file.exists():
            print(f"WARNING: {dataset_name} data file not found, skipping.")
            continue

        results = run_dataset(dataset_name, data_file, base_dir)
        all_results.extend(results)

        csv_name = f"fair_dimacs_results_{dataset_name.lower().replace('-', '_')}.csv"
        save_results_to_csv(results, base_dir / "results" / csv_name)
        print(f"\nSaved: results/{csv_name}")

    if all_results:
        save_results_to_csv(all_results, base_dir / "results" / "fair_dimacs_results_all.csv")
        print("\nSaved: results/fair_dimacs_results_all.csv")


if __name__ == "__main__":
    main()
