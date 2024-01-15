
from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def database_connection():
    try:
        connection = mysql.connector.connect(host='localhost',
                                    user='root',
                                    password='ken_1002161089',
                                    db='body_fitness')
        return connection
    except Error as e:
        print("Database unreachable, " + str(e))
        return None

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/registro.html')
def registro():
    return render_template('registro.html')

@app.route('/registro.html', methods=['POST'])
def form_data():
    if request.method == 'POST':
        user = request.form.to_dict()
        user_no_empty = {k: v for k, v in user.items() if v}
        user = user_no_empty

        connection = database_connection()
        with connection.cursor() as cursor:
            sql = "INSERT INTO users (nombre, apellido, edad, cedula, correo, celular, direccion) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (user['nombre'], user['apellido'], user['edad'], user['cedula'], user['correo'], user['celular'], user['direccion']))

        cursor.close()
        connection.close()

        return render_template('registro.html')

if __name__ == '__main__':
    app.run(debug=True, port=10000)