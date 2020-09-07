
from enhancer.grid_identifier import SIZE

class Finder:

    def __init__(self):
        super().__init__()
        self.cols, self.rows = SIZE
        self.matrix = []
        count = 0
        for row in range(self.rows):
            self.matrix.append([])
            for col in range(self.cols):
                self.matrix[row].append(count)
                count += 1
    
    def by_id(self, x, y):
        return self.matrix[y][x]