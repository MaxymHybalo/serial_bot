import logging
from utils.configurator import Configurator

from processes.recognizer import Recognizer
from processes.wait import Wait
from processes.key import Key

class Buffer:

    def __init__(self, configpath):
        self.log = logging.getLogger('buffer')
        self.config = Configurator(configpath).from_yaml()
        self.menu = self.config['asset_preffix'] + '/' + self.config['markers']['menu']
        self.selector = self.config['asset_preffix'] + '/' + self.config['markers']['selector']

        self.serial = None

    def process(self, serial):
        self.serial = serial
        print(self.config)
        # wait just for testing
        Wait(2).delay()
        self._setup_buff_mode()


    def _setup_buff_mode(self):
        state = self._game_state()
        if state is 'game':
            # go to selector
            Key('z').press(self.serial)
        elif state is None:
            return 'Error!'
        else:
            # buff chains next
            pass

    def _game_state(self):
        game_state = Recognizer(self.menu, None).recognize(once=True)
        if not game_state:
            game_state = Recognizer(self.selector, None).recognize(once=True)
            if not game_state:
                return None
            return 'selector'
        return 'game'
