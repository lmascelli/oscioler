from .. import oscioler
import time
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from typing import List


def current_position(slide_address):
    slide_controller = oscioler.SlideController(slide_address)
    slide_controller.status()


def measure(
    slide_address: str,
    oscilloscope_address: str,
    slide_initial_distance: float,
    step: float,
    n_steps: int,
) -> List[float]:
    oscilloscope = oscioler.Oscilloscope(oscilloscope_address)
    slide_controller = oscioler.SlideController(slide_address)
    pressures = []

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

    for i in range(n_steps):
        values, time_step = oscilloscope.read_data(end=1_000_000)
        data = np.array(values)
        num_of_samples_between_peaks = 0.95 * (1e-6 / time_step)
        peaks = find_peaks(
            -data, distance=num_of_samples_between_peaks, prominence=np.std(data)
        )[0]
        pressures.append(np.mean(peaks))
        slide_controller.relative_move(step)
        slide_controller.move()
        time.sleep(5)

    return pressures


if __name__ == "__main__":
    start_distance = 2e-2
    step = 0.2e-3
    n_steps = 75
    pressures = measure("COM2", "", 3.7e-2, step, n_steps)
    distances = [2e-3 - step * i for i in range(n_steps)]
