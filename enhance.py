from variables import *

CUBE_X = 1
CUBE_Y = 6

START_ITEM_X = 2
START_ITEM_Y = 6

# now consistent  with grid
MAX_H_CELLS = 10
MAX_V_CELLS = 10

ITEM_ENHANCE_CYCLE = 1 

START_POINT = (85, 85)
ENHANCE_POINT = (132, 693)
BREAK_POINT = (134, 628)
CLEAR_FIX = (260, 605)

DELTA = 35

def getMatrix():
	values = []
	for y in range(MAX_V_CELLS):
		values.append([])
		for x in range(MAX_H_CELLS):
			calcX = DELTA * x + START_POINT[0]
			calcY = DELTA * y + START_POINT[1]
			values[y].append((calcX, calcY))
	return values


def getClick(_x, _y):
	values = getMatrix()
	_x -= 1
	_y -= 1
	return {
		x: values[_y][_x][0],
		y: values[_y][_x][1],
		delay: 0.5,
		process: 'dclick'
	}


def _enchance_move(x, y):
	return [
			getClick(x,y),
			getClick(CUBE_X, CUBE_Y),
			click(CLEAR_FIX[0], CLEAR_FIX[1], 0),
			click(ENHANCE_POINT[0], ENHANCE_POINT[1]),
			click(BREAK_POINT[0], BREAK_POINT[1], 1)
		]

def _enhance():
	current_item_enhance = []
	for line in range(START_ITEM_Y, MAX_V_CELLS + 1):
		start_line = 1 if (len(current_item_enhance) > 0) else START_ITEM_X
		for col in range(start_line, MAX_H_CELLS + 1):
			current_item_enhance += _enchance_move(col, line)
	return current_item_enhance

def enhance():
	loops = []
	for i in range(ITEM_ENHANCE_CYCLE):
		loops += _enhance()
	return loops

def click(_x, _y, _delay = 2):
	return {
		process: 'dclick',
		x: _x,
		y: _y,
		delay: _delay
	}
