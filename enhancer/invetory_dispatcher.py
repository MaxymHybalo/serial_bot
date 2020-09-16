from utils.configurator import Configurator
from enhancer.inventory import Inventory
from enhancer.tasks.enhancer import Enhancer
class InventoryDispatcher:
    
    def __init__(self, config):
        self.config = Configurator(config['enhancer']).from_yaml()
        self.inventory = Inventory(self.config)

    def enhance(self):
        Enhancer({
            'mode': self.config['mode'],
            'options': self.config['enhancement'],
            'assets': self.config['recognize']
        }, self.inventory)
        # Enhancer(self.inventory)
