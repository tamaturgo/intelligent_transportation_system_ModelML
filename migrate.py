import sqlite3

conn = sqlite3.connect('its.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS poligonos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pontos TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS regras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT,
        valor REAL,
        aux_valor REAL,
        criado_em DATE
    )    
''')

cursor.execute('''
               CREATE TABLE IF NOT EXISTS rel_poligonos_regras (
                     poligono_id INTEGER,
                     regra_id INTEGER
                )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        data DATE
    )   
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        data DATE,
        duracao INTEGER
    )
''')
conn.commit()
conn.close()
