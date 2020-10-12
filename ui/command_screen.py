import logging
from utils.configurator import Configurator
from utils.config import Config

class CommandScreen:
    visible = False

    def __init__(self, message, bot):
        self.log = logging.getLogger('command-screen')
        self.message = message
        self.bot = bot

    def set_await(self, delay):
        enhancer = Config().config
        file = Configurator(enhancer['enhancer'])
        config = file.from_yaml()
        config['enhancement']['await'] = delay
        file.dump_yaml(config)
        self.log.info('Changed await')
