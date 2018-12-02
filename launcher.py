import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import handlers
import logging
from utils.configurator import Configurator

CONFIG_FILE = 'config.yml'

MODES = ['buff', 'spawn', 'logout', 'enhance']
def configure_logger():
    log_format = '%(levelname)s : %(name)s %(asctime)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        format=log_format,
                        datefmt='%d-%m %H:%M:%S')

def load_config():
    return Configurator(CONFIG_FILE).from_yaml()

configure_logger()
config = load_config()
bot = telebot.TeleBot(config['token'])

@bot.message_handler(commands=['start'])
def start(message):
    markup = create_base_keyboard()
    bot.send_message(message.chat.id, "Let's start work", reply_markup=markup)

@bot.message_handler(commands=['config'])
def config_handler(message):
    bot.send_message(message.chat.id, handlers.get_config(config))

@bot.message_handler(commands=['mode'])
def mode_handler(message):
    mode = validate(message, message.chat.id)
    if len(mode) > 1:
        mode = mode[1]
    else:
        return None
    bot.send_message(message.chat.id, handlers.set_mode(mode, CONFIG_FILE))

@bot.message_handler(commands=['run'])
def run_handler(message):
    bot.send_message(message.chat.id, 'Okay, just run for you this')
    final = handlers.run_bot()
    bot.send_message(message.chat.id, 'Good, that\'s all, just in ' + str(final/60))

@bot.message_handler(commands=['cube'])
def cube_handler(message):
    mode = validate(message, message.chat.id)
    if len(mode) > 1:
        handlers.set_cube(mode, config)
    bot.send_message(message.chat.id, 'Maybe I update cube position')

def cycles(cycle):
    handlers.set_cycles(cycle, config)
    handlers.run_bot()

def spawn():
    handlers.set_spawn(config)
    handlers.run_bot()

def logout():
    handlers.set_logout(config)
    handlers.run_bot()

def buff():
    handlers.set_mode('buff', CONFIG_FILE)

def enhance(id):
    markup = InlineKeyboardMarkup()
    keyboard = [
        {
            'title': 'cycles 1',
            'data': 'child_cycle_1',
        },
        {
            'title': 'cycles 3',
            'data': 'child_cycle_3',
        },
        {
            'title': 'cycles 4',
            'data': 'child_cycle_4',
        }
    ]
    markup.add(InlineKeyboardButton('cube', callback_data='cube'))
    row = []
    for c_key in keyboard:
        row.append(InlineKeyboardButton(c_key['title'], callback_data=c_key['data']))
    markup.add(*row)
    bot.send_message(id, 'Enhance menu', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_base_callbacks(call):
    bot.answer_callback_query(call.id, 'Start ' + call.data)
    data = call.data.split('_')
    print(data, data[0] is 'child')
    if data[0] == 'child':
        handle_child_nodes(data[1:])
        bot.answer_callback_query(call.id, 'End ' + call.data)
        return
    globals()[data[0]](call.message.chat.id)
    bot.answer_callback_query(call.id, 'End ' + call.data)
            
def handle_child_nodes(data):
    if data[0] == 'cycle':
        cycles(data[1])

def validate(params, id):
    mode = params.text.split(' ')
    if len(mode) <= 1:
        bot.send_message(id, 'You forget give me mode name')
    return mode

def create_base_keyboard():
    markup = InlineKeyboardMarkup()
    keyboard = MODES
    for key in keyboard:
        markup.add(InlineKeyboardButton(key, callback_data=key))
    return markup

if not config['debug']:
    bot.polling()
else:
    handlers.run_bot()

