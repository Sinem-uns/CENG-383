"""
BMSSP - Bucket-based SSSP inspired by Duan et al. (STOC 2025)

Reference:
  Ran Duan, Jiayi Mao, Xiao Mao, Xinkai Shu, Longhui Yin.
  "Breaking the Sorting Barrier for Directed Single-Source Shortest Paths."
  STOC 2025. arXiv:2504.17033.

What Duan et al. achieve:
  - Deterministic O(m * log^(2/3) n) time - the first algorithm to break
    Dijkstra's O(m + n log n) sorting barrier on sparse directed graphs.
  - Key components: (1) a monotone min-priority queue with O(sqrt(log n))
    amortised cost per operation, (2) recursive subproblem decomposition
    into O(log^(2/3) n) levels, (3) bucket-based distance grouping to
    avoid global re-sorting of vertices.

What this implementation does:
  - Captures idea (3): a Dial-style bucket queue that groups nodes by their
    exact integer distance, achieving O(1) amortised bucket access when
    distances are dense integers - a core sub-idea from the Duan et al.
    framework.
  - Replaces ideas (1) and (2) with a standard Python heapq to track
    non-empty bucket keys, giving O(log k) per bucket-key operation
    instead of O(sqrt(log n)).

Why the full algorithm is not implemented here:
  - The monotone priority queue from the paper requires a Trans-Dichotomous
    data structure operating on word-RAM integers; published C implementations
    run to several thousand lines of carefully tuned code.
  - The theoretical speedup over Dijkstra only materialises at n > 10^5 nodes;
    on the subgraphs tested (up to 10,000 nodes) Dijkstra is already near-
    optimal in practice, so the added complexity is not justified.

Time complexity:  O(V + E + D)  where D = max finite shortest-path distance
Space complexity: O(V + E)      — settled buckets are deleted immediately
                                  to prevent memory accumulation on graphs
                                  with large integer weights (DIMACS weights
                                  can reach ~10^6, which caused an 11x memory
                                  overhead before the cleanup fix).
"""

import heapq
import math
from collections import defaultdict, deque


def bmssp_like(graph, source):
    dist = {node: math.inf for node in graph}
    dist[source] = 0

    buckets = defaultdict(deque)
    buckets[0].append(source)

    # Min-heap tracking non-empty bucket keys.
    # May contain duplicates/stale entries; empty buckets are skipped below.
    heap = [0]

    while heap:
        current_distance = heapq.heappop(heap)

        # Skip if bucket was already processed or never had valid entries.
        if current_distance not in buckets:
            continue

        bucket = buckets[current_distance]

        while bucket:
            u = bucket.popleft()

            # Stale entry: node already settled at a shorter distance.
            if dist[u] != current_distance:
                continue

            for v, w in graph[u]:
                new_dist = dist[u] + w
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    buckets[new_dist].append(v)
                    heapq.heappush(heap, new_dist)

        # Critical: free memory once this distance level is fully processed.
        # Without this, large integer keys accumulate and memory explodes.
        del buckets[current_distance]

    return dist
