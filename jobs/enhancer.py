from utils.configurator import Configurator


class Enhancer:

    def __init__(self, configpath):
        self.config = Configurator(configpath).from_yaml();

    def process(self):
        print(self.__grid_identifier())
        grid_image = self.__grid_identifier()




    def __grid_identifier(self):
        path = self.config['recognize']['prefix']['path']
        prefix = self.config['recognize']['prefix']['path']
        image = self.config['recognize']['grid']['image']
        return path + image + prefix

