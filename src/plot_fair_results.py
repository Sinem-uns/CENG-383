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


def plot_runtime(data, output_path):
    plt.figure(figsize=(8, 5))

    for algo, values in data.items():
        plt.plot(values["nodes"], values["values"], marker="o", label=algo)

    plt.yscale("log")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Runtime (seconds, log scale)")
    plt.title("Runtime Comparison of SSSP Algorithms")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(output_path)
    plt.show()   # 🔥 otomatik aç
    plt.close()


def plot_memory(data, output_path):
    plt.figure(figsize=(8, 5))

    for algo, values in data.items():
        plt.plot(values["nodes"], values["values"], marker="o", label=algo)

    plt.xlabel("Number of Nodes")
    plt.ylabel("Memory Usage (KB)")
    plt.title("Memory Usage Comparison of SSSP Algorithms")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(output_path)
    plt.show()   # 🔥 otomatik aç
    plt.close()


def main():
    base_dir = Path(__file__).resolve().parents[1]

    csv_path = base_dir / "results" / "fair_dimacs_results.csv"
    plots_dir = base_dir / "results" / "plots"

    plots_dir.mkdir(parents=True, exist_ok=True)

    if not csv_path.exists():
        print("CSV file not found:", csv_path)
        return

    runtime_data, memory_data = read_results(csv_path)

    runtime_plot = plots_dir / "fair_runtime.png"
    memory_plot = plots_dir / "fair_memory.png"

    plot_runtime(runtime_data, runtime_plot)
    plot_memory(memory_data, memory_plot)

    print("Runtime plot created:", runtime_plot)
    print("Memory plot created:", memory_plot)


if __name__ == "__main__":
    main()