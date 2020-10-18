from sqlalchemy import create_engine, text, MetaData 
from models.cell import Cell, metadata
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
connect_url = 'postgresql+psycopg2://dev:123@localhost:5432/serial_bot_dev'

db = create_engine(connect_url)
# import pdb; pdb.set_trace()

Session = sessionmaker(bind=db)
session = Session()
cell = Cell(2,2,3,4,5)
session.add(cell)
session.commit()

cells = session.query(Cell).all()
# with db.engine.connect() as c:
#     query = text('SELECT * FROM test')
#     tables = c.execute(query)
#     import pdb; pdb.set_trace()
#     print(tables[0])
# print(db)