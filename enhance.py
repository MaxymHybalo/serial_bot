from processes.click import Click
from processes.enhance_flow import EnhanceFlow
from processes.combination_flow import CombinationFlow
from utils.configurator import Configurator


class Enhancer:

    def __init__(self, config):
        self.config = Configurator(config)
        self.config = self.config.from_yaml()
        self.combination_cfg = self.config['combination']
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
        return EnhanceFlow(cell, self.config)

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

    def combination(self):
        matrix = self.get_matrix()
        config = self.combination_cfg
        cell0 = config['cell_0']
        cell1 = config['cell_1']
        cells = [matrix[cell0[1] - 1][cell0[0] - 1], matrix[cell1[1] - 1][cell1[0] - 1]]
        return CombinationFlow(cells, self.combination_cfg).get_flow()
