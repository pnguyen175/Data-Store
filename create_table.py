import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute(''' 
          CREATE TABLE company_order
          (id INTEGER PRIMARY KEY ASC,
          company_name VARCHAR(250) NOT NULL,
          material VARCHAR(250) NOT NULL,
          quantity INTEGER NOT NULL,
          price INTEGER NOT NULL,
          status VARCHAR(250) NOT NULL,
          date_created VARCHAR(100) NOT NULL)
          ''')

c.execute('''
          CREATE TABLE company_info
          (id INTEGER PRIMARY KEY ASC,
          company_name VARCHAR(250) NOT NULL,
          order_date VARCHAR(250) NOT NULL,
          order_date_complete VARCHAR(250) NOT NULL,
          date_created VARCHAR(100) NOT NULL)
          ''')

conn.commit()
conn.close()