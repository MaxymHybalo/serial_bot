def get_config(config):
    return 'Mode ' + config['mode'] + ', Serial port ' + str(config['serial']['port'])


def set_mode(mode):
    print(mode)
    return mode
