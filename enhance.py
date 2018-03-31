from processes.click import Click
from processes.enhance_flow import EnhanceFlow
from utils.configurator import Configurator


class Enhancer:

    def __init__(self, config):
        self.config = Configurator(config)
        self.config = self.config.from_yaml()
        self.config = self.config['enhance']

    # enhancement _enhance_move for enhancing, _open_move - for open items
    def enhancement(self):
        # firstly get enhancement matrix
        matrix = self._slice_matrix_by_config()
        current_item_enhance = []
        for line in matrix:
            for cell in line:
                current_item_enhance += self._enhance_move(cell).get_flow()
        return current_item_enhance

    def _slice_matrix_by_config(self):
        scope = self.config['scope']
        max_x = self.config['max']['horizontal']
        first_line = scope['start']
        last_line = scope['end']
        matrix = self.get_matrix()
        result = []
        first_line_points = matrix[first_line[1] - 1][first_line[0] - 1: max_x]  # get first line
        result.append(first_line_points)
        body = matrix[first_line[1]:last_line[1] - 1]
        for b in body:
            result.append(b)
        last_line_points = matrix[last_line[1] - 1][:last_line[0]]
        result.append(last_line_points)
        return result

    def _enhance_move(self, cell):
<<<<<<< HEAD
        cube_click = self._get_click(self.config['cube']['x'], self.config['cube']['y'])
        return EnhanceFlow(
            Click(cell[0], cell[1], process='dclick'),
            cube_click,
            self.clear_fix,
            self.enhance_point,
            self.break_point
        )
=======
        return EnhanceFlow(cell, self.config)
>>>>>>> f198e75894716115fb04f542c0b69d19788adbda

    def enhance(self, flow):
        loops = []
        for i in range(self.config['cycles']):
            loops += flow()
        return loops

    def _get_click(self, _x, _y):
        values = self.get_matrix()
        _x -= 1
        _y -= 1
        return Click(values[_y][_x][0], values[_y][_x][1], process='dclick')

    def get_matrix(self):
        values = []
        for y in range(self.config['max']['vertical']):
            values.append([])
            for x in range(self.config['max']['horizontal']):
                delta = self.config['delta']
                start_point = self.config['points']['start']
                calc_x = delta * x + start_point[0]
                calc_y = delta * y + start_point[1]
                values[y].append((calc_x, calc_y))
        return values
#
# def combination():
#     return _combination_move((1, 11), (2, 11)).get_flow()
#


#
# # x & y is tuples of two combination el
# def _combination_move(x, y):
#     return EnhanceFlow(
#         _get_click(x[0], x[1]),
#         __select_count(2),
#         __select_count(8),
#         __select_count(0),
#         comb_ok,
#         _get_click(y[0], y[1]),
#         __select_count(7),
#         __select_count(0),
#         comb_ok,
#         enhance_point
#     )
#
#
# def __select_count(digit):
#     point = __combination_digit_grid(digit)
#     return Click(point[0], point[1])
#
#
# def __combination_digit_grid(digit):
#     one = [638, 422]
#     delta = 20
#     if digit > 3:
#         one[1] -= delta
#     if digit > 6:
#         one[1] -= delta
#     if digit in [8, 5, 2]:
#         one[0] += delta
#     if digit in [9, 6, 3]:
#         one[0] += delta
#     if digit == 0:
#         one = [658, 442]
#     return one
