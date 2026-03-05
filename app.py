from flask import Flask, render_template, request, redirect, session, flash    
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

@app.route('/agregar_carrito/<int:id>')
def agregar_carrito(id):
    # Ahora el carrito será un diccionario: { "id": cantidad }
    if 'carrito' not in session:
        session['carrito'] = {}
    
    # Agregamos el ID del producto
    carrito = session['carrito']

    # Si el producto ya está, sumamos 1. Si no, lo iniciamos en 1.
    id_str = str(id) # Las claves en las sesiones de Flask deben ser strings
    if id_str in carrito:
        carrito[id_str] += 1
    else:
        carrito[id_str] = 1
    
    session['carrito'] = carrito
    session.modified = True

    # --- AQUÍ ESTÁ EL AVISO ---
    # Buscamos el nombre para que el mensaje sea personalizado
    conexion = sqlite3.connect("tienda.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre FROM productos WHERE id = ?", (id,))
    producto = cursor.fetchone()
    conexion.close()

    if producto:
        flash(f"✅ ¡{producto[0]} añadido al carrito!")
    
    return redirect('/productos')

@app.route('/carrito')
def mostrar_carrito():
    carrito = session.get('carrito', {})
    items_completos = []
    total = 0
    
    if carrito:
        conexion = sqlite3.connect("tienda.db")
        cursor = conexion.cursor()
        
        for id_prod, cantidad in carrito.items():
            cursor.execute("SELECT id, nombre, precio FROM productos WHERE id = ?", (id_prod,))
            p = cursor.fetchone()
            if p:
                subtotal = p[2] * cantidad
                total += subtotal
                # Creamos un objeto temporal con los datos + cantidad + subtotal
                items_completos.append({
                    'id': p[0],
                    'nombre': p[1],
                    'precio': p[2],
                    'cantidad': cantidad,
                    'subtotal': subtotal
                })
        conexion.close()

    return render_template('carrito.html', productos=items_completos, total=total) 

@app.route('/eliminar_carrito/<int:id>')
def eliminar_carrito(id):
    if 'carrito' in session:
        carrito = session['carrito']
        id_str = str(id)  # Convertimos a string para asegurar coincidencia
        
        if id_str in carrito:
            if carrito[id_str] > 1:
                # Si hay más de uno, restamos una unidad
                carrito[id_str] -= 1
            else:
                # Si solo queda uno, eliminamos el producto por completo
                del carrito[id_str]
            
            session['carrito'] = carrito
            session.modified = True
            
    return redirect('/carrito')

@app.route('/finalizar_compra')
def finalizar_compra():
    # 1. Seguridad: ¿Está logueado?
    if 'user_id' not in session:
        return redirect('/login')

    ids = session.get('carrito', [])
    if not ids:
        return redirect('/productos')

    conexion = sqlite3.connect("tienda.db")
    cursor = conexion.cursor()

    try:
        # 2. Descontar stock para cada producto en el carrito
        for p_id in ids:
            # Primero verificamos si hay stock
            cursor.execute("SELECT stock, nombre FROM productos WHERE id = ?", (p_id,))
            producto = cursor.fetchone()
            
            if producto and producto[0] > 0:
                cursor.execute("UPDATE productos SET stock = stock - 1 WHERE id = ?", (p_id,))
            else:
                return f"Lo sentimos, no hay stock de {producto[1]}"

        # 3. Guardar cambios y vaciar carrito
        conexion.commit()
        session.pop('carrito') # El carrito ahora está vacío
        return "<h1>✅ ¡Gracias por tu compra!</h1><a href='/'>Volver al inicio</a>"

    except Exception as e:
        return f"Error al procesar la compra: {e}"
    finally:
        conexion.close()

if __name__ == '__main__':
    app.run(debug=True)