import cv2
import numpy as np
import time
import pyautogui as u

from shapes.window import Window

from jobs.helpers.extruder import Extruder, CharTitleConfig
from jobs.helpers.navigator import Navigator

from test.timerfunc import timerfunc
from test.tasks import make_extruder_env

TEMPLATE = 'assets/circus_flow/guide_siege_title.png'

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

@timerfunc
def move_to_npc(times=10, imagepath='assets/data/npc_extruded_by_char_color/'):
    template = cv2.imread(TEMPLATE)
    window = Window()

    for i in range(times):
        image = u.screenshot(region=window.rect)
        extruded = Extruder(image)
        title_roi = extruded.match_by_template(template, image=extruded.filtredImgByColor(CharTitleConfig))
        print(title_roi)
        Navigator.move_to_npc(title_roi)
        

def fetch_window(times, delay=2, dir='assets/data/screens/'):
    window = Window()
    id = 0
    while id < times:
        time.sleep(delay)
        img = u.screenshot(region=window.rect)
        img = np.array(img)
        cv2.imwrite(dir + str(id) + '.png', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        id = id + 1

@timerfunc
def run(times=30):
    make_extruder_env()
    fetch_window(times, delay=0.5)
    filter_img_by_color(times)
    match_by_template(times)
    move_to_npc(2)