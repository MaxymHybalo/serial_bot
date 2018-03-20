import time
import pyautogui as p

repeats = 1 
count = 0

time.sleep(3)
# p.moveTo(85, 85)
while count < repeats:
	count += 1
	time.sleep(4)
	print(p.position())

# (242, 33)
# (579, 513)
