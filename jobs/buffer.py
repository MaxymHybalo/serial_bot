import logging
from utils.configurator import Configurator

from processes.recognizer import Recognizer
from processes.wait import Wait
from processes.click import Click
from shapes.rect import Rect
from processes.key import Key

class Buffer:

    def __init__(self, configpath):
        self.log = logging.getLogger('buffer')
        self.config = Configurator(configpath).from_yaml()
        self.menu = self.config['asset_preffix'] + '/' + self.config['markers']['menu']
        self.selector = self.config['asset_preffix'] + '/' + self.config['markers']['selector']
        self.select_marker = self.config['asset_preffix'] + '/' + self.config['markers']['select_menu']
        self.ok = self.config['asset_preffix'] + '/' + self.config['markers']['ok']
        self.selector_ok = self.config['asset_preffix'] + '/' + self.config['markers']['selector_ok']
        self.moon = self.config['asset_preffix'] + '/' + self.config['markers']['moon']
        self.serial = None

    def process(self, serial):
        self.serial = serial
        print(self.config)
        # wait just for testing
        Wait(2).delay()
        selector_ok = self._go_to_selector()
        Rect(selector_ok).click().make_click(self.serial) # use after select buffer
        Recognizer(self.moon, None).recognize() # redy to buff marker

    def _go_to_selector(self):
        self._setup_buff_mode()
        select_button = Recognizer(self.select_marker, None).recognize()
        Rect(select_button).click().make_click(self.serial)
        ok = Recognizer(self.ok, None).recognize()
        Rect(ok).click().make_click(self.serial)
        return Recognizer(self.selector_ok, None).recognize()


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
