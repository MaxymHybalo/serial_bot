from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapper

metadata = MetaData()

cell = Table('cells', metadata,
    Column('id', Integer, primary_key=True),
    Column('col', Integer),
    Column('row', Integer),
    Column('x', Integer),
    Column('y', Integer),
    Column('grid_id', Integer))

class Cell(object):
    def __init__(self, col, row, x, y, gid):
        self.col     = col
        self.row     = row
        self.x       = x
        self.y       = y
        self.grid_id = gid

    def __repr__(self):
        return 'Cell({0}, {1}, {2}, {3}, {4}'.format(self.col, self.row, self.x, self.y, self.grid_id)
mapper(Cell, cell)