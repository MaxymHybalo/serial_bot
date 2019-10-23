import time

from test.configs import buff_config
from processes.recognizer import Recognizer
from processes.key import Key
from utils.serial_controller import SerialController
from shapes.window import Window

# timer decorator
def timerfunc(func):
    def function_timer(*args, **kwargs):
        start = time.time()
        value = func(*args, **kwargs)
        end = time.time()
        runtime = end - start
        msg = "[{func}] took {time} sec. to complete"
        print(msg.format(func=func.__name__, time=round(runtime, 4)))
        return value
    return function_timer

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
    SerialController().run_serial({'baudrate': 9600, 'port': 12})

@timerfunc
def key():
    Key('0').press()

@timerfunc
def init_window():
    window = Window()


# running benchmarks
init_window()
menu_region_recognize()
menu_recognize()
serial_run()
key()