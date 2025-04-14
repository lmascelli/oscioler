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
        print(self.instr.query("*IDN?"))

    def save_image(self, file: str):
        self.instr.write("SAVE:IMAG:FILEF PNG")
        self.instr.write("HARDCOPY START")
        data = self.instr.read_raw()
        
    def read_data(self, channel: int = "1"):
        self.instr.write(f":DATa:SOUrche CH{channel}")
        self.instr.write(f":DATa:START {1}")
        self.instr.write(f":DATa:STOP {4096}")
        self.instr.write(f":WFMOutpre:ENCdg {'ASCii'}")
        self.instr.write(f":WFMOutpre:BYT_Nr {1}")
        self.instr.write(f":HEADer {1}")
        self.instr.write(f":VERBose {1}")
        self.instr.query(":WFMOutpre?")
        data_string = self.instr.query(":CURVe?")
        data_string = data_string[data_string.find(',')+1:]
        data_string_io = StringIO(data_string)
        reader = csv.reader(data_string_io)
        numbers = [int(num) for row in reader for num in row]

        return numbers

    def acquire_params(self) -> str:
        return self.instr.query("ACQuire?")
