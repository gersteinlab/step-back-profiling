import matplotlib.pyplot as plt
import numpy as np

# Data for the radar chart
labels = np.array(["ROUGE-1", "ROUGE-L", "Consistency", "Fluency", "Relevance", "Novelty"])
datasets = ["PSW-1", "PSW-2", "PSW-3", "PSW-4"]
stats = {
    "PSW-1": {
        "Original": [0.337, 0.280, 3.59, 2.58, 3.67, 2.63],
        "Swap-Random": [0.321, 0.272, 3.42, 2.48, 3.69, 2.45],
        "Swap-First": [0.314, 0.260, 3.35, 2.42, 3.48, 2.37]
    },
    "PSW-2": {
        "Original": [0.201, 0.186, 4.60, 2.39, 3.91, 2.38],
        "Swap-Random": [0.193, 0.178, 4.53, 2.30, 3.85, 2.42],
        "Swap-First": [0.186, 0.171, 4.46, 2.27, 3.77, 2.29]
    },
    "PSW-3": {
        "Original": [0.145, 0.131, 4.92, 2.94, 4.71, 2.45],
        "Swap-Random": [0.138, 0.125, 4.84, 2.88, 4.65, 2.50],
        "Swap-First": [0.130, 0.117, 4.78, 2.98, 4.57, 2.55]
    },
    "PSW-4": {
        "Original": [0.505, 0.444, 4.64, 2.59, 3.79, 2.64],
        "Swap-Random": [0.492, 0.431, 4.57, 2.55, 3.72, 2.70],
        "Swap-First": [0.483, 0.421, 4.50, 2.50, 3.64, 2.76]
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
    for model, values in reversed(stats[dataset].items()):
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
    plt.savefig(f"{dataset}_ablation_1_radar_chart.pdf")