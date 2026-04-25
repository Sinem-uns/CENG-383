"""Utilities for loading DIMACS shortest-path graph files."""

from __future__ import annotations

import gzip
from pathlib import Path
from typing import Dict, List, Tuple

Graph = Dict[int, List[Tuple[int, int]]]


def _open_text(path: Path):
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8")
    return open(path, "r", encoding="utf-8")


def load_dimacs_graph(file_path: str | Path) -> Graph:
    """Load a directed weighted graph from a DIMACS .gr or .gr.gz file.

    DIMACS road-network files contain lines of the form:
      c ...            comments
      p sp <n> <m>     problem definition
      a <u> <v> <w>    directed arc with weight w

    Important: edge weights are preserved exactly as provided by the dataset.
    Changing or normalizing them would make the experiment less faithful.
    """
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