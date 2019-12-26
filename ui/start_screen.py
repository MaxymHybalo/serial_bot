from ui.screen import Screen
from ui.buff_screen import BuffScreen
from ui.enhance_screen import EnhanceScreen


class StartScreen(Screen):

    buttons = ['BUFF', 'ENHANCE', 'CIRCUS', 'FARMING', 'STOP']

    def __init__(self, message, bot):
        super().__init__(message, bot)
        self.title = 'Menu:'

    def buff(self, call, state):
        bs = state['BuffScreen'] if 'BuffScreen' in state else BuffScreen(self.message, self.bot)
        bs.render(call=call)
        return bs.name, bs

    def enhance(self, call, state):
        print('make_enhnace')
        bs = state['EnhanceScreen'] if 'EnhanceScreen' in state else EnhanceScreen(self.message, self.bot)
        bs.render(call=call)
        return bs.name, bs