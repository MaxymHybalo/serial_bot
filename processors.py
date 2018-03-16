import serial

from click import Click
from recognizer import Recognizer
from wait import Wait

PORT = 'COM5'
BAUDRATE = 9600


class InstructionProcessor:

    def __init__(self, instructions):
        self.instructions = instructions
        self.serial = self._run_serial()

    def process(self):
        command = 0
        for e in self.instructions:
            command += 1
            if type(e) == Click:
                e.make_click(self.serial)
            if type(e) == Recognizer:
                if e.process == 'center_on':
                    center = e.center_of()
                    center_click = Click(center['x'], center['y'], delay=1)
                    center_click.make_click(self.serial)
                if e.process == 'find':
                    e.find()
                else:
                    e.recognize()
            if type(e) == Wait:
                e.delay()
        if self.serial is not None:
            self.serial.close()

    @staticmethod
    def _run_serial():
        try:
            s = serial.Serial(PORT, BAUDRATE)
            s.timeout = 0.1
            if not s.is_open:
                s.open()
        except serial.SerialException:
            s = None
        return s
