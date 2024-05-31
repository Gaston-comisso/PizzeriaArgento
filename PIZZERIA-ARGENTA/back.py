from flask import Flask, render_template, request, session
from flask_mysqldb import MySQL, MySQLdb
from flask_session import Session
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Cargar variables de entorno desde un archivo .env
load_dotenv()

#Conexion a BDD
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST') 
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB') 
mysql = MySQL(app)


#rutas
@app.route("/login")
def home():
    return render_template("index.html")

@app.route("/")
def cliente():
    return render_template("cliente.html")

@app.route("/admin")
def admin():
    cur = mysql.connection.cursor() 
    cur.execute('SELECT * FROM formularios')
    forms = cur.fetchall()

    cur.close()
    return render_template("paginaadmin.html", forms = forms)

#ruta para recibir los datos del login
@app.route('/procesar_login', methods=['POST']) 
def login():
    if  request.method == 'POST':
        email = request.form['email']
        password = request.form['Password']
        cur = mysql.connection.cursor()    
        cur.execute('SELECT nombre, contraseña FROM admins WHERE email = %s AND contraseña = %s', (email, password))

        logueo =cur.fetchone()
    if logueo:
            session['logeado'] = True
            
            return render_template('paginaadmin.html')
    else:
            return render_template('index.html', error='Usuario o contraseña incorrectos')

#ruta para recibir el formulario
@app.route('/cargarFormulario', methods=['POST'])
def cargarFormulario(): #query
    if  request.method == 'POST':
        telefono = request.form['telefono']
        nombre = request.form['nombre']
        email= request.form['email']
        barrio= request.form['barrio']
        direccion= request.form['direccion']
        costo= 10600 #lo dejo con un valor fijo ya que en el html 'cliente' el valor es fijo
        comentario= request.form['comentario']  
        
        cur = mysql.connection.cursor()    
        
        cur.execute('''INSERT INTO formularios (telefono, nombre, email, barrio, direccion,costo,comentario)
                    VALUES (%s, %s, %s, %s,%s,%s,%s)'''
                    , (telefono,nombre,email,barrio,direccion,costo,comentario))
        
        mysql.connection.commit()
        
        
        return render_template('cliente.html', mensaje= "¡Formulario enviado con éxito! ") #lo dirijimos a cliente

if __name__=="__main__":
    app.secret_key='llave secreta'
    app.run(debug=True)