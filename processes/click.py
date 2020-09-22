import pyautogui as ui
from processes.wait import Wait
from processes.move import Move
from utils.serial_controller import SerialController


CLICK = b'C'

class Click:

    def __init__(self, x, y, process='click', delay=0):
        self.x = x
        self.y = y
        self.process = process
        self.delay = delay

    # param click mean Click instance
    def make_click(self, serial=SerialController()):
        if hasattr(serial, 'serial'):
            serial = serial.serial
        Move().moveTo(self.x, self.y)
        serial.write(CLICK)
        if self.process == 'dclick' or self.process == 'double':
            serial.write(CLICK)
        delay = Wait(self.delay)
        delay.delay()

    
    def __str__(self):
        return "x: " + str(self.x) + " y: " + str(self.y)