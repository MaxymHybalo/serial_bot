import logging

from enhancer.cell import Cell

def run():
    Cell().call()

class Enhancer:

    def __init__(self, config):
        self.log = logging.getLogger('enhancer-v2')
        self.log.info('Created new enhancer instance')
        self.log.info('Config, {0}'.format(config))