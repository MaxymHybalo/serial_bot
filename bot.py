import time
import buff_instruction as buff
import enhance

from processors import InstructionProcessor
from click import Click


# def processInstruction(instruction):
#   command = 0
#   for e in instruction:
#     command += 1
#     print('[' + str(command) + '] ' + str(e))
#     if e['process'] == 'click':
#       click(e['x'], e['y'], e['delay'])
#     if e['process'] == 'recognize':
#       recognize(e)
#     if e['process'] == 'wait':
#       time.sleep(e['delay'])
#     if e['process'] == 'center_on':
#       center_on(e)
#     if e['process'] == 'dclick':
#       double_click(e['x'], e['y'], e['delay'])


# def center_on(data):
#   ins = recognize(data)
#   print(data)
#   click(ins[0] + ins[2] / 2, ins[1] + ins[3] / 2, 1)


# def recognize(data):
#   wait = int(data['freq'])
#   value = ui.locateOnScreen(str(data['img']), region = data['region'])
#   while (value is None):
#     time.sleep(wait)
#     value = ui.locateOnScreen(data['img'], region = data['region'])
#   print(value)
#   return value

if __name__ == '__main__':
  startTime = time.time()
  # run()
  # print(buff.getBuffInstruction())
  # processInstruction(enhance.enhance())
  # print(enhance.enhance())
  # processInstruction(buff.getBuffInstruction())

  processor = InstructionProcessor([Click(100,200), Click(320, 230, process="dclick")])
  processor.process()

  execTime = (time.time() - startTime)

  print("Finished work, time:", execTime,'(sec) ', execTime / 60, '(min)')
