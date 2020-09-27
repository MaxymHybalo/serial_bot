import os
import logging

# import telebot
# from telebot import types
# from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.configurator import Configurator
from utils.config import Config

from utils.serial_controller import SerialController

# ---- development imports
from enhancer.invetory_dispatcher import InventoryDispatcher

from holder.bot import Bot
CONFIG_FILE = 'config.yml'


def configure_logger():
    log_format = '[%(levelname)s][%(name)s %(asctime)s]||%(message)s||'
    logging.basicConfig(level=logging.INFO,
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
# chat_id = None
# message_id = None

# state = dict()

# @bot.message_handler(commands=['start'])
# def start(message):
#     init_state(message, bot)

#     ss = StartScreen(message, bot)
#     state[ss.name] = ss
#     ss.render()

# def proceed_screen(call):
#     screen, action = call.data.split('.')
#     screen = state[screen]
#     action_key, action_value = getattr(screen, action)(call, state)
#     if action_key:
#         state[action_key] = action_value

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

# TODO remove to use bot
# if not config['debug']:
#     bot.polling()
# else:
# inv_dispatcher = InventoryDispatcher(config)
# inv_dispatcher.enhance()
# inv_dispatcher.unpack()
Bot(config['token']).observe()
