from .. import oscioler
import time
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt


def current_position(slide_address):
    slide_controller = oscioler.SlideController(slide_address)
    slide_controller.status()


def measure(slide_address, oscilloscope_address, slide_initial_distane):
    oscilloscope = oscioler.Oscilloscope(oscilloscope_address)
    slide_controller = oscioler.SlideController(slide_address)

    print("""
The slide is going to be moved until the bottom of the rail.
REMOVE ALL OBSTACLES IN THE PATH!!!
    """)
    input("Press ENTER when ready")

    slide_controller.mechanical_origin()
    slide_controller.move()
    time.sleep(1)

    slide_controller.absolute_move(slide_initial_distane + 3e-2)
    slide_controller.move()

    print("""
Now put the probe under the ultrasound transducer.
    """)
    input("Press ENTER when ready")

    slide_controller.relative_move(-3e-2)
    slide_controller.move()


if __name__ == "__main__":
    current_position("COM2")
