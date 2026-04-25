import csv
import matplotlib.pyplot as plt


def read_results(filename="../results/runtime_memory_results.csv"):
    nodes = []
    dijkstra_times = []
    bellman_times = []
    dijkstra_memory = []
    bellman_memory = []

    with open(filename, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            nodes.append(int(row["nodes"]))
            dijkstra_times.append(float(row["dijkstra_time"]))
            bellman_times.append(float(row["bellman_ford_time"]))
            dijkstra_memory.append(int(row["dijkstra_memory"]))
            bellman_memory.append(int(row["bellman_ford_memory"]))

    return nodes, dijkstra_times, bellman_times, dijkstra_memory, bellman_memory


def plot_runtime(nodes, dijkstra_times, bellman_times):
    plt.figure(figsize=(8, 5))
    plt.plot(nodes, dijkstra_times, marker="o", label="Dijkstra")
    plt.plot(nodes, bellman_times, marker="o", label="Bellman-Ford")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Runtime (seconds)")
    plt.title("Runtime Comparison")
    plt.legend()
    plt.grid(True)
    plt.savefig("../results/plots/runtime_comparison.png")
    plt.show()


def plot_memory(nodes, dijkstra_memory, bellman_memory):
    plt.figure(figsize=(8, 5))
    plt.plot(nodes, dijkstra_memory, marker="o", label="Dijkstra")
    plt.plot(nodes, bellman_memory, marker="o", label="Bellman-Ford")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Memory Usage (bytes)")
    plt.title("Memory Usage Comparison")
    plt.legend()
    plt.grid(True)
    plt.savefig("../results/plots/memory_comparison.png")
    plt.show()


def main():
    nodes, dijkstra_times, bellman_times, dijkstra_memory, bellman_memory = read_results()
    plot_runtime(nodes, dijkstra_times, bellman_times)
    plot_memory(nodes, dijkstra_memory, bellman_memory)


if __name__ == "__main__":
    main()