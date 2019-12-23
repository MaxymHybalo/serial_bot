from ui.screen import Screen
class StartScreen(Screen):

    buttons = ['BUFF', 'ENHANCE', 'CIRCUS', 'FARMING', 'STOP']

    def __init__(self, message, bot):
        super().__init__(message, bot)
        self.title = 'Menu:'    

    def render(self):
        for b in self.buttons:
            self.markup.add(self.InlineKeyboardButton(b,
                            callback_data='{name}.{action}'.format(name=self.name, action=b.lower())))
        
        self.send()

    def buff(self, state):
        print('make_buff')
        # self.bot
        # before defintion check if markup exist at state
        # define BuffScreen and return itself key and instance
        return 'BuffScreen', 14