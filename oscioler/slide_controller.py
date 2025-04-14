import serial

# SLIDE CONTROLLER
class SlideController:
    def __init__(self, com: str, step_size: float = 2e-6):
        self.ser = serial.Serial(baudrate = 9600, port = com, timeout = 3)
        self.step_size = step_size
        print(f"Serial connection state: {self.ser.is_open}")

    def __del__(self):
        self.ser.close()

    def _command(self, cmd: str) -> str:
        command = f"{cmd}\r\n".encode("utf-8")
        print(f"Sending command: {command}")
        self.ser.write(command)
        ret = self.ser.readline()
        return ret

    def mechanical_origin(self, axis: str = "1"):
        ret = self._command(f"H:{axis}")
        print(f"Mechanical_Origin: {ret}")
        match ret:
            case b"OK\r\n":
                print("Mechanical_Origin: SUCCESS")
                return True
            case b"NG\r\n":
                print("Mechanical_Origin: FAIL")
                return False
            case _:
                print("Mechanical_Origin: UNKNOWN RETURN")
                return None

    def jogging(self, axis: str = "1") -> str:
        ret = self._command(f"J:{axis}+")
        print(f"Jogging: {ret}")
        match ret:
            case b"OK\r\n":
                print("Jogging: SUCCESS")
                return True
            case b"NG\r\n":
                print("Jogging: FAIL")
                return False
            case _:
                print("Jogging: UNKNOWN RETURN")
                return None

    def relative_move(self, distance: float, axis: str = "1"):
        pulses = int(distance/self.step_size)
        command = f"M:{axis}{'-' if pulses < 0 else '+'}P{abs(pulses)}"
        ret = self._command(command)
        match ret:
            case b"OK\r\n":
                print(f"Relative_Move of {pulses} pulses: SUCCESS")
                return True
            case b"NG\r\n":
                print(f"Relative_Move of {pulses} pulses: FAIL")
                return False
            case _:
                print(f"Relative_Move of {pulses} pulses: UNKWNON RETURN")
                return None

    def absolute_move(self, distance: int, axis: str = "1"):
        pulses = int(distance/self.step_size)
        command = f"A:{axis}{'-' if pulses < 0 else '+'}P{abs(pulses)}"
        ret = self._command(command)
        match ret:
            case b"OK\r\n":
                print(f"Absolute_Move of {pulses} pulses: SUCCESS")
                return True
            case b"NG\r\n":
                print(f"Absolute_Move of {pulses} pulses: FAIL")
                return False
            case _:
                print(f"Absolute_Move of {pulses} pulses: UNKNOWN RETURN")
                return None

    def move(self):
        ret = self._command("G:")
        self.wait()
        match ret:
            case b"OK\r\n":
                return True
            case b"NG\r\n":
                return False
            case _:
                return None

    def immediate_stop(self):
        ret = self._command("L:E")
        match ret:
            case b"OK\r\n":
                return True
            case b"NG\r\n":
                return False
            case _:
                return None

    def status(self):
        ret = self._command("Q:")
        print(f"Status: {ret}")
        ret = self._command("!:")
        print(f"Status: {ret}")

    def is_busy(self):
        ret = self._command("!:")
        match ret:
            case b"B\r\n":
                return True
            case b"R\r\n":
                return False
            case _:
                return None

    def wait(self):
        while self.is_busy():
            pass
