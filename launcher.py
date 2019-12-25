import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import handlers
import logging
from utils.configurator import Configurator

from utils.config import Config

from ui.start_screen import StartScreen



CONFIG_FILE = 'config.yml'

MODES = [
        ('buff', 'enhance'),
        ('spawn','taming'), 
        ('logout','stop')
    ]

def configure_logger():
    log_format = '%(levelname)s : %(name)s %(asctime)s - %(message)s'
    logging.basicConfig(level=logging.INFO,
                        format=log_format,
                        datefmt='%d-%m %H:%M:%S')

def load_config():
    return Configurator(CONFIG_FILE).from_yaml()

configure_logger()
config = load_config()
bot = telebot.TeleBot(config['token'])
chat_id = None
message_id = None

state = dict()

@bot.message_handler(commands=['start'])
def start(message):
    ss = StartScreen(message, bot)
    state[ss.name] = ss
    ss.render()

def combination():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('atack', callback_data='atack'))
    markup.add(InlineKeyboardButton('armor', callback_data='armor'))
    markup.add(InlineKeyboardButton('<< Back', callback_data='back'))
    return markup

def atack():
    handlers.set_mode('combination', CONFIG_FILE)
    handlers.set_combination_mode('atack', config)
    handlers.run_bot()
    return None

def armor():
    handlers.set_mode('combination', CONFIG_FILE)
    handlers.set_combination_mode('armor', config)
    handlers.run_bot()
    return None

def cycles(cycle):
    handlers.set_enhance_mode('single', config)
    handlers.set_mode('enhance', CONFIG_FILE)
    handlers.set_cycles(cycle, config)
    handlers.run_bot()
    return None

def binary():
    handlers.set_mode('enhance', CONFIG_FILE)
    handlers.set_enhance_mode('binary', config)
    handlers.set_cycles(1, config)
    handlers.run_bot()
    return None

def spawn():
    handlers.set_spawn(config)
    handlers.run_bot()
    return None

def logout():
    handlers.set_mode('buff', CONFIG_FILE)
    handlers.set_logout(config)
    handlers.run_bot()
    return None

def buff():
    handlers.set_mode('buff', CONFIG_FILE)
    Config().mode = 'changed mode'
    handlers.set_buff(['buff'], config)
    handlers.run_bot()
    return None

def quests():
    handlers.set_mode('buff', CONFIG_FILE)
    handlers.set_logout(config)
    handlers.get_quests(config)
    return None

def taming():
    handlers.set_mode('taming', CONFIG_FILE)
    handlers.run_bot()

def farming():
    handlers.set_mode('farming', CONFIG_FILE)
    handlers.run_bot()

def stop():
    Config().disable()

def handle_child_nodes(data):
    if data[0] == 'cycle':
        return cycles(data[1])
    if data[0] == 'coords':
        handlers.set_cube(data[1:], config)
        return enhance()
    return None

def enhance():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('cube', callback_data='cube'))
    row = []
    for i in range(1, 5):
        title = 'cycles ' + str(i)
        callback = 'child_cycle_' + str(i) 
        row.append(InlineKeyboardButton(title, callback_data=callback))
    markup.row_width = 4
    markup.add(*row)
    markup.add(InlineKeyboardButton('binary', callback_data='binary'))
    markup.add(InlineKeyboardButton('<< Back', callback_data='back'))
    return markup

def cube():
    markup = InlineKeyboardMarkup()
    markup.row_width = 9
    for row in range(1, 12):
        line = []
        for col in range(1, 10):
            line.append(InlineKeyboardButton(str(col) + ':' + str(row), callback_data='child_coords_' + str(col) + '_' + str(row)))
        markup.row(*line)
    markup.add(InlineKeyboardButton('<< Enhance', callback_data='enhance'))
    return markup

def back():
    return create_base_keyboard()

def create_base_keyboard():
    markup = InlineKeyboardMarkup()
    keyboard = MODES
    for row in keyboard:
        line = [InlineKeyboardButton(key, callback_data=key) for key in row]
        markup.row(*line)
    markup.add(InlineKeyboardButton('combination', callback_data='combination'))
    markup.add(InlineKeyboardButton('farming', callback_data='farming'))
    markup.add(InlineKeyboardButton('Get cicus quest', callback_data='quests'))

    return markup

@bot.callback_query_handler(func=lambda call: True)
def handle_base_callbacks(call):
    screen, action = call.data.split('.')
    try:
        screen = state[screen]
        action_key, action_value = getattr(screen, action)(call, state)
        state[action_key] = action_value
    except KeyError:
        if screen == 'StartScreen':
            print('Start screen not defined')
            bot.answer_callback_query(call.id, 'StartScreen intiated, try again')
            start(call.message)

# @bot.callback_query_handler(func=lambda call: True)
# def handle_base_callbacks(call):
#     bot.answer_callback_query(call.id, 'Start ' + call.data)
#     data = call.data.split('_')
#     if data[0] == 'child':
#         handle = handle_child_nodes(data[1:])
#         print(handle)
#         if handle:
#             bot.edit_message_reply_markup(
#                 chat_id=call.message.chat.id,
#                 message_id=call.message.message_id,
#                 reply_markup=handle
#             )
#             return
#     markup = None
#     if len(data) == 1:
#         markup = globals()[data[0]]()
#     if not markup:
#         _start(call.message.chat.id)
#     else:
#         bot.edit_message_reply_markup(
#             chat_id=call.message.chat.id,
#             message_id=call.message.message_id,
#             reply_markup=markup
#         )

def _start(id):
    markup = create_base_keyboard()
    bot.send_message(id, "Let's start work", reply_markup=markup)

if not config['debug']:
    bot.polling()
else:
    handlers.run_bot()
