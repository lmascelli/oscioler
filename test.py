import oscioler
import time

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
    # # print(oscilloscope.save_image(""))
    # # print(oscilloscope.read_data(1))
    # print(oscilloscope.acquire_params())

if __name__ == '__main__':
    # test_slide_controller("/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AB0PWJ79-if00-port0")
    test_oscilloscope("10.186.24.126")
