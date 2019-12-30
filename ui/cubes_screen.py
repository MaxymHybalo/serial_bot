from ui.screen import Screen
from jobs.enhancer import Enhancer
from utils.configurator import Configurator

class CubesScreen(Screen):

    def __init__(self, message, bot):
        super().__init__(message, bot)
        self.title = 'Select cube position:'
        self.load_config()
        self.generate_cubes()


    def generate_cubes(self):
        for i in range(4):
            cycle_id = i+1
            attr_name = 'cycle_{0}'.format(cycle_id)

            def cycle(call, state):
                data = call.data.split('_')[1]
                self.config['enhancement']['cycles'] = data
                self.bot.answer_callback_query(call.id, 'Start {0} cycles'.format(data))
                es = state['EnhanceScreen']
                es.render(call=call)
                return 'EnhanceScreen', es
            
            setattr(self, attr_name, cycle)
        return None


    def render(self, call=None):
            self.markup.keyboard = []
            cycles = []

            for i in range(1, 5):
                title = '1:' + str(i)
                callback = '{name}.cycle_{i}'.format(name=self.name, i=str(i))
                cycles.append(self.InlineKeyboardButton(title, callback_data=callback))
            self.markup.row_width = 4
            self.markup.add(*cycles)
            
            if call is None:
                self.send()
            else:
                self.edit(call)
    
    def load_config(self):
        self.config = Configurator(self.config['enhancer']).from_yaml()