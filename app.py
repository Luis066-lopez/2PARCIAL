from flask import Flask, render_template, redirect, url_for, request, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecreto'

# Inicializar la sesión de productos si no existe
def init_session():
    if 'productos' not in session:
        session['productos'] = []

# Página principal con la lista de productos
@app.route('/')
def index():
    init_session()
    return render_template('index.html', productos=session['productos'])

# Página para agregar un nuevo producto
@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    init_session()
    if request.method == 'POST':
        # Recoger datos del formulario
        nuevo_id = len(session['productos']) + 1
        nombre = request.form['nombre']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        fecha_vencimiento = request.form['fecha_vencimiento']
        categoria = request.form['categoria']

        # Crear el diccionario del producto
        nuevo_producto = {
            'id': nuevo_id,
            'nombre': nombre,
            'cantidad': cantidad,
            'precio': precio,
            'fecha_vencimiento': fecha_vencimiento,
            'categoria': categoria
        }

        #------ Agregar el producto a la sesión
        productos = session['productos']
        session['productos'].append(nuevo_producto)
        session['productos'] = productos
        return redirect(url_for('index'))

    return render_template('nuevo_producto.html')

# Ruta para eliminar un producto
@app.route('/eliminar/<int:id>')
def eliminar_producto(id):
    init_session()
    session['productos'] = [prod for prod in session['productos'] if prod['id'] != id]
    return redirect(url_for('index'))

# Ruta para editar un producto
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    init_session()
    producto = next((prod for prod in session['productos'] if prod['id'] == id), None)
    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = int(request.form['cantidad'])
        producto['precio'] = float(request.form['precio'])
        producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
        producto['categoria'] = request.form['categoria']
        session.modified = True
        return redirect(url_for('index'))
    
    return render_template('editar_producto.html', producto=producto)

if __name__ == '__main__':
    app.run(debug=True)
