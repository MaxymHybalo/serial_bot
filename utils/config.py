from utils.singleton import Singleton

class Config(metaclass=Singleton):
    
    def __init__(self, *args, **kwargs):
        self.mode = 'test'
    
    def isWorks(self):
        return self.mode == 'enabled'
    
    def disable(self):
        self.mode = 'disabled'

    def enable(self):
        self.mode = 'enabled'