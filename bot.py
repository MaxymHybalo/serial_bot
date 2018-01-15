import serial
import time
import pyautogui as ui
import buff_instruction as buff
import enhance

CLICK = b'C'

PORT = 'COM4'
BAUDRATE = 9600

# s = serial.Serial(PORT, BAUDRATE)

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


def search(goal, dim, direction):
  coord = ui.position()[dim]
  while not (coord <= goal + ACCURACY and coord >= goal - ACCURACY):
    if coord >= goal + ACCURACY:
      move(direction[1])
    else:
      move(direction[0])
    coord = ui.position()[dim]


def click(x, y, delay):
  search(x, 0, X_DIRECT)
  search(y,1, Y_DIRECT)
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

  # run()
  # enhance_loops = 3
  # for i in range(1):
  # processInstruction(enhance.enhance())
  print(enhance.enhance())
  # processInstruction(buff.getBuffInstruction())

  print("Finished work")
