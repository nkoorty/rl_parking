import csv
import matplotlib.pyplot as plt

def read_csv_data(file_path):
    steps = []
    values = []

    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            steps.append(int(row['Step']))
            values.append(float(row['Value']))
    return steps, values

parallel_59 = 'analysis/parallel_59_ppo_1_loss.csv'
parallel_63 = 'analysis/parallel_63_ppo_1_loss.csv'

perpen_19 = 'analysis/perpen_19_ppo_1_loss.csv'
perpen_24 = 'analysis/perpen_24_ppo_1_loss.csv'

steps_59, values_59 = read_csv_data(parallel_59)
steps_63, values_63 = read_csv_data(parallel_63)
steps_19, values_19 = read_csv_data(perpen_19)
steps_24, values_24 = read_csv_data(perpen_24)

# Parallel Parking
plt.figure()
plt.plot(steps_59, values_59, label='Good Case')
plt.plot(steps_63, values_63, label='Base Case')
plt.xlabel('Steps')
plt.ylabel('Loss')
plt.title('Loss vs. Steps (Parallel Parking)')
plt.grid(True)
plt.legend()

plt.xlim(min(steps_59), 150000)
tick_locations = list(range(0, 150000 + 25000, 25000))
tick_labels = [str(tick) for tick in tick_locations]

plt.xticks(tick_locations, tick_labels)

# Perpendicular Parking
plt.figure()
plt.plot(steps_19, values_19, label='Good Case')
plt.plot(steps_24, values_24, label='Base Case')
plt.xlabel('Steps')
plt.ylabel('Loss')
plt.title('Loss vs. Steps (Perpendicular Parking)')
plt.grid(True)
plt.legend()

plt.xlim(min(steps_19), 100000)
tick_locations = list(range(0, 100000 + 25000, 25000))
tick_labels = [str(tick) for tick in tick_locations]

plt.xticks(tick_locations, tick_labels)

plt.show()