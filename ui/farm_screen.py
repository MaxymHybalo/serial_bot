from ui.screen import Screen
from utils.configurator import Configurator
from jobs.farming import Farming
from utils.config import Config

class FarmScreen(Screen):

    def __init__(self, message, bot):
        super().__init__(message, bot)
        self.title = 'Famring options:'
        self.load_config()
        self._init_buttons()

    # Try to move this method do Screen class
    def load_config(self):
        self.configfile = Configurator(self.config['farming'])
        self.config = self.configfile.from_yaml()
        # print(self.config)

    def back(self, call, state):
        screen = 'StartScreen'
        ss = state[screen]
        ss.render(call=call)
        return 'StartScreen', ss

    def stop(self, call, state):
        Config().disable()
        return None, None

    def _init_buttons(self):
        for b in self.config['presets']:
            name = 'farm_{0}'.format(b['name'])
            def handle(call, state):
                data = call.data.split('_')[1]
                preset = self._findPreset(data)
                a = preset['actions']
                t = preset['timings']

                print('call key', data, a, t)
                Farming(a, t).run()
                return None, None
            setattr(self, name, handle)
        return None

    def render(self, call=None):
        self.markup.keyboard = []
        for i in self.config['presets']:
            title = '{0}'.format(i['name'])
            callback = '{name}.farm_{executor}'.format(name=self.name, executor=str(title))
            self.markup.add(self.InlineKeyboardButton(title, callback_data=callback))
        self.markup.add(self.InlineKeyboardButton('STOP', callback_data='{0}.{1}'.format(self.name, 'stop')))
        self.markup.add(self.InlineKeyboardButton('BACK', callback_data='{0}.{1}'.format(self.name, 'back')))

        if call is None:
            self.send()
        else:
            self.edit(call)

    def _findPreset(self, name):
        for p in self.config['presets']:
            if p['name'] == name:
                return p
        return []