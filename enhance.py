from processes.click import Click
from processes.enhance_flow import EnhanceFlow

CUBE_X = 1
CUBE_Y = 5

START_ITEM_X = 2
START_ITEM_Y = 5

# now consistent  with grid
MAX_H_CELLS = 9
MAX_V_CELLS = 11

ITEM_ENHANCE_CYCLE = 4

START_POINT = (85, 85)
ENHANCE_POINT = (132, 693)
BREAK_POINT = (134, 628)
CLEAR_FIX = (260, 605)

DELTA = 35

# frequently used clicks
clear_fix = Click(CLEAR_FIX[0], CLEAR_FIX[1], process='dclick', delay=0)
enhance_point = Click(ENHANCE_POINT[0], ENHANCE_POINT[1], process='dclick', delay=2)
break_point = Click(BREAK_POINT[0], BREAK_POINT[1], process='dclick', delay=0)
comb_ok = Click(585, 440)

# enhancement _enhance_move for enhancing, _open_move - for open items
def enhancement():
    current_item_enhance = []
    for line in range(START_ITEM_Y, MAX_V_CELLS + 1):
        start_line = 1 if (len(current_item_enhance) > 0) else START_ITEM_X
        for col in range(start_line, MAX_H_CELLS + 1):
            current_item_enhance += _enhance_move(col, line).get_flow()
    return current_item_enhance


def combination():
    return _combination_move((1, 11), (2, 11)).get_flow()


def enhance(flow):
    loops = []
    for i in range(ITEM_ENHANCE_CYCLE):
        loops += flow()
    return loops


def get_matrix():
    values = []
    for y in range(MAX_V_CELLS):
        values.append([])
        for x in range(MAX_H_CELLS):
            calcX = DELTA * x + START_POINT[0]
            calcY = DELTA * y + START_POINT[1]
            values[y].append((calcX, calcY))
    return values


def _get_click(_x, _y):
    values = get_matrix()
    _x -= 1
    _y -= 1
    return Click(values[_y][_x][0], values[_y][_x][1], process='dclick', delay=0)


def _enhance_move(x, y):
    return EnhanceFlow(
        _get_click(x, y),
        _get_click(CUBE_X, CUBE_Y),
        clear_fix,
        enhance_point,
        break_point
    )

def _open_move(x,y):
    return EnhanceFlow(
        _get_click(x, y),
        _get_click(CUBE_X, CUBE_Y),
        clear_fix,
        enhance_point,
        break_point
    )

# x & y is tuples of two combination el
def _combination_move(x, y):
    return EnhanceFlow(
        _get_click(x[0], x[1]),
        __select_count(2),
        __select_count(8),
        __select_count(0),
        comb_ok,
        _get_click(y[0], y[1]),
        __select_count(7),
        __select_count(0),
        comb_ok,
        enhance_point
    )


def __select_count(digit):
    point = __combination_digit_grid(digit)
    return Click(point[0], point[1])


def __combination_digit_grid(digit):
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
