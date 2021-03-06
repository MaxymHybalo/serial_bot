from test.timerfunc import timerfunc

from test.configs import buff_config
from processes.recognizer import Recognizer
from processes.key import Key
from utils.serial_controller import SerialController
from shapes.window import Window
from utils.configurator import Configurator

def __asset_path(config, asset):
    return config['asset_preffix'] + '/' + config['markers'][asset]

@timerfunc
def menu_recognize():
    Recognizer(__asset_path(buff_config, 'menu'), None).recognize()

@timerfunc
def menu_region_recognize():
    window = Window()
    center = window.center()
    @timerfunc
    def recognize():
        region = (int(center[0]), int(center[1]), int(window.width / 2), int(window.height / 2))
        Recognizer(__asset_path(buff_config, 'menu'), region).recognize()
    recognize()

@timerfunc
def serial_run():
    config = Configurator('config.yml').from_yaml()
    SerialController().run_serial(config['serial'])

@timerfunc
def key():
    Key('0').press()

@timerfunc
def init_window():
    return  Window()


@timerfunc
def run():
    # init_window()
    # menu_region_recognize()
    # menu_recognize()
    serial_run()
    # key()