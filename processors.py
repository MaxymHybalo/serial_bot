import serial
import time
import pyautogui as ui

from click import Click
from recognizer import Recognizer
from wait import Wait
CLICK = b'C'

PORT = 'COM5'
BAUDRATE = 9600

X_DIRECT = ('X', 'Z')
Y_DIRECT = ('Y', 'U')
ACCURACY = 3


class InstructionProcessor:

    def __init__(self, instructions):
        self.instructions = instructions
        self.serial = self._run_serial()

    def process(self):
        command = 0
        for e in self.instructions:
            command += 1
            if type(e) == Click:
                self.make_click(e)
            if type(e) == Recognizer:
                if e.process == 'center_on':
                    center = e.center_of()
                    self.make_click(Click(center['x'], center['y'], delay=1))
                if e.process == 'find':
                    e.find()
                else:
                    e.recognize()
            if type(e) == Wait:
                e.delay()
        if self.serial is not None:
            self.serial.close()

    def search(self, x, y):
        _x, _y = ui.position()
        next='X'
        isXPass = self._isCoordLess(_x, x) and self._isCoordGreater(_x, x)
        isYPass = self._isCoordLess(_y, y) and self._isCoordGreater(_y, y)
        while not (isXPass and isYPass):
            if next == 'X':
                if(self._isCoordLess(_x, x)):
                    self._move(X_DIRECT[1])
                    next = 'Y' if not isYPass else 'X'
                else:
                    self._move(X_DIRECT[0])
                    next = 'Y' if not isYPass else 'X'
            if next == 'Y':
                if(self._isCoordLess(_y, y)):
                    self._move(Y_DIRECT[1])
                    next = 'X' if not isXPass else 'Y'
                else:
                    self._move(Y_DIRECT[0])
                    next = 'X' if not isXPass else 'Y'
            _x, _y = ui.position()
            isXPass = self._isCoordLess(_x, x) and self._isCoordGreater(_x, x)
            isYPass = self._isCoordLess(_y, y) and self._isCoordGreater(_y, y)
        
    def _isCoordLess(self,current, target):
            return current >= target - ACCURACY


    def _isCoordGreater(self, current, target):
        return current <= target + ACCURACY
    
    
    def _move(self, t):
        self.serial.write(t.encode())


    def _run_serial(self):
        try:
            s = serial.Serial(PORT, BAUDRATE)
            s.timeout = 0.1
            if not s.is_open:
                s.open()
        except serial.SerialException:
            s = None
        return s
    
        # param click mean Click instance
    def make_click (self, click):
        self.search(click.x, click.y)
        self.serial.write(CLICK)
        if click.process == 'dclick':
            self.serial.write(CLICK)
        time.sleep(click.delay)
