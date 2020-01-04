from ui.screen import Screen
from jobs.enhancer import Enhancer
from utils.configurator import Configurator

class CubesScreen(Screen):

    CELLS_ROW = 12
    CELLS_COL = 10

    def __init__(self, message, bot):
        super().__init__(message, bot)
        self.title = 'Select cube position:'
        self.load_config()
        self.generate_cubes()


    def generate_cubes(self):
        for i in range(1, self.CELLS_ROW):
            for j in range(1, self.CELLS_COL):
                attr_name = 'cube_{0}_{1}'.format(i, j)
                def cube(call, state):
                    self.set_cube_config(call)
                    es = state['EnhanceScreen']
                    es.render(call=call)
                    return 'EnhanceScreen', es
                
                setattr(self, attr_name, cube)
        return None

    def set_cube_config(self, call):
        data = call.data.split('_')[1:]
        data = data[::-1]
        self.config['enhancement']['cube'] = data
        self.bot.answer_callback_query(call.id, 'Set cube  {0}'.format(data))

    def render(self, call=None):
        self.markup.keyboard = []
        self.markup.row_width = self.CELLS_COL
        for i in range(1, self.CELLS_ROW):
            line = []
            for j in range(1, self.CELLS_COL):
                title = '{i}:{j}'.format(i=i, j=j)
                callback = '{name}.cube_{i}_{j}'.format(name=self.name, i=str(i), j=str(j))
                line.append(self.InlineKeyboardButton(title, callback_data=callback))
            self.markup.row(*line)
        
        if call is None:
            self.send()
        else:
            self.edit(call)
    
    def load_config(self):
        self.config = Configurator(self.config['enhancer']).from_yaml()