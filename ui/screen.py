from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class Screen:
    def __init__(self, message, bot):
        self.message = message
        self.bot = bot
        self.markup = InlineKeyboardMarkup()
        self.InlineKeyboardButton = InlineKeyboardButton
        self.title = 'Undefined'
        self.name = self.__class__.__name__

    def render(self, call=None):
        self.markup.keyboard = []

        for b in self.buttons:
            self.markup.add(self.InlineKeyboardButton(b,
                            callback_data='{name}.{action}'.format(name=self.name, action=b.lower())))
        
        if call is None:
            self.send()
        else:
            self.edit(call)
        
        
    def send(self):
        self.bot.send_message(self.message.chat.id, self.title, reply_markup=self.markup)
    
    def edit(self, call):
        self.bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=self.markup
        )
