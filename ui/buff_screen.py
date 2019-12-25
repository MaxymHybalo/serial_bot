from ui.screen import Screen

class BuffScreen(Screen):

    # another option for future
    buttons = ['Buff', 'Logout', 'Spawn', 'Back']

    def __init__(self, message, bot):
        super().__init__(message, bot)
        self.title = 'Buffer menu:'    


    def back(self, call, state):
        screen = 'StartScreen'
        ss = state[screen]
        ss.render(call=call)
        return 'StartScreen', ss

    def buff(self, call, state):
        self.bot.answer_callback_query(call.id, 'Start ' + call.data)
        return self.name, self