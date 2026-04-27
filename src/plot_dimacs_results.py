import csv
import matplotlib.pyplot as plt
import os


def read_dimacs_results(filename):
    labels = []
    times = []
    memories = []

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            labels.append(f"{row['algorithm']} ({row['nodes']} nodes)")
            times.append(float(row["time_seconds"]))
            memories.append(int(row["memory_bytes"]))

    return labels, times, memories


def plot_dimacs_runtime(labels, times, save_path):
    plt.figure(figsize=(9, 5))
    plt.bar(labels, times)
    plt.xlabel("Algorithm")
    plt.ylabel("Runtime (seconds)")
    plt.title("DIMACS Runtime Comparison")
    plt.xticks(rotation=45, ha="right")
    plt.grid(True, axis="y")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()
    plt.close()


def plot_dimacs_memory(labels, memories, save_path):
    plt.figure(figsize=(9, 5))
    plt.bar(labels, memories)
    plt.xlabel("Algorithm")
    plt.ylabel("Memory Usage (bytes)")
    plt.title("DIMACS Memory Comparison")
    plt.xticks(rotation=45, ha="right")
    plt.grid(True, axis="y")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()
    plt.close()


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results_file = os.path.join(base_dir, "results", "dimacs_results.csv")
    plots_dir = os.path.join(base_dir, "results", "plots")

    if os.path.exists(plots_dir) and not os.path.isdir(plots_dir):
        os.remove(plots_dir)

    os.makedirs(plots_dir, exist_ok=True)

    runtime_path = os.path.join(plots_dir, "dimacs_runtime_comparison.png")
    memory_path = os.path.join(plots_dir, "dimacs_memory_comparison.png")

    labels, times, memories = read_dimacs_results(results_file)

    plot_dimacs_runtime(labels, times, runtime_path)
    plot_dimacs_memory(labels, memories, memory_path)

    print("Plots saved successfully:")
    print(runtime_path)
    print(memory_path)


if __name__ == "__main__":
    main()
