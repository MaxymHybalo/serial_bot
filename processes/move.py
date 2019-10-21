import pyautogui as ui
from utils.serial_controller import SerialController
from processes.wait import Wait

class Move:

    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def exec(self):
        serial = SerialController().serial
        startX, startY = self.start
        ui.moveTo(startX, startY)
        serial.write(b'P')
        endX, endY = self.end
        Wait(0.1).delay()
        ui.moveTo(endX, endY)
        serial.write(b'R')
