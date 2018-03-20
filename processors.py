import serial

from processes.click import Click
from processes.recognizer import Recognizer
from processes.wait import Wait
from utils import cv2_utils as utils

PORT = 'COM4'
BAUDRATE = 9600


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
        if self.serial is not None:
            self.serial.close()

    def show_storage_at(self, image):
        for k,v in self.storage.items():
            image = utils.draw_corners(image, v)
            print(k,':',v)
        utils.show(image, name='results')

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
