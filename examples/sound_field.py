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

    with open(filename, newline="") as csvfile:
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
            values, time_step = oscilloscope.read_data(end=10_000)
            data = np.array(values)
            samples_in_a_period = 1e-6 / time_step
            number_of_samples = int(len(data) / samples_in_a_period) * int(samples_in_a_period)
            rms = np.sqrt(np.mean(data[0:number_of_samples]) ** 2)
            pressures[trial].append(rms * np.sqrt(2))
            slide_controller.relative_move(-step)
            slide_controller.move()
            time.sleep(5)
        input("Press ENTER to start an other trial")
        slide_controller.relative_move(step * n_steps)
        slide_controller.move()

    return pressures


if __name__ == "__main__":
    START_DISTANCE = 2e-2
    END_DISTANCE = 1e-2
    STEP = 1e-3 / 100
    N_STEPS = int((START_DISTANCE - END_DISTANCE) / STEP)
    NUM_OF_TRIALS = 1
    pressures = measure("COM2", "10.186.24.4", 3.7e-2, STEP, N_STEPS, NUM_OF_TRIALS)
    distances = [(START_DISTANCE - STEP * i) for i in range(N_STEPS)]

    savefile = "data.csv"
    with open(savefile, mode="w", newline="") as file:
        writer = csv.writer(file)
        header = ["Distances"] + [f"Trial{i + 1}" for i in range(len(pressures))]
        writer.writerow(header)

        for i in range(len(distances)):
            row_data = [distances[i]] + [pressures[i] for pressures_trial in pressures]
            writer.writerow(row_data)

    pressures = np.array(pressures) / 52e-3 # V/MPa
    mean_pressures = np.mean(pressures, axis=0)
    std_pressures = np.std(pressures, axis=0)
    
    plt.scatter(
        distances, mean_pressures, marker="o", color="blue", label="Mean pressure"
    )
    
    plt.errorbar(
        distances,
        mean_pressures,
        yerr=std_pressures,
        fmt="none",
        ecolor="red",
        capsize=5,
        label="Standard Deviation",
    )
    
    plt.xlabel("Distance from the surface (m)")
    plt.ylabel("Pressure (MPa)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
