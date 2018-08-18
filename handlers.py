from utils.configurator import Configurator
import bot
from processes.instruction_processor import InstructionProcessor
from buff_instruction import to_reload

AVAILABLE_MODES = ['buff', 'enhance', 'make', 'combination', 'return']


def get_config(config):
    return 'Mode ' + config['mode'] + ', Serial port ' + str(config['serial']['port'])


def set_mode(mode, config):
    configurator = Configurator(config)
    config = configurator.from_yaml()
    if mode not in AVAILABLE_MODES:
        return 'Wrong mode name'
    config['mode'] = mode
    configurator.dump_yaml(config)
    return 'I change mode to ' + mode


def set_cube(params, config):
    configurator = Configurator(config['enhancer'])
    config = configurator.from_yaml()
    config['enhancement']['cube'] = [params[1], params[2]]
    configurator.dump_yaml(config)


def set_cycles(params, config):
    configurator = Configurator(config['enhancer'])
    config = configurator.from_yaml()
    config['enhancement']['cycles'] = params[1]
    configurator.dump_yaml(config)

def set_buff(params, config):
    configurator = Configurator(config['buffer'])
    config = configurator.from_yaml()
    if len(params) > 1:
        if params[1] == 'refresh':
            config['refresh'] = False
    else:
        config['refresh'] = True
    configurator.dump_yaml(config)
    

def make(params, config):
    params = params[1]
    if params == 'reload':
        procesor = InstructionProcessor(config['serial'], to_reload(is_return=True))
        bot.run(procesor)
    return 'Ok!'


def run_bot():
    return bot.run()
