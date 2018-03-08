from click import Click

CUBE_X = 1
CUBE_Y = 1

START_ITEM_X = 1
START_ITEM_Y = 2

# now consistent  with grid
MAX_H_CELLS = 11
MAX_V_CELLS = 11

ITEM_ENHANCE_CYCLE = 3 

START_POINT = (85, 85)
ENHANCE_POINT = (132, 693)
BREAK_POINT = (134, 628)
CLEAR_FIX = (260, 605)

DELTA = 35

# ferquently used clicks
clear_fix = Click(CLEAR_FIX[0], CLEAR_FIX[1], process='dclick', delay=0)
enhance_point = Click(ENHANCE_POINT[0], ENHANCE_POINT[1], process='dclick', delay=2)
break_point = Click(BREAK_POINT[0], BREAK_POINT[1], process='dclick', delay=2)
comb_ok = Click(585, 440)

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
	
	return [
			getClick(x,y),
			getClick(CUBE_X, CUBE_Y),
			clear_fix,
			enhance_point,
			break_point
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

# x & y is tuples of two combination el
def _combination_move(x, y):
	return [
		getClick(x[0], x[1]),
		__select_count(5),
		comb_ok,
		getClick(y[0], y[1]),
		__select_count(7),
		comb_ok,
		enhance_point
	]
	
def __select_count(digit):
	point = __combination_diget_grid(digit)
	return Click(point[0], point[1])

def __combination_diget_grid(digit):
	one = [638, 422]
	delta = 20
	if digit > 3:
		one[1] -= delta
	if digit > 6:
		one[1] -= delta

	if digit in [8, 5, 2]:
		one[0] += delta
	if digit in [9, 6, 3]:
		one[0] += delta
	if digit == 0:
		one = [658, 442]
	return one

def combination():
	instruction = []
	for i in range(ITEM_ENHANCE_CYCLE):
		instruction += _combination_move((1,11), (2,11))
	return instruction
