import logging

class Key:

    def __init__(self, key):
        self.key = key
        self.COMMAND = b'K'
        self.log = logging.getLogger('key')

    def press(self, serial):
        serial.write(self.COMMAND)
        serial.write(self.key.encode())
        self.log.debug('Press key: {0}'.format(self.key))