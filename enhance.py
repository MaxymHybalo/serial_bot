from click import Click

CUBE_X = 1
CUBE_Y = 1

START_ITEM_X = 1
START_ITEM_Y = 2

# now consistent  with grid
MAX_H_CELLS = 2
MAX_V_CELLS = 2

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
	return Click(values[_y][_x][0], values[_y][_x][1], process='dclick', delay=0.5)


def _enchance_move(x, y):
	clear_fix = Click(CLEAR_FIX[0], CLEAR_FIX[1], process='dclick', delay=0)
	enhance_point = Click(ENHANCE_POINT[0], ENHANCE_POINT[1], process='dclick', delay=2)
	break_point = Click(BREAK_POINT[0], BREAK_POINT[1], process='dclick', delay=2)
	return [
			getClick(x,y).instruction(),
			getClick(CUBE_X, CUBE_Y).instruction(),
			clear_fix.instruction(),
			enhance_point.instruction(),
			break_point.instruction()
		]

def _enhance(move):
	current_item_enhance = []
	for line in range(START_ITEM_Y, MAX_V_CELLS + 1):
		start_line = 1 if (len(current_item_enhance) > 0) else START_ITEM_X
		for col in range(start_line, MAX_H_CELLS + 1):
			current_item_enhance += move(col, line)
	return current_item_enhance

def enhance():
	loops = []
	for i in range(ITEM_ENHANCE_CYCLE):
		loops += _enhance(_enchance_move)
	return loops

