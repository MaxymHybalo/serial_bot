from ui.screen import Screen
from ui.buff_screen import BuffScreen

class StartScreen(Screen):

    buttons = ['BUFF', 'ENHANCE', 'CIRCUS', 'FARMING', 'STOP']

    def __init__(self, message, bot):
        super().__init__(message, bot)
        self.title = 'Menu:'    

    def buff(self, call, state):
        print('make_buff')
        bs = state['BuffScreen'] if 'BuffScreen' in state else BuffScreen(self.message, self.bot)
        bs.render(call=call)

        # self.bot
        # before defintion check if markup exist at state
        # define BuffScreen and return itself key and instance
        return bs.name, bs