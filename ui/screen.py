from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class Screen:
    def __init__(self, message, bot):
        self.message = message
        self.bot = bot
        self.markup = InlineKeyboardMarkup()
        self.InlineKeyboardButton = InlineKeyboardButton
        self.title = 'Undefined'
        self.name = self.__class__.__name__

    def send(self):
        self.bot.send_message(self.message.chat.id, self.title, reply_markup=self.markup)