import cv2
import numpy as np
import time
import pyautogui as u

from shapes.window import Window

from jobs.helpers.extruder import Extruder, CharTitleConfig, GuildIconConfig, StartPointConfig
# from jobs.helpers.navigator import Navigator

from test.timerfunc import timerfunc
from test.tasks import make_extruder_env
from utils.cv2_utils import show_image

TEMPLATE = 'assets/circus_flow/guide_siege_title.png'
GUILD_TEMPLATE = 'assets/circus_flow/guild_icon.png'
SCREENS = 'assets/data/screens/'

@timerfunc
def filter_img_by_color(times=10, color_shcheme=CharTitleConfig):
    for i in range(times):
        image = cv2.imread('assets/data/screens/' + str(i) + '.png')
        extruded = Extruder(image)
        extruded = extruded.filtredImgByColor(color_shcheme)
        # show_image(extruded)
        cv2.imwrite('assets/data/church/' + str(i) + '.png', extruded)

@timerfunc
def match_title_by_template(times=11, imagepath='assets/data/screens/'):
    template = cv2.imread(TEMPLATE)
    for i in range(times):
        image = cv2.imread(imagepath + str(i) + '.png')
        extruded = Extruder(image)
        @timerfunc
        def test_extrude():
            return extruded.match_by_template(template)
        template_roi = test_extrude()
        result = cv2.rectangle(extruded.image, template_roi[:2], (template_roi[0] + template_roi[2], template_roi[1] + template_roi[3]), 255,2)
        cv2.imwrite('assets/data/altar_matched/' + str(i) + '.png', result)

@timerfunc
def draw_matched(times, imagepath='assets/data/screens/', config=StartPointConfig):
    for i in range(times):
        print('[${i}]'.format(i=i))
        image = cv2.imread(imagepath + str(i) + '.png')
        e = Extruder(image)
        rect = e.get_template_rect(config)
        result = cv2.rectangle(e.image, rect[:2], (rect[0] + rect[2], rect[1] + rect[3]), 255,2)
        cv2.imwrite('assets/data/altar_matched/' + str(i) + '.png', result)

@timerfunc
def match_guild_by_template(times=10, imagepath="assets/data/screens/"):
    from utils.cv2_utils import draw_rect
    guild_template = cv2.imread(GUILD_TEMPLATE)
    for i in range(times):
        image = cv2.imread(imagepath + str(i) + '.png')
        extruder = Extruder(image)
        guild_roi = extruder.match_by_template(guild_template)
        print('guild_roi', guild_roi)
        # result = draw_rect(extruder.image, guild_roi)
        # cv2.imwrite('assets/data/guild_icons_match/' + str(i) + '.png', result)

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
    from utils.cv2_utils import screenshot
    id = 0
    while id < times:
        time.sleep(delay)
        @timerfunc
        def screen():
            return screenshot(window.rect)
        
        screen()

        @timerfunc
        def save():
            img = np.array(screen())
            cv2.imwrite(dir + str(id) + '.png', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        save()
        id = id + 1

@timerfunc
def get_guild_npc_rect(times=10):
    for i in range(times):
        image = cv2.imread(SCREENS + str(i) + '.png')
        e = Extruder(image)
        e.threshold(StartPointConfig)
        # titleRoi, guildRoi = extruder.get_template_rect(CharTitleConfig), extruder.get_template_rect(StartPointConfig)
        # print(i, titleRoi, guildRoi)

@timerfunc
def draw_corners(times=10):
    rx,ry,w,h = StartPointConfig.roi
    for i in range(times):
        image = cv2.imread(SCREENS + str(i) + '.png')
        e = Extruder(image)
        roi = e.threshold(StartPointConfig)
        roi = e.clear(roi)

        corners = e.corners(roi)
        if corners is not None:
            for c in corners:
                x,y = c.ravel()
                cv2.circle(image, (rx + x, ry + y), 3, 255, -1)
        cv2.rectangle(image, (rx,ry), (rx+w, ry+h),(0,200,0), 2)
        cv2.imwrite('assets/data/altar_matched/' + str(i) + '.png', image)


from processes.move import Move 

@timerfunc
def run(times=50):
    # make_extruder_env()
    # fetch_window(times, delay=0)
    # filter_img_by_color(times=times)
    # match_title_by_template(times=times)
    # move_to_npc(1)
    # match_guild_by_template(times=times, imagepath='assets/data/npc_extruded_by_char_color/')
    # get_guild_npc_rect(times=times)
    draw_corners(times=times)
    # title = Navigator.touch_circus_npc()
    # x, y, _, _ = title
    # Navigator.turn_around(title)    
    # fetch_window(times=times, delay=0)
    # draw_matched(times=times)
    # filter_img_by_color(4, color_shcheme=StartPointConfig)


    # from processes.wait import Wait
    # npc_title = Navigator.touch_circus_npc()
    # Navigator.turn_around(npc_title)
    # Wait(1).delay()
    # Navigator.go_to_start()
