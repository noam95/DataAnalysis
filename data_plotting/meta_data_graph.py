import json
import matplotlib.pyplot as plt
from datetime import datetime

# Load JSON data from the file
with open('night_data/noam/2024-01-14-noam.json', 'r') as json_file:
    data = json.load(json_file)

# Extract relevant information
id_value = data['id']
date_value = data['data']
actions = data['actions']

# Create a figure and axis
fig, ax = plt.subplots()

# Plot horizontal line at y=-1
ax.axhline(y=1, color='black', linestyle='-', label='Base Line')

# Create a dictionary to map unique instance names to colors
instance_color_mapping = {
    "speaker": "red",
    "light": "green",
    "smell": "blue"
}

# Plot vertical lines for each action with different colors based on 'instance_name'
for action in actions:
    instance_name = action['payload']['instance_name']
    timestamp = action['timestamp'] / 1000  # Convert milliseconds to seconds
    time_to_run = datetime.strptime(action['payload']['time_to_run'], "%Y-%m-%d %H:%M:%S.%f%z").timestamp()

    # Assign a unique color to each unique instance name
    if instance_name not in instance_color_mapping:
        instance_color_mapping[instance_name] = plt.cm.rainbow(len(instance_color_mapping) / len(actions))

    # Plot vertical line
    ax.plot([timestamp, timestamp], [0, 2], color=instance_color_mapping[instance_name], linestyle='--')

    # ax.axvline(x=time_to_run, color=instance_color_mapping[instance_name], linestyle='--')

# Set plot title and labels
plt.title(f'ID: {id_value}, Date: {date_value}')
plt.xlabel('Timestamp (seconds)')
plt.ylabel('Value')

# Create legend outside the loop
legend_labels = [plt.Line2D([0], [0], color=color, label=f'Action: {instance_name}') for instance_name, color in instance_color_mapping.items()]
ax.legend(handles=legend_labels, loc='upper right')

# Show the plot
plt.show()