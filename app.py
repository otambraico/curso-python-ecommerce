from flask import Flask, render_template    
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

if __name__ == '__main__':
    app.run(debug=True)