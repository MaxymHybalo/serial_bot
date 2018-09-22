import logging
from utils.configurator import Configurator

from processes.recognizer import Recognizer
from processes.wait import Wait
from processes.click import Click
from shapes.rect import Rect
from processes.key import Key

class Buffer:

    FLOW = [
        ['1','7','2','3','4','5'],
        ['1','6','2','3','4', '5'],
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
        self.process_flow()

    def process_flow(self):
        if self.config['spawn']:
            if not self.config['logout']:
                Key('0').press(self.serial)
                Wait(10).delay()
            Recognizer(self.moon, None).recognize()
            self._go_to_selector()
            Key('U').press(self.serial)
            Wait(0.5).delay()
            Key('E').press(self.serial)
            Recognizer(self.moon, None).recognize()
            return
        self._go_to_selector()
        self._detect_chars()
        if self.config['buff']:
            self._go_over_chars(self._buff_flow)
        if self.config['refresh']:
            self._go_over_chars(self._refresh_flow)
            Key('E').press(self.serial)

    def _buff_flow(self, *arg):
        for buff in arg:
            Key(buff).press(self.serial)
            Wait(1.5).delay()
        self._go_to_selector()
        
    def _refresh_flow(self, *arg):
        Wait(5).delay()
        self._go_to_selector()

    def _go_over_chars(self, handle):
        for flow in self.FLOW:
            self._next_char()
            handle(*flow)
            self._go_to_selector()

    def _detect_chars(self):
        recognizer = Recognizer(self.selected_char, None)
        marker = recognizer.recognize()
        marker = Rect(marker).click()
        marker.process = 'click'
        marker.make_click(self.serial)
    
    def _next_char(self):
        Key('D').press(self.serial)
        Wait(1).delay()
        Key('E').press(self.serial)
        Recognizer(self.moon, None).recognize()

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