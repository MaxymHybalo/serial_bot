import logging
from utils.configurator import Configurator
from utils.config import Config

class CommandScreen:

    def __init__(self):
        super().__init__()
        self.log = logging.getLogger('command-screen')

    def set_await(self, delay):
        enhancer = Config().config
        file = Configurator(enhancer['enhancer'])
        config = file.from_yaml()
        config['enhancement']['await'] = delay
        file.dump_yaml(config)
        self.log.info('Changed await')
