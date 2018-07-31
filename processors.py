import serial

from processes.click import Click
from processes.recognizer import Recognizer
from processes.wait import Wait
from processes.nested_process import NestedProcessor


# TODO move to config file
PORT = 'COM7'
BAUDRATE = 9600


# TODO make extension class for serial delivery
# TODO show_storage remove

class InstructionProcessor:

    def __init__(self, instructions):
        self.instructions = instructions
        self.serial = self._run_serial()
        self.storage = dict()

    def process(self):
        command = 0
        for e in self.instructions:
            command += 1
            print('[' + str(command) + '] ', e.process)
            if type(e) == Click:
                e.make_click(self.serial)
            if type(e) == Recognizer:
                if e.process == 'center_on':
                    center = e.center_of()
                    center_click = Click(center['x'], center['y'])
                    center_click.make_click(self.serial)
                if e.process == 'find':
                    self.storage[str(e.properties['name'])] = e.find()
                if e.process == 'recognize':
                    e.recognize()
            if type(e) == Wait:
                e.delay()
            if type(e) == NestedProcessor:
                self.serial.close()
                e.handle()

        if self.serial is not None:
            self.serial.close()

    def show_storage(self):
        for key, value in self.storage.items():
            print(key, ' : ', value)

    # TODO make base class for process itializer and process intializer and make there this class
    @staticmethod
    def _run_serial():
        try:
            s = serial.Serial(PORT, BAUDRATE)
            s.timeout = 0.01
            if s.is_open:
                s.close()
            if not s.is_open:
                print('[SERIAL OPENED at: ', PORT, ']')
                s.open()
        except serial.SerialException as e:
            print('Serial Error', e)
            s = None
        return s
