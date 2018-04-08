import logging
from utils.configurator import Configurator
from jobs.grid_layout import Grid

class Enhancer:

    def __init__(self, configpath):
        logging.getLogger()
        self.config = Configurator(configpath).from_yaml()

    def process(self):
        grid_image = self.__grid_identifier()
        Grid(grid_image)

    def __grid_identifier(self):
        path = self.config['recognize']['prefix']['path']
        prefix = self.config['recognize']['prefix']['image_suffix']
        image = self.config['recognize']['grid']['image']
        full_path = path + image + prefix
        logging.debug('Grid identifier: {0}'.format(full_path))
        return full_path

