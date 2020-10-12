from utils.configurator import Configurator
from enhancer.inventory import Inventory
from enhancer.tasks.enhancer import Enhancer
from enhancer.tasks.unpacker import Unpacker
from enhancer.tasks.destructor import Destructor
class InventoryDispatcher:
    
    def __init__(self, config):
        if type(config) is dict:
            self.config = config
        else:
            self.config = Configurator(config).from_yaml()
        self.inventory = Inventory(self.config)
        self.enhancers_setup = {
            'options': self.config['enhancement'],
            'assets': self.config['recognize']
        }

    def enhance(self):
        Enhancer(self.enhancers_setup, self.inventory).proceed()

    def unpack(self):
        Unpacker(self.enhancers_setup, self.inventory).proceed()
    
    def destroy(self):
        Destructor(self.enhancers_setup, self.inventory).proceed()