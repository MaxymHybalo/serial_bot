from sqlalchemy import create_engine, text 

connect_url = 'postgresql+psycopg2://dev:123@localhost:5432/serial_bot_dev'

db = create_engine(connect_url)
with db.engine.connect() as c:
    query = text('SELECT version()')
    tables = c.execute(query)

    print(tables)
# print(db)