import time
import pyautogui as ui
import buff_instruction as buff
import enhance

from processors import InstructionProcessor
from click import Click
from configurator import Configurator
from recognizer import Recognizer

if __name__ == '__main__':
    startTime = time.time()
    # run()
    # print(buff.getBuffInstruction())
    # processInstruction(enhance.enhance())
    # processInstruction(buff.getBuffInstruction())
    # processor = InstructionProcessor(buff.getBuffInstruction())
    # processor = InstructionProcessor(Click(500, 300))
    # img = ui.screenshot(region=(242, 32, 337, 480))
    kwargs = {
        'roi': (0, 0, 280, 480),
        'color': ((0, 50, 50), (1, 255, 255)),
        'kernel': (2, 2)
    }
    rec = Recognizer('assets/inventory.JPG', None, **kwargs, process='find')
    processor = InstructionProcessor([rec, Click(400,500)])
    processor.process()
    execTime = (time.time() - startTime)

    print("Finished work, time:", execTime,'(sec) ', execTime / 60, '(min)')
