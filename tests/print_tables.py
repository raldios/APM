import sqlite3

tables = ['assets', 'folders']

connection = sqlite3.connect(r'C:\Users\glavi\AppData\Roaming\ADI\adi.db')

for table in tables:
    cursor = connection.execute(f'SELECT * FROM {table}')
    print(table)
    for item in cursor.description:
        print(f'\t{item[0]}')