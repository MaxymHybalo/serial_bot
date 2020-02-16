from ui.screen import Screen
from jobs.buffer import Buffer
from utils.configurator import Configurator

class BuffScreen(Screen):

    # another option for future
    buttons = ['Buff', 'Logout', 'Spawn', 'Back']

    def __init__(self, message, bot):
        super().__init__(message, bot)
        self.title = 'Buffer menu:'
        self.load_config()

    def load_config(self):
        self.configfile = Configurator(self.config['buffer'])
        self.config = self.configfile.from_yaml()

    def back(self, call, state):
        screen = 'StartScreen'
        ss = state[screen]
        ss.render(call=call)
        return 'StartScreen', ss

    def buff(self, call, state):
        self.config['refresh'] = True
        self.config['logout'] = True
        self.configfile.dump_yaml(self.config)
        return self.run_action(call)

    def logout(self, call, state):
        self.config['spawn'] = True
        self.config['logout'] = True
        self.configfile.dump_yaml(self.config)
        return self.run_action(call)

    def spawn(self, call, state):
        self.config['spawn'] = True
        self.config['logout'] = False
        self.configfile.dump_yaml(self.config)
        return self.run_action(call)

    def run_action(self, call):
        self.bot.answer_callback_query(call.id, 'Start ' + call.data)
        Buffer(self.config).process()
        return self.name, self
