from sqlalchemy import create_engine, text, MetaData 
from models.cell import Cell, metadata
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import cv2 
import numpy as np
import pickle
import utils.cv2_utils as u
connect_url = 'postgresql+psycopg2://dev:123@localhost:5432/serial_bot_dev'

db = create_engine(connect_url)
# metadata.bind = db
# metadata.create_all()
image = cv2.imread('db_blob.png')
image = np.array(image)
as_bytes = image.dumps()

Session = sessionmaker(bind=db)
session = Session()
cell = Cell(2,2,3,4, as_bytes, 1)
session.add(cell)
session.commit()

table_row = session.query(Cell).first()
print(table_row.source)
source = table_row.source

image = pickle.loads(source)

# print(size(as_bytes))
# print(pickle.loads(as_bytes))
u.show_image(image)