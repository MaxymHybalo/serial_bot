import serial

PORT = 'COM7'
BAUDRATE = 9600


class ObjectProcessor:

    def __init__(self, target):
        self.target = target
        self.serial = self._run_serial()

    def handle(self):
        print('[', type(self.target), ']')
        self.target.process()

    @staticmethod
    def _run_serial():
        try:
            s = serial.Serial(PORT, BAUDRATE)
            s.timeout = 0.01
            if s.is_open:
                s.close()
            if not s.is_open:
                print('[SERIAL OPENED AT: ', PORT, ']')
                s.open()
        except serial.SerialException:
            print('[SERIAL ERROR]')
            s = None
        return s
