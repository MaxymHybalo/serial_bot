import serial
import logging


class ObjectProcessor:

    def __init__(self, target, config):
        self.target = target
        self.config = config
        self.serial = self._run_serial()
        logging.getLogger()

    def handle(self):
        self.target.process(self.serial)

    def _run_serial(self):
        try:
            port = 'COM' + str(self.config['port'])
            baudrate = self.config['baudrate']
            logging.critical('Trying connect to Arduino via {0}'.format(port))
            s = serial.Serial(port, baudrate)
            s.timeout = 0.01
            if s.is_open:
                s.close()
            if not s.is_open:
                logging.info('Serial opened at: {0}'.format(port))
                s.open()
        except serial.SerialException:
            logging.critical('Serial connection error')
            s = None
        return s
