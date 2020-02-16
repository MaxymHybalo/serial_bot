import bot

from utils.configurator import Configurator
from processes.instruction_processor import InstructionProcessor

AVAILABLE_MODES = ['buff', 'enhance', 'make', 'combination', 'return', 'taming', 'farming']


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


def get_quests(config):
    from utils.serial_controller import SerialController
    from jobs.helpers.circus_handler import CircusHandler
    from processes.wait import Wait
    from jobs.buffer import Buffer
    from utils.config import Config

    Config().initialize_configs(config['navigator'])

    if not SerialController().serial:
        SerialController().run_serial(config['serial']) 

    buff_cfg = Configurator(config['buffer']).from_yaml()
    buff = Buffer(buff_cfg)
    for i in range(8):
        CircusHandler().get_quest()
        Wait(2).delay()
        buff.process_flow()
