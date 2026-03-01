import sqlite3

def insertar_desde_input():
# 1. Solicitar datos y convertirlos a los tipos correctos
    i_nombre = input("Ingrese nombre del producto: ")
# Convertimos a float para decimales y a int para números enteros
    try:
        i_precio = float(input("Ingrese precio: "))
        i_stock = int(input("Ingrese stock: "))
    except ValueError:
        print("❌ Error: El precio y el stock deben ser números.")
        return

# 2. Conectar a la base de datos
    conexion = sqlite3.connect("tienda.db")
    cursor = conexion.cursor()

    try:
        cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)", 
                       (i_nombre, i_precio, i_stock))
        # 3. Importante: El commit debe estar dentro del éxito
        conexion.commit()
        print(f"✅ Producto '{i_nombre}' insertado exitosamente.")
    except sqlite3.Error as e:
        print(f"❌ Ocurrió un error en la base de datos: {e}")
    finally:
        # 4. Cerramos siempre la conexión, ocurra o no un error
        conexion.close()
# ¡No olvides llamar a la función para que se ejecute!
insertar_desde_input()