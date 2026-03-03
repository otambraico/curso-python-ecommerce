from flask import Flask, render_template, request, redirect, session    
import sqlite3
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

app = Flask(__name__)

def obtener_datos():
    conexion = sqlite3.connect("tienda.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conexion.close()
    return productos

def buscar_usuario(email):
    conexion = sqlite3.connect("tienda.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    usuarios = cursor.fetchone()
    conexion.close()
    return usuarios

# Definimos la "Ruta" principal (Home)
@app.route('/')
def home():
    nombre = session.get('user_nombre')
    return render_template('home.html', nombre=nombre)
    "<br><h1>🏠 Inicio de la Tienda</h1>" \
    "<br><a href='/registro'>Registrar usuarios</a>"

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

@app.route('/borrar/<int:id>')
def borrar_producto(id):
    conexion = sqlite3.connect("tienda.db")
    cursor = conexion.cursor()
    
    # Ejecutamos la sentencia SQL de borrado filtrando por ID
    cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
    
    conexion.commit()
    conexion.close()
    
    # Regresamos al catálogo para ver que ya no está
    return redirect('/productos')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # 1. Obtener datos del formulario
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']

        # ¡Aquí está la magia! Encriptamos la clave antes de guardarla
        pass_encriptado = generate_password_hash(password)

        # 2. Guardar en la Base de Datos
        conexion = sqlite3.connect("tienda.db")
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (?, ?, ?)", 
                       (nombre, email, pass_encriptado))
        conexion.commit()
        conexion.close()

        # 3. Redirigir al catálogo para ver el cambio
        return redirect('/')
        
    # Si es GET, simplemente mostramos el formulario
    return render_template('registro.html')

# Secreto para que las sesiones sean seguras
app.secret_key = 'mi_clave_secreta_muy_dificil'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password_candidata = request.form['password']
        
        usuario = buscar_usuario(email) # Tu función
        
        if usuario and check_password_hash(usuario[3], password_candidata):
            # Si los datos coinciden, guardamos al usuario en la 'sesión'
            session['user_id'] = usuario[0]
            session['user_nombre'] = usuario[1]
            return redirect('/')
        else:
            return render_template('login.html', error="Email o clave incorrectos")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear() # Borra los datos de la sesión
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)