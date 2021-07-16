import sqlite3

connection = sqlite3.connect('database.sqlite3')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content, autor, lugar) VALUES (?, ?, ?, ?)",
            ('Primer Post', 'Contenido para el primer post', 'Francisco Aviña', 'Celaya')
            )

cur.execute("INSERT INTO posts (title, content, autor, lugar) VALUES (?, ?, ?, ?)",
            ('Segundo Post', 'Contenido para el segundo post', 'Francisco Aviña', 'Celaya')
            )
cur.execute("INSERT INTO posts (title, content, autor, lugar) VALUES (?, ?, ?, ?)",
            ('Tercer Post', 'Contenido para el tercer post', 'Francisco Aviña', 'Celaya')
            )
connection.commit()
connection.close()
