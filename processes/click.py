import pyautogui as ui
from processes.wait import Wait
from utils.serial_controller import SerialController


CLICK = b'C'

X_DIRECT = ('X', 'Z')
Y_DIRECT = ('Y', 'U')
ACCURACY = 3


class Click:

    def __init__(self, x, y, process='click', delay=0):
        self.x = x
        self.y = y
        self.process = process
        self.delay = delay

    # param click mean Click instance
    def make_click(self, serial=SerialController()):
        self.search(serial, self.x, self.y)
        serial.write(CLICK)
        if self.process == 'dclick':
            serial.write(CLICK)
        delay = Wait(self.delay)
        delay.delay()

    def search(self, serial, x, y):
        _x, _y = ui.position()
        axis = 'X'
        is_x_pass = self._get_axis_pass(x, _x)
        is_y_pass = self._get_axis_pass(y, _y)
        while not (is_x_pass and is_y_pass):
            if axis == 'X':
                if self._is_coord_less(_x, x):
                    self._move(serial, X_DIRECT[1])
                    axis = 'Y' if not is_y_pass else 'X'
                else:
                    self._move(serial, X_DIRECT[0])
                    axis = 'Y' if not is_y_pass else 'X'
            if axis == 'Y':
                if self._is_coord_less(_y, y):
                    self._move(serial, Y_DIRECT[1])
                    axis = 'X' if not is_x_pass else 'Y'
                else:
                    self._move(serial, Y_DIRECT[0])
                    axis = 'X' if not is_x_pass else 'Y'
            _x, _y = ui.position()
            is_x_pass = self._get_axis_pass(x, _x)
            is_y_pass = self._get_axis_pass(y, _y)

    def _get_axis_pass(self, target_point, actual_point):
        return self._is_coord_less(actual_point, target_point) and self._is_coord_greater(actual_point, target_point)

    @staticmethod
    def _is_coord_less(current, target):
            return current >= target - ACCURACY

    @staticmethod
    def _is_coord_greater(current, target):
        return current <= target + ACCURACY

    @staticmethod
    def _move(serial, t):
        serial.write(t.encode())

    def __str__(self):
        return "x: " + str(self.x) + " y: " + str(self.y)