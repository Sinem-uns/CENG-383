"""Plot NY vs BAY comparison — kopyala src/ klasörüne koy, sonra çalıştır:
   python src/plot_bay_comparison.py
   Grafikleri results/plots/ altına kaydeder ve ekranda açar.
"""

import csv
from pathlib import Path
import matplotlib.pyplot as plt


def read_results(filename):
    runtime_data = {}
    memory_data = {}

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["time_seconds"] == "NA" or row["memory_bytes"] == "NA":
                continue
            algo = row["algorithm"]
            nodes = int(row["nodes"])
            runtime = float(row["time_seconds"])
            memory_kb = int(float(row["memory_bytes"])) / 1024

            if algo not in runtime_data:
                runtime_data[algo] = {"nodes": [], "values": []}
            if algo not in memory_data:
                memory_data[algo] = {"nodes": [], "values": []}

            runtime_data[algo]["nodes"].append(nodes)
            runtime_data[algo]["values"].append(runtime)
            memory_data[algo]["nodes"].append(nodes)
            memory_data[algo]["values"].append(memory_kb)

    return runtime_data, memory_data


def main():
    base_dir = Path(__file__).resolve().parents[1]
    plots_dir = base_dir / "results" / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)

    ny_csv  = base_dir / "results" / "fair_dimacs_results.csv"
    bay_csv = base_dir / "results" / "bay_results.csv"

    if not bay_csv.exists():
        print("bay_results.csv bulunamadı. Önce BAY benchmark'ını çalıştır.")
        return

    ny_rt,  ny_mem  = read_results(ny_csv)
    bay_rt, bay_mem = read_results(bay_csv)

    colors = {"Dijkstra": "#2196F3", "BMSSP-like": "#4CAF50", "Bellman-Ford": "#FF9800"}

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle("SSSP Algorithms: NY Road Network vs BAY Road Network", fontsize=13, fontweight="bold")

    datasets = [
        (axes[0][0], "Runtime — DIMACS NY (New York)",          ny_rt,  True),
        (axes[0][1], "Runtime — DIMACS BAY (San Francisco Bay)", bay_rt, True),
        (axes[1][0], "Memory — DIMACS NY (New York)",           ny_mem, False),
        (axes[1][1], "Memory — DIMACS BAY (San Francisco Bay)", bay_mem, False),
    ]

    for ax, title, data, logscale in datasets:
        ax.set_title(title, fontsize=10)
        for algo, vals in data.items():
            ax.plot(vals["nodes"], vals["values"], "o-",
                    label=algo, color=colors.get(algo), linewidth=2, markersize=5)
        ax.set_xlabel("Number of Nodes")
        ax.set_ylabel("Time (s)" if logscale else "Memory (KB)")
        if logscale:
            ax.set_yscale("log")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    out = plots_dir / "ny_vs_bay_comparison.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print("Kaydedildi:", out)
    plt.show()
    plt.close()


if __name__ == "__main__":
    main()