from processes.click import Click


class EnhanceFlow:

    def __init__(self, cell, config, *args):
        self.cell = cell
        self.config = config
        self.flow = args
        self.__set_points(config['points'])

    def submit_enhance(self):
        return [
            self.clear_fix,
            self.enhance_point,
            self.break_point
        ]

    def __set_points(self, points):
        self.clear_fix = Click(points['clear'][0], points['clear'][1], process='dclick')
        self.enhance_point = Click(points['enhance'][0], points['enhance'][1], process='dclick', delay=2)
        self.break_point = Click(points['break'][0], points['break'][1], process='dclick')
        self.comb_ok = Click(points['combination'][0], points['combination'][1])

    def get_flow(self):
        cube = Click(self.cell[0], self.cell[1])
        item = Click(self.config['cube']['x'], self.config['cube']['y']),

        return [item, cube] + self.submit_enhance()
