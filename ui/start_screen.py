from ui.screen import Screen
from ui.buff_screen import BuffScreen
from ui.enhance_screen import EnhanceScreen
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
    
    def circus(self, call, state):
        pass

    def farming(self, call, state):
        Farming().run()
        return None, None

    def taming(self, call, state):
        Taming().run()
        return None, None

    def stop(self, call, state):
        Config().disable()
        return None, None
