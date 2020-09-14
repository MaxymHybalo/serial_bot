from utils.configurator import Configurator
from enhancer.inventory import Inventory

class InventoryDispatcher:
    
    def __init__(self, config):
        self.config = Configurator(config['enhancer']).from_yaml()
        self.inventory = Inventory(self.config)