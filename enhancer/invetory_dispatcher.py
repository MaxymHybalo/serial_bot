from utils.configurator import Configurator
from enhancer.inventory import Inventory
from enhancer.tasks.enhancer import Enhancer
from enhancer.tasks.unpacker import Unpacker
class InventoryDispatcher:
    
    def __init__(self, config):
        self.config = Configurator(config['enhancer']).from_yaml()
        self.inventory = Inventory(self.config)
        self.enhancers_setup = {
            'options': self.config['enhancement'],
            'assets': self.config['recognize']
        }

    def enhance(self):
        Enhancer(self.enhancers_setup, self.inventory).proceed()

    def unpack(self):
        Unpacker(self.enhancers_setup, self.inventory).proceed()