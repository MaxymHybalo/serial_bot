
import logging
import os

import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from ui.start_screen import StartScreen
from ui.command_screen import CommandScreen
from utils.config import Config

INVISIBLE_SCREENS = ('CommandScreen')

class Bot:

    def __init__(self, token):
        self.log = logging.getLogger('telebot')
        self.chat_id = None
        self.message_id = None
        self.state = dict()
        self.bot = telebot.TeleBot(token)
        self.setup()
        self.log.info('Inited {0}'.format(token))

    def observe(self):
        self.bot.polling()

    def setup(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.start(message)
        
        @self.bot.message_handler(commands=['await'])
        def start(message):
            self.set_await(message)

        @self.bot.callback_query_handler(func=lambda call: True)
        def callbacks(call):
            self.handle_base_callbacks(call)

    def set_await(self, message):
        # import pdb; pdb.set_trace()
        text = message.text
        delay = text.split()[1:]
        try:
            delay = float(delay[0])
        except Exception as e:
            self.log.error(str(e))
            return None

        CommandScreen().set_await(delay)

    def start(self, message):
        self.init_state(message, self.bot)

        ss = StartScreen(message, self.bot)
        self.state[ss.name] = ss
        ss.render()

    def handle_base_callbacks(self, call):
        try:
            self.proceed_screen(call)
        except KeyError as e:
            self.log.error(e)
            print('Start screen not defined')
            self.bot.answer_callback_query(call.id, 'StartScreen intiated, try again')
            self.init_state(call, self.bot)
            self.proceed_screen(call)
        except Exception as e:
            print(e)
            self.log.error(e)
            self.bot.answer_callback_query(str(e))
        except:
            e = 'Something went wrong'
            print(e)
            self.log.error(e)



    def init_state(self, message, bot):
        oldenv = os.getcwd()
        os.chdir(oldenv + '/ui')
        classes = {}
        modules = os.listdir()[:-1]
        os.chdir(oldenv)

        for m in modules:
            modname = m[:-3]
            classname = self.make_class_name(modname)
            if classname in INVISIBLE_SCREENS:
                continue
            classmodule = getattr(__import__('ui.' + modname), modname)
            class_tpl = getattr(classmodule, classname)
            classes[classname] = class_tpl
            
            cls = class_tpl(message, bot)
            self.state[cls.name] = cls

        globals().update(classes)

    def make_class_name(self, modulename):
        nameparts = modulename.split('_')
        name = ''
        for p in nameparts:
            name += p.capitalize()
        return name

    def proceed_screen(self, call):
        screen, action = call.data.split('.')
        screen = self.state[screen]
        action_key, action_value = getattr(screen, action)(call, self.state)
        if action_key:
            self.state[action_key] = action_value
