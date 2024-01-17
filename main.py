
from flask import Flask, render_template, request, jsonify
import pymysql
from pymysql import Error
from decouple import config
from datetime import datetime, timedelta

#body_fitness server 

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

def get_plan_duration(id_plan):
    try:
        connection = database_connection()
        if connection:
            with connection.cursor() as cursor:
                sql = "SELECT duration FROM plans where id = (%s)"
                cursor.execute(sql, id_plan)
                result = cursor.fetchall()
                connection.close()
                return result
           
        else:
            print("Database connection failed")
            return None
    except Error as e:
        print( 'Error ' + str(e))
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
        plan = user['plan']
        plan = int(plan)

        month_plans = [1, 2, 3, 4]
        day_plans = [5, 6, 7]
        if plan in month_plans:
            plan_duration= get_plan_duration(plan)
            plan_duration = plan_duration[0][0]
            plan_duration = int(plan_duration)

            end_date = datetime.now() + timedelta(days=30*plan_duration) 
            end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
            frequency = None
        elif plan in day_plans:
            plan_duration= get_plan_duration(plan)
            plan_duration = plan_duration[0][0]
            plan_duration = int(plan_duration)
            end_date = datetime.now() + timedelta(days=plan_duration)
            end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
            if plan == 5:
                frequency = 10
            elif plan == 6:
                frequency = 12
            else:
                frequency = 15
        else:
            plan_duration = user['duracion']
            plan_duration = int(plan_duration)
            end_date = datetime.now() + timedelta(days = 30*plan_duration)
            end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
            frequency = None
        print(end_date)
        
    try:
        connection = database_connection()
        if connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO users (nombre, apellido, edad, cedula, correo, celular, direccion) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                values = (user['nombre'], user['apellido'], user['edad'], user['cedula'], user['correo'], user['telefono'], user['direccion'])
                cursor.execute(sql,values)
                user_id = cursor.lastrowid
                sql = "INSERT INTO user_plans (user_id, plan_id, end_plan_date, frequency, payment_day) VALUES (%s, %s, %s, %s, %s)"
                values = (user_id, plan, end_date, frequency, datetime.now()) 
                cursor.execute(sql,values)
                
            connection.commit()
            connection.close()
            return jsonify({'message': 'User created successfully', 'plan': plan}), 200
        else:
            print("Database connection failed")
            return jsonify({'message': 'Database connection failed'}), 500
    except Error as e:
        print( 'Error ' + str(e), 500)
        return jsonify({'message': 'Error' + str(e)}), 500





if __name__ == '__main__':
    app.run(debug=True, port=10000)
