import variables as var

START_POINT = (85, 85)
MAX_H_CELLS = 6
MAX_V_CELLS = 3

CUBE_X = 1
CUBE_Y = 1

START_ITEM_X = 2
START_ITEM_Y = 1

ENHANCE_POINT = (132, 693)
BREAK_POINT = (134, 628)
CLEAR_FIX = (260, 605)

ITEM_ENHANCE_CYCLE = 1
delta = 35

def getMatrix():
	values = []
	for y in range(MAX_V_CELLS):
		values.append([])
		for x in range(MAX_H_CELLS):
			calcX = delta * x + START_POINT[0]
			calcY = delta * y + START_POINT[1]
			values[y].append((calcX, calcY))
	return values


values = getMatrix()

def getClick(x, y):
	x -= 1
	y -= 1
	return {
		var.x: values[y][x][0],
		var.y: values[y][x][1],
		var.delay: 1,
		var.process: 'dclick'
	}

def test():
	print(values)
	iterator = []
	for x in range(len(values)):
		for y in range(len(values[x])):
			iterator.append(getClick(x,y))
	return iterator

def _enchance(x, y):
	return [getClick(x,y),
			getClick(CUBE_X, CUBE_Y),
			click(CLEAR_FIX[0], CLEAR_FIX[1], 0),
			click(ENHANCE_POINT[0], ENHANCE_POINT[1]),
			click(BREAK_POINT[0], BREAK_POINT[1], 1)
	 	]

def enhance():
	current_item_enhance = []
	for i in range(ITEM_ENHANCE_CYCLE):
		for col in range(START_ITEM_Y, MAX_V_CELLS):
			start_line = 1 if (len(current_item_enhance) > 0) else START_ITEM_X
			for line in range(start_line, MAX_H_CELLS):
				# print(col, line)
				current_item_enhance += _enchance(line, col)
	return current_item_enhance


def click(_x, _y, _delay = 2):
	return {
		var.process: 'dclick',
		var.x: _x,
		var.y: _y,
		var.delay: _delay
	}
