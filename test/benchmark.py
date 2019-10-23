import time

from test.configs import buff_config
from processes.recognizer import Recognizer
from processes.key import Key
from utils.serial_controller import SerialController

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
def moon_recognize():
    Recognizer(__asset_path(buff_config, 'moon'), None).recognize()

@timerfunc
def menu_recognize():
    Recognizer(__asset_path(buff_config, 'menu'), (640, 400, 640, 400)).recognize()

@timerfunc
def serial_run():
    SerialController().run_serial({'baudrate': 9600, 'port': 12})

@timerfunc
def key():
    Key('0').press()


# running benchmarks
menu_recognize()
moon_recognize()
serial_run()
key()