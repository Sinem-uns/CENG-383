"""Utilities for loading DIMACS shortest-path graph files."""

from __future__ import annotations

import gzip
import math
from pathlib import Path
from typing import Dict, List, Tuple

Graph = Dict[int, List[Tuple[int, int]]]


def _open_text(path: Path):
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8")
    return open(path, "r", encoding="utf-8")


def load_dimacs_graph(file_path: str | Path) -> Graph:
    """Load a directed weighted graph from a DIMACS .gr or .gr.gz file."""
    path = Path(file_path)
    graph: Graph = {}

    with _open_text(path) as file:
        for raw_line in file:
            if not raw_line or raw_line.startswith("c"):
                continue
            parts = raw_line.split()
            if not parts:
                continue
            if parts[0] == "p":
                num_nodes = int(parts[2])
                graph = {i: [] for i in range(1, num_nodes + 1)}
            elif parts[0] == "a":
                _, u, v, w = parts
                graph[int(u)].append((int(v), int(w)))

    return graph


def create_induced_subgraph(graph: Graph, max_node_id: int) -> Graph:
    """Return nodes 1..max_node_id with only internal edges kept."""
    return {
        node: [(neighbor, weight) for neighbor, weight in graph[node] if neighbor <= max_node_id]
        for node in graph
        if node <= max_node_id
    }


def find_best_start_node(subgraph: Graph, sample_size: int = 20) -> int:
    """
    BUG FIX: In a directed induced subgraph (nodes 1..N), node 1 is often
    poorly connected — it may reach only a handful of nodes because most of
    its real neighbours have IDs > N and were cut off. Blindly using node 1
    as the source produces near-trivial shortest-path trees (e.g. only 8 out
    of 10,000 nodes reachable in DIMACS-BAY), which makes runtime and memory
    benchmarks meaningless.

    This function samples `sample_size` candidate start nodes spread across
    the subgraph and returns the one that reaches the most nodes. This ensures
    a representative, well-connected source for all algorithms.
    """
    n = max(subgraph.keys())
    # Sample nodes spread evenly, always include node 1 for reproducibility
    step = max(1, n // sample_size)
    candidates = list(range(1, n + 1, step))[:sample_size]

    best_node = candidates[0]
    best_reachable = 0

    for start in candidates:
        if start not in subgraph:
            continue
        # Simple BFS/DFS reachability (no weights needed here)
        visited = set()
        stack = [start]
        while stack:
            u = stack.pop()
            if u in visited:
                continue
            visited.add(u)
            for v, _ in subgraph.get(u, []):
                if v not in visited:
                    stack.append(v)
        if len(visited) > best_reachable:
            best_reachable = len(visited)
            best_node = start

    return best_node
