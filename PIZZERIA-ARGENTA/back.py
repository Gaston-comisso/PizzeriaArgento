from flask import Flask, render_template
from flask_mysqldb import MySQL, MySQLdb

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/registro")
def registro():
    return render_template("register.html")

@app.route("/pedidos")
def pedidos():
    return render_template("pedidos.html")

@app.route("/formulario")
def formulario():
    return render_template("formulario.html")


if __name__=="__main__":
    app.run(debug=True)