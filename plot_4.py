import numpy as np
import matplotlib.pyplot as plt

# Data for the radar chart
labels = np.array(["ROUGE-1", "ROUGE-L", "Consistency", "Fluency", "Relevance", "Novelty"])
datasets = ["PSW-1", "PSW-2", "PSW-3", "PSW-4"]
stats = {
    "PSW-1": {
        "Original": [0.337, 0.280, 3.59, 2.58, 3.67, 2.63],
        "Removed": [0.297, 0.250, 3.21, 2.49, 3.31, 2.57],
        "Random": [0.328, 0.272, 3.55, 2.56, 3.62, 2.68]
    },
    "PSW-2": {
        "Original": [0.201, 0.186, 4.60, 2.39, 3.91, 2.38],
        "Removed": [0.180, 0.166, 4.28, 2.32, 3.63, 2.33],
        "Random": [0.195, 0.182, 4.57, 2.42, 3.89, 2.45]
    },
    "PSW-3": {
        "Original": [0.145, 0.131, 4.92, 2.94, 4.71, 2.45],
        "Removed": [0.128, 0.115, 4.70, 2.87, 4.50, 2.41],
        "Random": [0.142, 0.128, 4.95, 2.96, 4.69, 2.51]
    },
    "PSW-4": {
        "Original": [0.505, 0.444, 4.64, 2.59, 3.79, 2.64],
        "Removed": [0.475, 0.419, 4.38, 2.53, 3.58, 2.56],
        "Random": [0.498, 0.438, 4.60, 2.58, 3.76, 2.69]
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
    plt.savefig(f"{dataset}_ablation_2_radar_chart.pdf")