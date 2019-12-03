import pyodbc

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\Cosmo\Documents\test1.accdb;')
cursor = conn.cursor()
cursor.execute('select * from testTable1')

for row in cursor.fetchall():
    print (row)
