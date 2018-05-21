import serial
import logging

PORT = 'COM9'
BAUDRATE = 9600


class ObjectProcessor:

    def __init__(self, target):
        self.target = target
        self.serial = self._run_serial()
        logging.getLogger()

    def handle(self):
        self.target.process(self.serial)

    @staticmethod
    def _run_serial():
        try:
            logging.critical('Trying connect to Arduino via {0}'.format(PORT))
            s = serial.Serial(PORT, BAUDRATE)
            s.timeout = 0.01
            if s.is_open:
                s.close()
            if not s.is_open:
                logging.info('Serial opened at: {0}'.format(PORT))
                s.open()
        except serial.SerialException:
            logging.critical('Serial connection error')
            s = None
        return s
