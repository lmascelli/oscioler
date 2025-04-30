from .. import oscioler
import time
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from typing import List
import csv


def current_position(slide_address):
    slide_controller = oscioler.SlideController(slide_address)
    slide_controller.status()

    
def plot_data(filename: str):
    distances = []
    pressures = []

    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            distances.append(float(row[0]))
            pressures.append(float(row[1]))
            
            
def measure(
    slide_address: str,
    oscilloscope_address: str,
    slide_initial_distance: float,
    step: float,
    n_steps: int,
    num_of_trials: int,
) -> List[float]:
    oscilloscope = oscioler.Oscilloscope(oscilloscope_address)
    slide_controller = oscioler.SlideController(slide_address)
    pressures = [[] for i in range(num_of_trials)]

    print("""
The slide is going to be moved until the bottom of the rail.
REMOVE ALL OBSTACLES IN THE PATH!!!
    """)
    input("Press ENTER when ready")

    slide_controller.mechanical_origin()
    slide_controller.move()
    time.sleep(1)

    slide_controller.absolute_move(slide_initial_distance + 5e-3)
    slide_controller.move()

    print("""
Now put the probe under the ultrasound transducer.
    """)
    input("Press ENTER when ready")

    slide_controller.relative_move(-5e-3)
    slide_controller.move()

    print("""
The measure is going to start.
    """)
    input("Press ENTER when ready")

    for trial in range(num_of_trials):
        for i in range(n_steps):
            print(f"STEP: {i}/{n_steps}")
            values, time_step = oscilloscope.read_data(end=1_000_000)
            data = np.array(values)
            num_of_samples_between_peaks = int(0.95 * (1e-6 / time_step))
            peaks = find_peaks(
                -data, distance=num_of_samples_between_peaks, prominence=np.std(data)
            )[0]
            pressures[trial].append(np.mean(peaks))
            slide_controller.relative_move(-step)
            slide_controller.move()
            time.sleep(5)
        slide_controller.relative_move(step*n_steps)
        slide_controller.move()

    result = []
    for i in range(n_steps):
        acc = 0
        for trial in range(num_of_trials):
            acc = acc + pressures[trial][i]
        result.append(52. / (acc/num_of_trials))
        
    return result


if __name__ == "__main__":
    start_distance = 2e-2
    end_distance = 1e-3
    step = 1e-3/20
    n_steps = int((start_distance - end_distance)/step)
    num_of_trials = 30
    pressures = measure("COM2", "", 3.7e-2, step, n_steps, num_of_trials)
    distances = [start_distance - step * i for i in range(n_steps)]

    savefile = 'data.csv'
    with open(savefile, mode='w', newline='') as file:
        writer = csv.writer(file)
        header = ['Distances'] + [f'Trial{i+1}' for i in range(len(pressures))]
        writer.writerow(header)

        for i in range(len(distances)):
            row_data = [distances[i]] + [pressures[i] for pressures_trial in pressures]
            writer.writerow(row_data)

    pressures = np.array(pressures)
    mean_pressure = np.mean(pressures, axis=0)
    std_pressure = np.std(pressures, axis=0)
    plt.scatter(distances, mean_pressures, marker='o', color='blue', label='Mean pressure')
    plt.errorbar(distances, mean_pressures, yerr=std_pressure, fmt='none', ecolor='red', capsize=5, label="Standard Deviation")
    plt.xlabel("Distance from the surface (m)")
    plt.ylabel("Pressure (MPa)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
