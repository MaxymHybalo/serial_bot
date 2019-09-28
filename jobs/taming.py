from utils.config import Config
from processes.key import Key
import time

class Taming:

    def __init__(self):
        self.config = Config()
        self.config.enable()

    def run(self):
        while self.config.isWorks():
            Key('-').press()
            time.sleep(3)
            Key('=').press()
            time.sleep(13)
