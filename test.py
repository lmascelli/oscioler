import oscioler
import time
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

def test_slide_controller(device):
    slide_controller = oscioler.SlideController(device)
    ret = slide_controller.status()
    ret = slide_controller.absolute_move(10e-2)
    ret = slide_controller.move()

    for i in range(10):
        distance = 5e-4 # meters
        ret = slide_controller.relative_move(-distance)
        ret = slide_controller.move()

    for i in range(10):
        distance = 1e-3 # meters
        ret = slide_controller.relative_move(-distance)
        ret = slide_controller.move()


def test_oscilloscope(address):
    oscioler.Oscilloscope.list_resources()
    oscilloscope = oscioler.Oscilloscope(address)
    oscilloscope.idn()
    data, delta_t = oscilloscope.read_data(end=1_000_000)
    data = np.array(data)
    data_std = np.std(data)
    peak_distance = 1e-1/delta_t
    peaks = find_peaks(-data, distance=int(0.95*peak_distance))

    plt.plot(data)
    plt.scatter(peaks[0], data[peaks[0]], color="red")
    plt.show()

    
if __name__ == '__main__':
    # test_slide_controller("/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AB0PWJ79-if00-port0")
    # test_oscilloscope("10.186.24.126")

    # Initialize resources
    DEVICE = ""
    ADDRESS = ""
    slide_controller = oscioler.SlideController(DEVICE)
    oscilloscope = oscioler.Oscilloscope(ADDRESS)
    
    result = []

    # Manually set the transducer at the start position (1.5 cm)

    step = 1e-4 # 0.1 mm
    start_distance = 1.4 e-2
    n_steps = int(start_distance / step)

    # Move the transdure and record the data
    for i in range(n_steps):
        slide_controller.relative_move(-i*step)
        slide_controller.move()
        data, delta_t = oscilloscope.read_data(end=1_000_000)
        data = np.array(data)
        data_std = np.std(data)
        peak_distance = 1e-6/delta_t
        peaks = find_peaks(-data, distance=int(0.99*peak_distance), prominence=3*data_std)
        result.append(np.mean(peaks))

    distances = [(15e-3 - i*step) for i in range(n_steps)]
    pressures = [52./v for v in result]
    plt.plot(distances, result)
    plt.xlabel("Distance from surface (cm)")
    plt.ylabel("Pressure (MPa)")
    plt.show()
