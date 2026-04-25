# CENG 383 — Single-Source Shortest Path Assignment

## Overview
Comparison of three SSSP algorithms on the DIMACS New York road network:
- Dijkstra's Algorithm
- Bellman-Ford Algorithm
- BMSSP-like (Dial/Bucket variant inspired by Duan et al., STOC 2025)

## Project Structure
```
CENG-383/
├── data/
│   ├── USA-road-d.NY.gr        # DIMACS NY road network (uncompressed)
│   └── USA-road-d.NY.gr.gz     # DIMACS NY road network (compressed)
├── src/
│   ├── main.py                 # Run benchmarks → saves results/fair_dimacs_results.csv
│   ├── dijkstra.py             # Dijkstra implementation (binary min-heap)
│   ├── bellman_ford.py         # Bellman-Ford implementation (early-exit)
│   ├── bmssp_like.py           # BMSSP-like implementation (Dial/bucket queue)
│   ├── benchmark.py            # Timing & memory measurement helpers
│   ├── dimacs_parser.py        # DIMACS .gr / .gr.gz file loader
│   ├── graph_utils.py          # Random graph generator
│   ├── plot_fair_results.py    # Plot runtime & memory from fair_dimacs_results.csv
│   └── plot_results.py         # Plot from runtime_memory_results.csv
├── results/
│   ├── fair_dimacs_results.csv # Benchmark results (runtime + memory)
│   └── plots/                  # Generated PNG charts
└── report/
    └── CENG383_SSSP_Report.pdf # Final report (PDF)
```

## How to Run

### 1. Run benchmarks
```bash
cd src
python main.py
```
Results are saved to `results/fair_dimacs_results.csv`.

### 2. Generate plots
```bash
python plot_fair_results.py
```
Plots are saved to `results/plots/`.

## Dataset
**DIMACS 9th Implementation Challenge — New York Road Network**  
Source: http://users.diag.uniroma1.it/challenge9/download.shtml  
- Nodes: ~264,000  
- Arcs: ~733,000  
- Format: directed weighted graph (.gr)

## Dependencies
- Python 3.8+
- matplotlib (for plots): `pip install matplotlib`
- No other external dependencies

## Reference
Duan, R., Mao, J., Mao, X., Shu, X., & Yin, L. (2025).  
*Breaking the Sorting Barrier for Directed Single-Source Shortest Paths.*  
STOC 2025. arXiv:2504.17033.
