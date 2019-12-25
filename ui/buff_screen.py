from ui.screen import Screen
from jobs.buffer import Buffer

class BuffScreen(Screen):

    # another option for future
    buttons = ['Buff', 'Logout', 'Spawn', 'Back']

    def __init__(self, message, bot):
        super().__init__(message, bot)
        self.title = 'Buffer menu:'
        self.load_config()

    def load_config(self):
        from utils.configurator import Configurator
        self.config = Configurator(self.config['buffer']).from_yaml()

    def back(self, call, state):
        screen = 'StartScreen'
        ss = state[screen]
        ss.render(call=call)
        return 'StartScreen', ss

    def buff(self, call, state):
        self.bot.answer_callback_query(call.id, 'Start ' + call.data)
        
        Buffer(self.config).process()

        return self.name, self