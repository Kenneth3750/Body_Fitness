
from flask import Flask, render_template, request
import pymysql
from pymysql import Error
from decouple import config

#body_fitness server correct

app = Flask(__name__)

def database_connection():
    try:
        connection = pymysql.connect(host=config('host'),
                                    user=config('user'),
                                    password=config('password'),
                                    db=config('db') )
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


#user register :)
@app.route('/registro.html', methods=['POST'])
def form_data():
    if request.method == 'POST':
        user = request.form.to_dict()
        user_no_empty = {k: v for k, v in user.items() if v}
        user = user_no_empty
    try:
        connection = database_connection()
        if connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO users (nombre, apellido, edad, cedula, correo, celular, direccion) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                values = (user['nombre'], user['apellido'], user['edad'], user['cedula'], user['correo'], user['telefono'], user['direccion'])
                cursor.execute(sql,values )

            connection.commit()
            connection.close()
        else:
            print("Database connection failed")
    except Error as e:
        return 'Error ' + str(e)

    return render_template('registro.html')




if __name__ == '__main__':
    app.run(debug=True, port=10000)