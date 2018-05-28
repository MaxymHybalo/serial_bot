from utils.configurator import Configurator
import bot

AVAILABLE_MODES = ['buff', 'enhance']


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


def run_bot():
    return bot.run()
