from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''   
app.config['MYSQL_DB'] = 'contactos'
mysql = MySQL(app)

app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos')
    data = cur.fetchall()
    return render_template('index.html', contactos = data)
    
    
@app.route('/agregarcontacto', methods=['POST'])
def agrregar_contactos():
    if request.method == 'POST':
        nombre = request.form['nombre']
        print(nombre)
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        correo = request.form['correo']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contactos (nombre, apellido, telefono, correo) VALUES (%s, %s, %s, %s)', (nombre, apellido, telefono, correo))
        if nombre and apellido and telefono and correo != '':
            mysql.connection.commit()
            flash('Contacto agregado correctamente')
        else:
            mysql.connection.close()
            flash('No ha completado los campos') 
        
        return redirect(url_for('index'))

@app.route('/actualizar/<id>')
def actualizar(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos WHERE id= %s',(id,))
    datos = cur.fetchall()
    print(datos)
    return render_template('actualizar-contacto.html',contactos=datos[0])

@app.route('/actualizarcontacto/<id>',methods=['POST'])
def actualizarcontacto(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        correo = request.form['correo']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE contactos SET nombre=%s,apellido=%s,telefono=%s,correo=%s WHERE id = %s', (nombre,apellido,telefono,correo,id))
        mysql.connection.commit()
        flash('Contacto actualizado correctamente')
        return redirect(url_for('index'))
@app.route('/eliminar/<string:id>')
def eliminar(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contactos WHERE id=%s',(id,))
    mysql.connection.commit()
    flash('Contacto eliminado')
    return redirect(url_for('index'))
   
if __name__ == '__main__':
    app.run(debug=True)
