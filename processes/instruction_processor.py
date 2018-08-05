import serial

from processes.click import Click
from processes.recognizer import Recognizer
from processes.wait import Wait
from processes.process import Process

class InstructionProcessor(Process):

    def __init__(self, config, instructions):
        super().__init__(config)
        self.instructions = instructions
        self.serial = self.run_serial()

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
                if e.process == 'recognize':
                    e.recognize()
            if type(e) == Wait:
                e.delay()

        if self.serial is not None:
            self.serial.close()
