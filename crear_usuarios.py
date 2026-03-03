import sqlite3

# 1. Conectar (si no existe, se crea el archivo 'tienda.db')
conexion = sqlite3.connect("tienda.db")
cursor = conexion.cursor()

# 2. Crear la tabla de usuarios (solo la primera vez)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

# 3. Guardar cambios y cerrar
conexion.commit()
conexion.close()