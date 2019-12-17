import pyodbc

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\Cosmo\Documents\test1.accdb;')
cursor = conn.cursor()
cursor.execute(
'''
INSERT INTO testTable1(ID,Word,Iteration)
VALUES(3,'test',19);
'''
)

cursor.execute(
'''
SELECT * FROM testTable1;
'''
)


for row in cursor.fetchall():
    print(row)
