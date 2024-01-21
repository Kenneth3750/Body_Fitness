
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
def plan_info(plan, user):
    month_plans = [1, 2, 3, 4]
    day_plans = [5, 6, 7]
    if plan in month_plans:
        plan_duration= get_plan_duration(plan)
        plan_duration = plan_duration[0][0]
        plan_duration = int(plan_duration)

        end_date = datetime.now() + timedelta(days=30*plan_duration) 
        end_date = end_date.strftime("%Y-%m-%d")
        frequency = None
    elif plan in day_plans:
        plan_duration= get_plan_duration(plan)
        plan_duration = plan_duration[0][0]
        plan_duration = int(plan_duration)
        end_date = datetime.now() + timedelta(days=plan_duration)
        end_date = end_date.strftime("%Y-%m-%d")
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
        end_date = end_date.strftime("%Y-%m-%d")
        frequency = None
    return end_date, frequency



@app.route('/')
def login():
    return render_template('login.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/index.html', methods=['POST'])
def login_data():
    if request.method == 'POST':
        data = request.form.to_dict()
        form_id = data['form_id']
        print(form_id)
        if form_id == 'form3':
            try:
                connection = database_connection()
                if connection:
                    with connection.cursor() as cursor:
                        sql = """SELECT users.nombre, users.apellido, users.cedula, user_plans.end_plan_date, user_plans.frequency
                                FROM users
                                INNER JOIN user_plans ON users.id = user_plans.user_id
                                WHERE (
                                    (user_plans.frequency <= 3 AND DATEDIFF(user_plans.end_plan_date, CURDATE()) > 0)
                                    OR (user_plans.frequency IS NULL AND ABS(DATEDIFF(user_plans.end_plan_date, CURDATE())) <= 3)
                                    OR (ABS(DATEDIFF(user_plans.end_plan_date, CURDATE())) <= 3 AND user_plans.frequency IS NOT NULL)
                                )
                                GROUP BY users.cedula, users.nombre, users.apellido, user_plans.end_plan_date, user_plans.frequency
                                ORDER BY user_plans.end_plan_date DESC;"""
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        connection.close()
                        print(result)
                        return jsonify(result), 200
                else:
                    print("Database connection failed")
                    return jsonify({'message': 'Database connection failed'}), 500
            except Error as e:
                print( 'Error ' + str(e))
                return jsonify({'message': 'Error' + str(e)}), 500
            
        else:
            user = request.form.to_dict()
            id = user['id']
            try:
                connection = database_connection()
                if connection:
                    with connection.cursor() as cursor:
                        sql = "SELECT users.id FROM users WHERE users.cedula = (%s)"
                        cursor.execute(sql, id)
                        result = cursor.fetchall()
                        print(result[0][0])
                        connection.close()
                        return jsonify(result), 200
                else:
                    print("Database connection failed")
                    return jsonify({'message': 'Database connection failed'}), 500
            except Error as e:
                print( 'Error ' + str(e))
                return jsonify({'message': 'Error' + str(e)}), 500
        

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
        end_date, frequency = plan_info(plan, user)
        
        current_date = datetime.now()
        current_date = current_date.strftime("%Y-%m-%d")
        
    try:
        connection = database_connection()
        if connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO users (nombre, apellido, edad, cedula, correo, celular, direccion) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                values = (user['nombre'], user['apellido'], user['edad'], user['cedula'], user['correo'], user['telefono'], user['direccion'])
                cursor.execute(sql,values)
                user_id = cursor.lastrowid
                sql = "INSERT INTO user_plans (user_id, plan_id, start_plan_date, end_plan_date, frequency, payment_day) VALUES (%s, %s, %s, %s, %s, %s)"
                values = (user_id, plan, current_date, end_date, frequency, datetime.now()) 
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
    


@app.route('/usuarios.html')
def usuario():
    return render_template('usuarios.html')

#view and renew an user
@app.route('/usuarios.html', methods=['POST', 'GET'])
def search_user():
    if request.method == 'POST':
        data = request.form.to_dict()
        #form1 --> view user
        if data['form_id'] == 'form1':
            user_dni = data['id']
            try:
                connection = database_connection()
                if connection:
                    with connection.cursor() as cursor:
                        sql = "SELECT * FROM users INNER JOIN user_plans on users.id = user_plans.user_id WHERE cedula = (%s) order by end_plan_date desc limit 6"
                        cursor.execute(sql, user_dni)
                        result = cursor.fetchall()
                        connection.close()
                        return jsonify(result), 200
                else:
                    print("Database connection failed")
                    return jsonify({'message': 'Database connection failed'}), 500
            except Error as e:
                print( 'Error ' + str(e))
                return jsonify({'message': 'Error' + str(e)}), 500
        #form2 --> renew user
        elif data['form_id'] == 'form2':
            print(data)
            plan = data['plan']
            int_plan = int(plan)
            user_dni = data['id']
            end_date, frequency = plan_info(int_plan, data)
            try:
                connection = database_connection()
                if connection:
                    with connection.cursor() as cursor:
                        sql = "INSERT INTO user_plans (user_id, plan_id, start_plan_date, end_plan_date, frequency, payment_day) VALUES (%s, %s, %s, %s, %s, %s)"
                        values = (user_dni, plan, datetime.now(), end_date, frequency, None)
                        cursor.execute(sql, values)
                        connection.commit()
                        connection.close()
                        return jsonify({'message': 'User updated successfully'}), 200
                else:
                    print("Database connection failed")
                    return jsonify({'message': 'Database connection failed'}), 500
            except Error as e:
                print( 'Error ' + str(e))
                return jsonify({'message': 'Error' + str(e)}), 500
        


        






if __name__ == '__main__':
    app.run(debug=True, port=10000)
