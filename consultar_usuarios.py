import sqlite3

def consultar_usuarios():
    # 1. Conexión a la base de datos
    conexion = sqlite3.connect("tienda.db")
    cursor = conexion.cursor()

    try:
        # 2. Ejecutar la consulta SELECT
        # Seleccionamos las columnas específicas que queremos ver
        cursor.execute("SELECT id, nombre, email, password FROM usuarios")
        
        # 3. Obtener todos los resultados (fetchall devuelve una lista de tuplas)
        usuarios = cursor.fetchall()

        print(f"{'ID':<5} | {'NOMBRE':<15} | {'EMAIL':<20} | {'PASSWORD ENCRIPTADA'}")
        print("-" * 80)

        for user in usuarios:
            # user[0] es ID, user[1] es Nombre, etc.
            print(f"{user[0]:<5} | {user[1]:<15} | {user[2]:<20} | {user[3][:20]}...") 
            # Nota: Usamos [:20] para no llenar la pantalla con el hash completo

    except sqlite3.Error as e:
        print(f"Error al consultar: {e}")
    
    finally:
        # 4. Cerrar conexión
        conexion.close()

if __name__ == "__main__":
    consultar_usuarios()