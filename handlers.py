from utils.configurator import Configurator
import bot
from processes.instruction_processor import InstructionProcessor

AVAILABLE_MODES = ['buff', 'enhance', 'make', 'combination', 'return', 'taming']


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
    config['enhancement']['cube'] = [params[0], params[1]]
    configurator.dump_yaml(config)

def set_cycles(params, config):
    configurator = Configurator(config['enhancer'])
    config = configurator.from_yaml()
    config['enhancement']['cycles'] = params
    configurator.dump_yaml(config)


def set_enhance_mode(mode, config):
    configurator = Configurator(config['enhancer'])
    config = configurator.from_yaml()
    config['mode'] = mode
    configurator.dump_yaml(config)

def set_buff(params, config):
    configurator = Configurator(config['buffer'])
    config = configurator.from_yaml()
    config['refresh'] = True
    config['spawn'] = False
    configurator.dump_yaml(config)
    
def set_spawn(config):
    configurator = Configurator(config['buffer'])
    config = configurator.from_yaml()
    config['spawn'] = True
    config['logout'] = False
    configurator.dump_yaml(config)

def set_logout(config):
    configurator = Configurator(config['buffer'])
    config = configurator.from_yaml()
    config['spawn'] = True
    config['logout'] = True
    configurator.dump_yaml(config)

def set_combination_mode(mode, config):
    configurator = Configurator(config['enhancer'])
    config = configurator.from_yaml()
    config['combination']['mode'] = mode
    configurator.dump_yaml(config)

def run_bot():
    return bot.run()
