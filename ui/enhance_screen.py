from ui.screen import Screen
from ui.cubes_screen import CubesScreen
from ui.combination_screen import CombinationScreen
from utils.configurator import Configurator

from enhancer.invetory_dispatcher import InventoryDispatcher

class EnhanceScreen(Screen):

    buttons = ['Cube', 'Unpack', 'Disassamble', 'Binary', 'Combination', 'Back']

    def __init__(self, message, bot):
        super().__init__(message, bot)
        self.title = 'Enhance menu:'
        self.load_config()
        self.generate_cycles()

            
    def generate_cycles(self):
        for i in range(4):
            cycle_id = i+1
            attr_name = 'cycle_{0}'.format(cycle_id)

            def cycle(call, state):
                data = call.data.split('_')[1]
                self.config['enhancement']['cycles'] = data
                self.config['enhancement']['cube'] = state['CubesScreen'].config['enhancement']['cube']
                self.configfile.dump_yaml(self.config)
                self.bot.answer_callback_query(call.id, 'Start {0} cycles'.format(data))

                InventoryDispatcher(self.config).enhance()
                return self.name, self
            
            setattr(self, attr_name, cycle)
        return None

        
    def render(self, call=None):
        self.markup.keyboard = []
        cycles = []

        for i in range(1, 5):
            title = 'Сycles ' + str(i)
            callback = '{name}.cycle_{i}'.format(name=self.name, i=str(i))
            cycles.append(self.InlineKeyboardButton(title, callback_data=callback))
        self.markup.row_width = 4
        self.markup.add(*cycles)
        for b in self.buttons:
            self.markup.add(self.InlineKeyboardButton(b,
                            callback_data='{name}.{action}'.format(name=self.name, action=b.lower())))
        if call is None:
            self.send()
        else:
            self.edit(call)
    
    def cube(self, call, state):
        cs = CubesScreen(self.message, self.bot)
        cs.render(call=call)
        return cs.name, cs

    def unpack(self, call, state):
        InventoryDispatcher(self.config).unpack()
        return self.name, self
        
    def binary(self, call, state):
        self.config['enhancement']['cube'] = state['CubesScreen'].config['enhancement']['cube']
        self.config['mode'] = 'binary'
        self.configfile.dump_yaml(self.config)
        InventoryDispatcher(self.config).enhance() # TODO change when unifier will be ready
        return self.name, self

    def combination(self, call, state):
        cs = CombinationScreen(self.message, self.bot)
        cs.render(call=call)
        return cs.name, cs
    
    def disassamble(self, call, state):
        self.config['enhancement']['cube'] = state['CubesScreen'].config['enhancement']['cube']
        self.config['mode'] = 'disassamble'
        # Enhancer(self.config).process() # TODO when destructor implemented
        return self.name, self

    def back(self, call, state):
        screen = 'StartScreen'
        ss = state[screen]
        ss.render(call=call)
        return 'StartScreen', ss
    
    def load_config(self):
        self.configfile = Configurator(self.config['enhancer'])
        self.config = self.configfile.from_yaml()