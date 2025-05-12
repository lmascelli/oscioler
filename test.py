import numpy as np
import matplotlib.pyplot as plt
from pprint import pp
import csv

filename = "/home/leonardo/Documents/unige/data/Caratterizzazione/caratterizzazione/50_3_trials.csv"
distances = []
trials = []

with open(filename, 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    
    for _ in range(len(header)-1):
        trials.append([])
        
    for row in reader:
        distances.append(float(row[0]))
        for i, value in enumerate(row[1:]):
            trials[i].append(float(value))

distances = np.array(distances)
trials = np.array(trials).T

pp(trials.shape)
plt.plot(distances, trials[:, 2])
plt.scatter(distances, trials[:, 2])
plt.title("Trial 3")
plt.xlabel("Distance from surface (cm)")
plt.ylabel("Pressure (MPa)")
plt.show()
