import pandas as pd
import matplotlib.pyplot as plt
import json
from collections import Counter


def load_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


data = load_data('data/nl2bash-data.json')

# Assuming 'commands' contains the list of all extracted commands
commands = [entry['cmd'] for entry in data.values()]


base_commands = [cmd.split()[0] for cmd in commands if cmd]

base_command_counts = Counter(base_commands)

# Converting to a pandas Series for easy plotting
base_command_series = pd.Series(
    base_command_counts).sort_values(ascending=False)

# Plotting the distribution of the most common base commands
plt.figure(figsize=(10, 6))
base_command_series.head(20).plot(kind='bar')
plt.title('Distribution of Top 20 Base Commands')
plt.xlabel('Base Commands')
plt.ylabel('Frequency')
plt.xticks(rotation=45, ha='right')
plt.show()
