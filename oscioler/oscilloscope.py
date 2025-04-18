from typing import Optional
import pyvisa
import csv
from io import StringIO

TERMINATION_CHAR = "\n"


class Oscilloscope:
    def list_resources():
        rm = pyvisa.ResourceManager("@py")
        if rm is not None:
            print(rm.list_resources())

    def __init__(self, address: Optional[str] = None):
        rm = pyvisa.ResourceManager("@py")
        if rm is not None:
            print(rm.list_resources())
            if address is not None:
                self.instr = rm.open_resource(f"TCPIP::{address}::INSTR")
                self.instr.read_termination = TERMINATION_CHAR
                self.instr.write_termination = TERMINATION_CHAR
        else:
            print("Failed to open a PyVisa resource manager")
            return None

    def idn(self):
        print(f"[INFO]: Found instrument data:\n{self.instr.query("*IDN?")}")

    def save_image(self, file: str):
        self.instr.write("SAVE:IMAG:FILEF PNG")
        self.instr.write("HARDCOPY START")
        data = self.instr.read_raw()

    def read_data(
        self,
        channel: int = "1",
        start: int = 1,
        end: int = 4096,
        encoding: str = "ASCii",
    ):
        self.instr.write(f":DATa:SOUrce CH{channel}")
        self.instr.write(f":DATa:START {start}")
        self.instr.write(f":DATa:STOP {end}")
        self.instr.write(f":WFMOutpre:ENCdg {encoding}")
        self.instr.write(f":WFMOutpre:BYT_Nr {1}")
        self.instr.write(f":HEADer {1}")
        self.instr.write(f":VERBose {1}")
        self.instr.query(":WFMOutpre?")
        self.instr.write(f":HEADer {0}")
        self.instr.write(f":VERBose {0}")
        print(f"[INFO]: Time scale unit is: {self.instr.query(":WFMOutpre:XUNit?")}")
        x_scale = float(self.instr.query(":WFMOutpre:XINcr?"))
        v_scale = float(self.instr.query(":WFMOutpre:YMUlt?"))
        data_string = self.instr.query(":CURVe?")
        data_string = data_string[data_string.find(",") + 1 :]
        data_string_io = StringIO(data_string)
        reader = csv.reader(data_string_io)
        numbers = [int(num) * v_scale for row in reader for num in row]

        return numbers, x_scale

    def acquire_params(self) -> str:
        return self.instr.query("ACQuire?")
