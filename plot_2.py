import matplotlib.pyplot as plt
import numpy as np

# Data for the radar chart
labels = np.array(["ROUGE-1", "ROUGE-L", "Consistency", "Fluency", "Relevance", "Novelty"])
datasets = ["PSW-1", "PSW-2", "PSW-3", "PSW-4"]
stats = {
    "PSW-1": {
        "Zero-shot": [0.306, 0.257, 3.43, 2.65, 3.53, 2.30],
        "Single-Author": [0.325, 0.266, 3.44, 2.47, 3.61, 2.59],
        "Multi-Author": [0.337, 0.280, 3.59, 2.58, 3.67, 2.63]
    },
    "PSW-2": {
        "Zero-shot": [0.196, 0.179, 4.31, 2.04, 3.89, 2.21],
        "Single-Author": [0.190, 0.171, 4.20, 2.23, 3.67, 2.01],
        "Multi-Author": [0.201, 0.186, 4.60, 2.39, 3.91, 2.38]
    },
    "PSW-3": {
        "Zero-shot": [0.099, 0.094, 4.43, 2.81, 4.43, 2.40],
        "Single-Author": [0.131, 0.124, 4.94, 2.94, 4.70, 2.40],
        "Multi-Author": [0.145, 0.131, 4.92, 2.94, 4.71, 2.45]
    },
    "PSW-4": {
        "Zero-shot": [0.459, 0.391, 4.41, 2.41, 3.58, 2.38],
        "Single-Author": [0.472, 0.409, 4.59, 2.49, 3.78, 2.60],
        "Multi-Author": [0.505, 0.444, 4.64, 2.59, 3.79, 2.64]
    }
}

# Calculate the angles for the radar chart
num_vars = len(labels)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]

for dataset in datasets:
    fig, ax = plt.subplots(figsize=(12, 10), subplot_kw=dict(polar=True))

    # Find the maximum value for each metric within the dataset
    max_values_rouge = max([max(values[i] for values in stats[dataset].values()) for i in range(2)])
    max_values_others = max([max(values[i] for values in stats[dataset].values()) for i in range(2, num_vars)])

    # Normalize the values and plot each data set
    for model, values in stats[dataset].items():
        # Normalize the values
        normalized_values = [value / max_values_rouge for i, value in enumerate(values[:2])]
        normalized_values += [value / max_values_others for i, value in enumerate(values[2:])]
        normalized_values += normalized_values[:1]

        # Plot the normalized values
        ax.plot(angles, normalized_values, label=model)
        ax.fill(angles, normalized_values, alpha=0.25)

    # Label the points with the largest value for each metric
    for i, angle in enumerate(angles[:-1]):
        if i < 2:
            max_value = max(values[i] for values in stats[dataset].values())
            ax.text(angle - 0.05, max_value / max_values_rouge, f"{max_value:.3f}", fontsize=24, ha='center', va='top')
        elif i != 4:
            max_value = max(values[i] for values in stats[dataset].values())
            ax.text(angle + 0.05, max_value / max_values_others, f"{max_value:.3f}", fontsize=24, ha='center', va='top')
        else:
            max_value = max(values[i] for values in stats[dataset].values())
            ax.text(angle - 0.05, max_value / max_values_others, f"{max_value:.3f}", fontsize=24, ha='center', va='center')

    # Draw labels
    ax.set_thetagrids(np.degrees(angles[:-1]), labels, fontsize=24, fontweight='bold', va='bottom')
    ax.set_yticklabels([])

    plt.legend(loc='lower right', bbox_to_anchor=(1.4, -0.1), fontsize=24)
    plt.subplots_adjust(left=0.0, right=0.8)
    plt.savefig(f"{dataset}_radar_chart.pdf")