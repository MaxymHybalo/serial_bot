class Key:

    def __init__(self, key):
        self.key = key
        self.COMMAND = b'K'

    def press(self, serial):
        serial.write(self.COMMAND)
        serial.write(self.key.encode())