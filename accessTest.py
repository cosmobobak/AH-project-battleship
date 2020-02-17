import pyodbc

driver = 'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
path = r'DBQ=C:\Users\bobakcjs\Documents\GitHub\battleship\\'
database = 'battleshipDB'
connstring = driver + path + database + '.accdb;'
conn = pyodbc.connect(connstring, autocommit=True)
cursor = conn.cursor()

cursor.execute('select * from Table1')

for row in cursor.fetchall():
    print(row)

#cursor.execute("insert into Table1 values(3,'data7','data8','data9')")

cursor.execute('select * from testTable')

for row in cursor.fetchall():
    print(row)
