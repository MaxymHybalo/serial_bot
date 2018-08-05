import serial
import logging
from processes.process import Process

class ProcessInitializer(Process):

    def __init__(self, target, config):
        super().__init__(config)
        self.target = target
        self.serial = self.run_serial()
        logging.getLogger()

    def handle(self):
        self.target.process(self.serial)