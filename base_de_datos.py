import sqlite3

# 1. Conectar (si no existe, se crea el archivo 'tienda.db')
conexion = sqlite3.connect("tienda.db")
cursor = conexion.cursor()

# 2. Crear la tabla de productos (solo la primera vez)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL,
        stock INTEGER NOT NULL
    )
''')

# 3. Guardar cambios y cerrar
conexion.commit()
conexion.close()

print("✅ Base de datos y tabla creadas con éxito.")