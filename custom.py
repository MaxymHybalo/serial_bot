from processes.process import Process
from utils.configurator import Configurator
from processes.click import Click
from processes.wait import Wait
from processes.key import Key
import pyautogui as ui

config = Configurator('config.yml').from_yaml()

serial = Process(config['serial']).run_serial()

for i in range(0, 6):
    count = Click(536, 450, process='dclick') 
    count.make_click(serial)
    Wait(0.5).delay()

    on = Click(464, 451, process='dclick')
    on.make_click(serial)
    Wait(0.5).delay()

    one = Key('1')
    one.press(serial)
    Wait(0.5).delay()

    enter = Key('E')
    enter.press(serial)
    Wait(0.5).delay()

    make = Click(352, 492)
    make.make_click(serial)
    Wait(1).delay()
print(ui.position())