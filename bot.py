import serial
import time
import pyautogui as ui
import buff_instruction as buff
import enhance

CLICK = b'C'

PORT = 'COM4'
BAUDRATE = 9600

s = serial.Serial(PORT, BAUDRATE)

SCREEN_SIZE = ui.size()

ACCURACY = 3

X_DIRECT = ('X', 'Z')
Y_DIRECT = ('Y', 'U')

def run():
  s.timeout = 0.1
  if not s.is_open:
    s.open()


def move(t):
  s.write(t.encode())


def search(x,y,):
  _x, _y = ui.position()
  next='X'
  isXPass = _isCoordLess(_x, x) and _isCoordGreater(_x, x)
  isYPass = _isCoordLess(_y, y) and _isCoordGreater(_y, y)
  while not (isXPass and isYPass):
    if next == 'X':
      if(_isCoordLess(_x, x)):
        move(X_DIRECT[1])
        next = 'Y' if not isYPass else 'X'
      else:
        move(X_DIRECT[0])
        next = 'Y' if not isYPass else 'X'
    if next == 'Y':
      if(_isCoordLess(_y, y)):
        move(Y_DIRECT[1])
        next = 'X' if not isXPass else 'Y'
      else:
        move(Y_DIRECT[0])
        next = 'X' if not isXPass else 'Y'
    _x, _y = ui.position()
    isXPass = _isCoordLess(_x, x) and _isCoordGreater(_x, x)
    isYPass = _isCoordLess(_y, y) and _isCoordGreater(_y, y)


def _isCoordLess(current, target):
  return current >= target - ACCURACY


def _isCoordGreater(current, target):
  return current <= target + ACCURACY



def click(x, y, delay):
  search(x, y)
  s.write(b'C')
  time.sleep(delay)

def double_click(x, y, delay):
  click(x, y, 0)
  click(x, y, delay)

def processInstruction(instruction):
  command = 0
  for e in instruction:
    command += 1
    print('[' + str(command) + '] ' + str(e))
    if e['process'] == 'click':
      click(e['x'], e['y'], e['delay'])
    if e['process'] == 'recognize':
      recognize(e)
    if e['process'] == 'wait':
      time.sleep(e['delay'])
    if e['process'] == 'center_on':
      center_on(e)
    if e['process'] == 'dclick':
      double_click(e['x'], e['y'], e['delay'])


def center_on(data):
  ins = recognize(data)
  print(data)
  click(ins[0] + ins[2] / 2, ins[1] + ins[3] / 2, 1)


def recognize(data):
  wait = int(data['freq'])
  value = ui.locateOnScreen(str(data['img']), region = data['region'])
  while (value is None):
    time.sleep(wait)
    value = ui.locateOnScreen(data['img'], region = data['region'])
  print(value)
  return value

if __name__ == '__main__':
  startTime = time.time()
  run()
  # print(buff.getBuffInstruction())
  # processInstruction(enhance.enhance())
  # prin/t(enhance.enhance())
  processInstruction(buff.getBuffInstruction())
  execTime = (time.time() - startTime)

  print("Finished work, time:", execTime,'(sec) ', execTime / 60, '(min)')
