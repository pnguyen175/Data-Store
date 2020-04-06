import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()

c.execute('''
          DROP TABLE company_info
          ''')

c.execute('''
          DROP TABLE company_order
          ''')
          
conn.commit()
conn.close()