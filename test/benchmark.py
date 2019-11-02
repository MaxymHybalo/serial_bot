import cv2
import pyautogui as u
import numpy as np
import time

from test.configs import buff_config
from processes.recognizer import Recognizer
from processes.key import Key
from utils.serial_controller import SerialController
from shapes.window import Window
from utils.configurator import Configurator
from jobs.helpers.extruder import Extruder, CharTitleConfig

from test.tasks import make_extruder_env

TEMPLATE = 'assets/circus_flow/guide_siege_title.png'

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
    config = Configurator('config.yml').from_yaml()
    SerialController().run_serial(config['serial'])

@timerfunc
def key():
    Key('0').press()

@timerfunc
def init_window():
    return  Window()


# running benchmarks
# init_window()
# menu_region_recognize()
# menu_recognize()
# serial_run()
# key()


# writes filtred images

@timerfunc
def filter_img_by_color(times=10):
    for i in range(times):
        image = cv2.imread('assets/data/screens/' + str(i) + '.png')
        extruded = Extruder(image)
        extruded = extruded.filtredImgByColor(CharTitleConfig)
        cv2.imwrite('assets/data/npc_extruded_by_char_color/' + str(i) + '.png', extruded)

@timerfunc
def match_by_template(times=11, imagepath='assets/data/screens/'):
    template = cv2.imread(TEMPLATE)
    for i in range(times):
        image = cv2.imread(imagepath + str(i) + '.png')
        extruded = Extruder(image)
        @timerfunc
        def test_extrude():
            return extruded.match_by_template(template)
        template_roi = test_extrude()
        result = cv2.rectangle(extruded.image, template_roi[:2], (template_roi[0] + template_roi[2], template_roi[1] + template_roi[3]), 255,2)
        cv2.imwrite('assets/data/npc_template_matched_1/' + str(i) + '.png', result)


def fetch_window(times, delay=2, dir='assets/data/screens/'):
    window = init_window()
    id = 0
    while id < times:
        time.sleep(delay)
        img = u.screenshot(region=window.rect)
        img = np.array(img)
        cv2.imwrite(dir + str(id) + '.png', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        id = id + 1

@timerfunc
def generate_guide_siege_area(times):
    make_extruder_env()
    fetch_window(times, delay=0.5)
    filter_img_by_color(times)
    match_by_template(times)

generate_guide_siege_area(40)