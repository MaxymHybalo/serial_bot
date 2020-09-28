import logging

from utils.configurator import Configurator
from utils.config import Config
from utils.serial_controller import SerialController
from holder.bot import Bot

CONFIG_FILE = 'config.yml'

def configure_logger():
    log_format = '[%(levelname)s][%(name)s %(asctime)s]||%(message)s||'
    logging.basicConfig(level=logging.INFO,
                        format=log_format,
                        datefmt='%d-%m %H:%M:%S')

def load_config():
    cfg = Config()
    cfg.load_config(CONFIG_FILE)
    return cfg.config

config = load_config()
configure_logger()
SerialController().run_serial(config['serial'])
# Bot(config['token']).observe()

from enhancer.invetory_dispatcher import InventoryDispatcher
inv_dispatcher = InventoryDispatcher(config['enhancer'])
inv_dispatcher.destroy()
