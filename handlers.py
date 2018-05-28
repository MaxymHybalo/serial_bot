from utils.configurator import Configurator

AVAILABLE_MODES = ['buff', 'enhance']


def get_config(config):
    return 'Mode ' + config['mode'] + ', Serial port ' + str(config['serial']['port'])


def set_mode(mode, config):
    if len(mode) <= 1:
        return 'You forget give me mode name'
    mode = mode[1]
    configurator = Configurator(config)
    config = configurator.from_yaml()
    if mode not in AVAILABLE_MODES:
        return 'Wrong mode name'
    config['mode'] = mode
    configurator.dump_yaml(config)
    return 'I change mode to ' + mode

