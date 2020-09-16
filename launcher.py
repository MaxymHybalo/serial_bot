import os
import logging

# import telebot
# from telebot import types
# from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# import handlers
from utils.configurator import Configurator
from utils.config import Config

# from ui.start_screen import StartScreen
from utils.serial_controller import SerialController

# ---- development imports
from enhancer.invetory_dispatcher import InventoryDispatcher

CONFIG_FILE = 'config.yml'

MODES = [
        ('buff', 'enhance'),
        ('spawn','taming'), 
        ('logout','stop')
    ]

def configure_logger():
    log_format = '[%(levelname)s][%(name)s %(asctime)s]||%(message)s||'
    logging.basicConfig(level=logging.DEBUG,
                        format=log_format,
                        datefmt='%d-%m %H:%M:%S')

def load_config():
    cfg = Config()
    cfg.load_config(CONFIG_FILE)
    return cfg.config

configure_logger()
config = load_config()
SerialController().run_serial(config['serial'])
# bot = telebot.TeleBot(config['token'])
chat_id = None
message_id = None

state = dict()

# @bot.message_handler(commands=['start'])
# def start(message):
#     init_state(message, bot)

#     ss = StartScreen(message, bot)
#     state[ss.name] = ss
#     ss.render()

def quests():
    handlers.set_mode('buff', CONFIG_FILE)
    handlers.set_logout(config)
    handlers.get_quests(config)
    return None


def proceed_screen(call):
    screen, action = call.data.split('.')
    screen = state[screen]
    action_key, action_value = getattr(screen, action)(call, state)
    if action_key:
        state[action_key] = action_value

# @bot.callback_query_handler(func=lambda call: True)
# def handle_base_callbacks(call):
#     try:
#         proceed_screen(call)
#     except KeyError as e:
#         logging.error(e)
#         print('Start screen not defined')
#         bot.answer_callback_query(call.id, 'StartScreen intiated, try again')
#         init_state(call, bot)
#         proceed_screen(call)
#     except Exception as e:
#         print(e)
#         logging.error(e)
#         bot.answer_callback_query(str(e))
#     except:
#         e = 'Something went wrong'
#         print(e)
#         logging.error(e)


def init_state(message, bot):
    oldenv = os.getcwd()
    os.chdir(oldenv + '/ui')
    classes = {}
    modules = os.listdir()[:-1]
    os.chdir(oldenv)

    for m in modules:
        modname = m[:-3]
        classname = make_class_name(modname)
        classmodule = getattr(__import__('ui.' + modname), modname)
        class_tpl = getattr(classmodule, classname)
        classes[classname] = class_tpl
        
        cls = class_tpl(message, bot)
        state[cls.name] = cls

    globals().update(classes)

def make_class_name(modulename):
    nameparts = modulename.split('_')
    name = ''
    for p in nameparts:
        name += p.capitalize()
    return name

# TODO remove to use bot
# if not config['debug']:
#     bot.polling()
# else:
#     handlers.run_bot()
inv_dispatcher = InventoryDispatcher(config)
inv_dispatcher.enhance()