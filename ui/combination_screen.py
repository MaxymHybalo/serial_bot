from ui.screen import Screen
from utils.configurator import Configurator

from jobs.combinator import Combinator
class CombinationScreen(Screen):

    buttons = ['Armor', 'Atack', 'Back']
    
    def __init__(self, message, bot):
        super().__init__(message, bot)
        self.title = 'Combination menu:'
        self.load_config()

    def armor(self, call, state):
        self.config['combination']['mode'] = 'armor'
        Combinator(self.config).process()
        return self.to_enhance(call, state)


    def atack(self, call, state):
        self.config['combination']['mode'] = 'atack'
        Combinator(self.config).process()
        return self.to_enhance(call, state)

    def back(self, call, state):
        return self.to_enhance(call, state)

    def to_enhance(self,call, state):
        es = state['EnhanceScreen']
        es.render(call=call)
        return 'EnhanceScreen', es

    def load_config(self):
        self.config = Configurator(self.config['enhancer']).from_yaml()