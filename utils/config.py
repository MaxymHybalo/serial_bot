from utils.singleton import Singleton

class Config(metaclass=Singleton):
    
    def __init__(self, *args, **kwargs):
        self.mode = 'test'