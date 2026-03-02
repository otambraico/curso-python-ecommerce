from flask import Flask, render_template, request, redirect    
import sqlite3

app = Flask(__name__)

def obtener_datos():
    conexion = sqlite3.connect("tienda.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conexion.close()
    return productos

# Definimos la "Ruta" principal (Home)
@app.route('/')
def home():
    return "<h1>🏠 Inicio de la Tienda</h1><a href='/productos'>Ver Catálogo</a>"

@app.route('/productos')
def lista_productos():
    datos = obtener_datos() # La función que ya tenías de SQLite
    return render_template('index.html', productos=datos)

@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        # 1. Obtener datos del formulario
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])

        # 2. Guardar en la Base de Datos
        conexion = sqlite3.connect("tienda.db")
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)", 
                       (nombre, precio, stock))
        conexion.commit()
        conexion.close()

        # 3. Redirigir al catálogo para ver el cambio
        return redirect('/productos')
    
    # Si es GET, simplemente mostramos el formulario
    return render_template('nuevo_producto.html')

if __name__ == '__main__':
    app.run(debug=True)