import matplotlib.pyplot as plt

# Data
N = [3, 5, 13, 25]
avg_time = [0.004, 0.008, 0.042, 0.137]  # ms
operation_count = [9, 25, 169, 625]     # N²

fig, ax1 = plt.subplots(figsize=(8, 5))

# Left y-axis: computation time
line1 = ax1.plot(
    N, avg_time,
    marker="o",
    color="blue",
    label="Average Computation Time (ms)"
)
ax1.set_xlabel("Matrix Size (N)")
ax1.set_ylabel("Average Computation Time (ms)")
ax1.grid(True, alpha=0.3)

# Right y-axis: operation count
ax2 = ax1.twinx()

line2 = ax2.plot(
    N, operation_count,
    marker="s",
    color="gray",
    label="Operation Count (N²)"
)
ax2.set_ylabel("Operation Count (N²)")

# Combined legend
lines = line1 + line2
labels = [line.get_label() for line in lines]
ax1.legend(lines, labels, loc="upper left")

plt.title("Computation Performance by Matrix Size")
plt.tight_layout()

# Save as PNG
plt.savefig("./images/computation_performance.png", dpi=300)

plt.show()