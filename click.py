class Click:

    def __init__(self, x, y, process='click', delay=0):
        self.x = x
        self.y = y
        self.process = process
        self.delay = delay


    def instruction(self):
        return {
            'x': self.x,
            'y': self.y,
            'process': self.process,
            'delay': self.delay
        }
