import csv
from pathlib import Path
import matplotlib.pyplot as plt

DATASETS = [
    ("DIMACS-NY",  "fair_dimacs_results_dimacs_ny.csv"),
    ("DIMACS-BAY", "fair_dimacs_results_dimacs_bay.csv"),
]
LEGACY_CSV = "fair_dimacs_results.csv"

STYLE = {
    "Dijkstra":     {"color": "#1565C0", "marker": "o", "linestyle": "-",  "linewidth": 2.0, "markersize": 6, "zorder": 4},
    "Bellman-Ford": {"color": "#E65100", "marker": "s", "linestyle": "--", "linewidth": 2.0, "markersize": 6, "zorder": 3},
    "BMSSP-like":   {"color": "#2E7D32", "marker": "^", "linestyle": ":",  "linewidth": 2.5, "markersize": 7, "zorder": 2},
}


def read_results(filename):
    data = {}
    with open(filename, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["time_seconds"] == "NA" or row["memory_bytes"] == "NA":
                continue
            algo  = row["algorithm"]
            nodes = int(row["nodes"])
            t_s   = float(row["time_seconds"])
            m_kb  = float(row["memory_bytes"]) / 1024
            if algo not in data:
                data[algo] = {"nodes": [], "time": [], "memory": []}
            data[algo]["nodes"].append(nodes)
            data[algo]["time"].append(t_s)
            data[algo]["memory"].append(m_kb)
    return data


def _draw_lines(ax, dataset, metric, log=False):
    for algo, vals in dataset.items():
        s = STYLE.get(algo, {})
        ax.plot(vals["nodes"], vals[metric], label=algo, **s)
    if log:
        ax.set_yscale("log")
    ax.legend(fontsize=8)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.set_xlabel("Number of Nodes", fontsize=9)


def plot_two_datasets(ny_data, bay_data, plots_dir):
    fig, axes = plt.subplots(2, 2, figsize=(13, 8))
    fig.suptitle("SSSP Algorithms: NY Road Network vs BAY Road Network",
                 fontsize=13, fontweight="bold")

    # --- Runtime NY ---
    _draw_lines(axes[0, 0], ny_data, "time", log=True)
    axes[0, 0].set_title("Runtime - DIMACS-NY (log scale)", fontsize=10, fontweight="bold")
    axes[0, 0].set_ylabel("Runtime (s)", fontsize=9)

    # --- Runtime BAY ---
    _draw_lines(axes[0, 1], bay_data, "time", log=True)
    axes[0, 1].set_title("Runtime - DIMACS-BAY (log scale)", fontsize=10, fontweight="bold")
    axes[0, 1].set_ylabel("Runtime (s)", fontsize=9)

    # --- Memory NY ---
    _draw_lines(axes[1, 0], ny_data, "memory")
    axes[1, 0].set_title("Memory - DIMACS-NY", fontsize=10, fontweight="bold")
    axes[1, 0].set_ylabel("Memory (KB)", fontsize=9)

    # --- Memory BAY ---
    ax4 = axes[1, 1]
    for algo in ["BMSSP-like", "Bellman-Ford", "Dijkstra"]:
        if algo not in bay_data:
            continue
        vals = bay_data[algo]
        s = STYLE.get(algo, {})
        ax4.plot(vals["nodes"], vals["memory"], label=algo, **s)
    ax4.set_title("Memory - DIMACS-BAY", fontsize=10, fontweight="bold")
    ax4.set_ylabel("Memory (KB)", fontsize=9)
    ax4.set_xlabel("Number of Nodes", fontsize=9)
    ax4.legend(fontsize=8)
    ax4.grid(True, linestyle="--", alpha=0.4)

    plt.tight_layout()
    out = plots_dir / "sssp_comparison_both_datasets.png"
    plt.savefig(out, dpi=150)
    plt.show()
    plt.close()
    print("Combined plot saved:", out)


def plot_single_dataset(data, dataset_name, plots_dir):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("SSSP Algorithms - " + dataset_name, fontsize=12, fontweight="bold")

    _draw_lines(ax1, data, "time", log=True)
    ax1.set_title("Runtime (log scale)")
    ax1.set_ylabel("Runtime (s)")

    _draw_lines(ax2, data, "memory")
    ax2.set_title("Memory Usage")
    ax2.set_ylabel("Memory (KB)")

    plt.tight_layout()
    safe_name = dataset_name.lower().replace("-", "_")
    out = plots_dir / ("sssp_" + safe_name + ".png")
    plt.savefig(out, dpi=150)
    plt.show()
    plt.close()
    print(dataset_name + " plot saved:", out)


def main():
    base_dir  = Path(__file__).resolve().parents[1]
    results   = base_dir / "results"
    plots_dir = results / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)

    dataset_data = {}
    for name, csv_file in DATASETS:
        path = results / csv_file
        if path.exists():
            dataset_data[name] = read_results(path)
        else:
            print("WARNING: " + csv_file + " not found - run main.py first.")

    if len(dataset_data) == 2:
        plot_two_datasets(dataset_data["DIMACS-NY"], dataset_data["DIMACS-BAY"], plots_dir)
        for name, data in dataset_data.items():
            plot_single_dataset(data, name, plots_dir)
    elif len(dataset_data) == 1:
        name, data = next(iter(dataset_data.items()))
        plot_single_dataset(data, name, plots_dir)
    else:
        legacy = results / LEGACY_CSV
        if legacy.exists():
            print("Falling back to " + LEGACY_CSV)
            data = read_results(legacy)
            plot_single_dataset(data, "DIMACS", plots_dir)
        else:
            print("No result CSV found. Run main.py first.")


if __name__ == "__main__":
    main()
