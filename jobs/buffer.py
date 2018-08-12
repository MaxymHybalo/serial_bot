import logging
from utils.configurator import Configurator

from processes.recognizer import Recognizer
from processes.wait import Wait
from processes.click import Click
from shapes.rect import Rect
from processes.key import Key

class Buffer:

    FLOW = [
        ['1','2','3','4','5'],
        ['1','2','3','4'],
        ['1'],
        ['1'],
        ['1'],
        ['1'],
        ['1'],
        ['2', '3','1']
    ]
    def __init__(self, configpath):
        self.log = logging.getLogger('buffer')
        self.config = Configurator(configpath).from_yaml()
        self.serial = None
        self.menu = self.__asset_path('menu')
        self.selector = self.__asset_path('selector')
        self.select_marker = self.__asset_path('select_menu')
        self.ok = self.__asset_path('ok')
        self.selector_ok = self.__asset_path('selector_ok')
        self.moon = self.__asset_path('moon')
        self.selected_char = self.__asset_path('selected_char_marker')

    def process(self, serial):
        self.serial = serial
        print(self.config)
        # wait just for testing
        Wait(2).delay()
        selector_ok = self._go_to_selector()
        self._detect_chars()
        self.process_flow()

    def process_flow(self):
        for buffer in self.FLOW:
            Rect(Recognizer(self.selector_ok, None).recognize()).click().make_click(self.serial)
            Recognizer(self.moon, None).recognize()
            for buff in buffer:
                Key(buff).press(self.serial)
                Wait(1).delay()
            self._go_to_selector()
            Key('D').press(self.serial)

    def _detect_chars(self):
        recognizer = Recognizer(self.selected_char, None)
        marker = recognizer.recognize(once=True)
        key = Key('D')
        print(marker)
        if marker:
            key.press(self.serial)
        while not marker:
            marker = recognizer.recognize(once=True)
            key.press(self.serial)

    def _go_to_selector(self):
        mode = self._setup_buff_mode()
        if mode:
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
            return True
        elif state is None:
            return 'Error!'
        else:
            return False

    def _game_state(self):
        game_state = Recognizer(self.menu, None).recognize(once=True)
        if not game_state:
            game_state = Recognizer(self.selector, None).recognize(once=True)
            if not game_state:
                return None
            return 'selector'
        return 'game'

    def __asset_path(self, asset):
        return self.config['asset_preffix'] + '/' + self.config['markers'][asset]