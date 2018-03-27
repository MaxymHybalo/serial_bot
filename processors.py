import serial

from processes.click import Click
from processes.recognizer import Recognizer
from processes.wait import Wait
from processes.items_handler import ItemsHandler
from processes.nested_process import NestedProcessor
from utils import cv2_utils as utils

PORT = 'COM9'
BAUDRATE = 9600


class InstructionProcessor:

    def __init__(self, instructions):
        self.instructions = instructions
        self.serial = self._run_serial()
        self.storage = dict()

    def process(self):
        command = 0
        print(self.instructions)
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
            if type(e) == ItemsHandler:
                e.set_items(self.storage[e.items_name])
                e.set_grid(self.storage[e.grid_name])
                self.storage['targets'] = e.handle()
            if type(e) == NestedProcessor:
                self.serial.close()
                e.handle()

        if self.serial is not None:
            self.serial.close()

    def show_storage_at(self, image):
        for k, v in self.storage.items():
            image = utils.draw_corners(image, v)
            utils.show(image, name='results')

    def show_storage(self):
        for key, value in self.storage.items():
            print(key, ' : ', value)

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
        except serial.SerialException:
            print('Serial Error')
            s = None
        return s
