import matplotlib.pyplot as plt
import numpy as np

# Data for the radar chart
labels = np.array(["LaMP-1 (Accuracy)", "LaMP-2 (Accuracy)", "LaMP-3 (RMSE)", "LaMP-4 (ROUGE-1)", "LaMP-5 (ROUGE-1)", "LaMP-6 (ROUGE-1)", "LaMP-7 (ROUGE-1)"])
stats = {
    "Non-personalized FlanT5-XXL": [0.522, 0.591, 0.666, 0.164, 0.455, 0.332, 0.459],
    "Non-personalized ChatGPT": [0.510, 0.610, 0.977, 0.133, 0.395, 0, 0.396],
    "Personalized FlanT5-XXL": [0.675, 0.598, 0.584, 0.192, 0.466, 0.466, 0.448],
    "Personalized ChatGPT": [0.701, 0.693, 1.102, 0.160, 0.398, 0, 0.391],
    "Step-back Profiling": [0.624, 0.729, 0.559, 0.195, 0.469, 0.485, 0.455]
}

# Calculate the angles for the radar chart
num_vars = len(labels)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(figsize=(15, 10), subplot_kw=dict(polar=True))

# Find the maximum value for each task
max_values = [max(values[i] for values in stats.values()) for i in range(num_vars)]
min_values = [min(values[i] for values in stats.values()) for i in range(num_vars)]

# Normalize the values and plot each data set
for model, values in stats.items():
    # Normalize the values
    normalized_values = [value / max_values[i] if i != 2 else value / min_values[i] for i, value in enumerate(values)]
    normalized_values[2] = 1 - normalized_values[2] + 1
    normalized_values += normalized_values[:1]
    
    # Plot the normalized values
    ax.plot(angles, normalized_values, label=model)
    ax.fill(angles, normalized_values, alpha=0.25)
    
    # Label the points with the largest value for each task
    for i, (angle, value) in enumerate(zip(angles, values)):
        if value == max_values[i]:
            if i == 0 or i == 3:
                ax.text(angle + 0.05, normalized_values[i], f"{value:.3f}", fontsize=18, ha='center', va='bottom')
            else:
                ax.text(angle - 0.05, normalized_values[i], f"{value:.3f}", fontsize=18, ha='center', va='center')
        elif value == min_values[i] and value != 0:
            if i == 0 or i == 3:
                ax.text(angle + 0.05, normalized_values[i], f"{value:.3f}", fontsize=18, ha='center', va='bottom')
            else:
                ax.text(angle - 0.05, normalized_values[i], f"{value:.3f}", fontsize=18, ha='center', va='center')

# Draw labels
ax.set_thetagrids(np.degrees(angles[:-1]), labels, fontsize=24, fontweight='bold')
ax.set_yticklabels([])

plt.legend(loc='lower right', bbox_to_anchor=(1.65, -0.1), fontsize=20)
plt.subplots_adjust(left=0.0, right=0.8)
plt.savefig("LaMP_radar_chart.pdf")