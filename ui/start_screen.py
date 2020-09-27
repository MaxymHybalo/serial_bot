from ui.screen import Screen
from ui.buff_screen import BuffScreen
from ui.enhance_screen import EnhanceScreen
from ui.circus_screen import CircusScreen
from ui.farm_screen import FarmScreen
from jobs.farming import Farming
from jobs.taming import Taming
from utils.config import Config

class StartScreen(Screen):

    buttons = ['BUFF', 'ENHANCE', 'CIRCUS', 'FARMING', 'TAMING', 'STOP']

    def __init__(self, message, bot):
        super().__init__(message, bot)
        self.title = 'Menu:'

    def buff(self, call, state):
        bs = state['BuffScreen'] if 'BuffScreen' in state else BuffScreen(self.message, self.bot)
        bs.render(call=call)
        return bs.name, bs

    def enhance(self, call, state):
        bs = state['EnhanceScreen'] if 'EnhanceScreen' in state else EnhanceScreen(self.message, self.bot)
        bs.render(call=call)
        return bs.name, bs
        return None
        
    def circus(self, call, state):
        cs = CircusScreen(self.message, self.bot)
        cs.render(call=call)
        return cs.name, cs

    def farming(self, call, state):
        fs = FarmScreen(self.message, self.bot)
        fs.render(call=call)
        return fs.name, fs

    def taming(self, call, state):
        Taming().run()
        return None, None

    def stop(self, call, state):
        Config().disable()
        return None, None
