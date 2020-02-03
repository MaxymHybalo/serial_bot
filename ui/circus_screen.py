from ui.screen import Screen

from utils.config import Config
from utils.configurator import Configurator
from jobs.helpers.circus_handler import CircusHandler
from jobs.buffer import Buffer

class CircusScreen(Screen):

    buttons = [['Get quests', 'quests'], ['Go to dungeon', 'dungeon'], ['Go to dungeon with party', 'party_dungeon'], ['Back', 'back']]

    def __init__(self, message, bot):
        super().__init__(message, bot)
        self.title = 'Circus:'
        self.load_config()

    def render(self, call=None):
        self.markup.keyboard = []
        for b in self.buttons:
            self.markup.add(self.InlineKeyboardButton(b[0],
                            callback_data='{name}.{action}'.format(name=self.name, action=b[1].lower())))
        if call is None:
            self.send()
        else:
            self.edit(call)

    def quests(self, call, state):
        self.bot.answer_callback_query(call.id, 'Get circus quests')

        buff_cfg = Configurator(self.config['buffer']).from_yaml()
        buff_cfg['spawn'] = True
        buff_cfg['logout'] = True

        buff = Buffer(buff_cfg)

        for i in range(8):
            CircusHandler().get_quest()
            buff.process_flow()

        return None, None

    def dungeon(self, call, state):
        CircusHandler().go_to_dungeon(False)
        return None, None

    def party_dungeon(self, call, state):
        CircusHandler().go_to_dungeon(True)
        return None, None

    def back(self, call, state):
        ss = state['StartScreen']
        ss.render(call=call)
        return ss.name, ss

    def load_config(self):
        Config().initialize_configs(self.config['navigator'])