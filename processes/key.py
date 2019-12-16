import logging
from utils.serial_controller import SerialController

class Key:
    
    COMMAND = b'K'
    RELEASE = b'Q'

    def __init__(self, key):
        self.key = key
        self.log = logging.getLogger('key')

    def press(self, serial=SerialController()):
        if hasattr(serial, 'serial'):
            serial = serial.serial
        serial.write(self.COMMAND)
        serial.write(self.key.encode())
        serial.write(self.RELEASE)

        self.log.debug('Press key: {0}'.format(self.key))