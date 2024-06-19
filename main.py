
from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
from flask_apscheduler import APScheduler
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
import pymysql
from pymysql import Error, MySQLError
from decouple import config
from datetime import datetime, timedelta, date
from functions import plan_info
from colorama import Fore, Style
import os


#body_fitness server 

app = Flask(__name__)
mail = Mail()
# flask_mail for gmail config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME']="bodyfitness12478@gmail.com"
app.config['MAIL_PASSWORD']=
mail.init_app(app)


#  APScheduler config
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

def database_connection():
    try:
        connection = pymysql.connect(host=config('host'),
                                    user=config('user'),
                                    password=config('password'),
                                    db=config('db'),
                                    charset='utf8mb4')
        return connection
    except MySQLError as e:
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
@app.route('/ingreso.html')
def ingreso():
    return render_template('ingreso.html')

@app.route('/ingreso.html', methods=['POST'])
def login_user():
    if request.method == 'POST':
        data = request.form.to_dict()
        form_id = data['form_id']
        if form_id == 'form4':
            user_dni = data['id'].replace(" ", "")
            try:
                connection = database_connection()
                if connection:
                    with connection.cursor() as cursor:
                        cursor.execute("SET NAMES utf8mb4;")
                        cursor.execute("SET CHARACTER SET utf8mb4;")
                        cursor.execute("SET character_set_connection=utf8mb4;")
                        sql = "SELECT users.nombre, users.apellido, user_plans.frequency, user_plans.end_plan_date, user_plans.user_id, user_plans.last_entry FROM users INNER JOIN user_plans on users.id = user_plans.user_id WHERE cedula = (%s) order by end_plan_date desc limit 1"
                        values = (user_dni)
                        cursor.execute(sql, values)
                        result = cursor.fetchall()
                        data = result
                        user_id = result[0][4]
                        frequency = result[0][2]
                        end_date = result[0][3]
                        last_entry = result[0][5]
                        last_entry = last_entry.strftime("%Y-%m-%d")
                        if last_entry != datetime.now().strftime("%Y-%m-%d"):
                            if frequency:
                                sql = "UPDATE user_plans SET frequency = frequency - 1 WHERE user_id = (%s) and end_plan_date = (%s)"
                                values = (user_id, end_date) 
                                cursor.execute(sql,values)
                                connection.commit()
                            else:
                                current_date = datetime.now()
                                sql = "UPDATE user_plans SET last_entry = (%s) WHERE user_id = (%s) and end_plan_date = (%s)"
                                values = (current_date,user_id, end_date) 
                                cursor.execute(sql,values)
                                connection.commit()
                    connection.close()
                    return jsonify(data), 200
            except Error as e:
                print( 'Error ' + str(e))
                return jsonify({'message': 'Error' + str(e)}), 500


@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/index.html', methods=['POST'])
def login_data():
    if request.method == 'POST':
        data = request.form.to_dict()
        form_id = data['form_id']
        if form_id == 'form3':
            try:
                connection = database_connection()
                if connection:
                    with connection.cursor() as cursor:
                        cursor.execute("SET NAMES utf8mb4;")
                        cursor.execute("SET CHARACTER SET utf8mb4;")
                        cursor.execute("SET character_set_connection=utf8mb4;")
                        sql ="""SELECT users.nombre, users.apellido, users.cedula, user_plans.end_plan_date, user_plans.frequency
                                FROM users
                                INNER JOIN ( select * from user_plans where (user_id, start_plan_date) in (select user_id, max(start_plan_date) from user_plans group by user_id)) as user_plans
                                ON users.id = user_plans.user_id
                                WHERE (
                                    (user_plans.frequency <= 3 AND DATEDIFF(user_plans.end_plan_date, CURDATE()) > 0)
                                    OR (user_plans.frequency IS NULL AND DATEDIFF(user_plans.end_plan_date, CURDATE()) <= 0 and DATEDIFF(user_plans.end_plan_date, CURDATE()) > -30)
                                    OR (user_plans.frequency IS NULL AND DATEDIFF(user_plans.end_plan_date, CURDATE()) <= 3 and DATEDIFF(user_plans.end_plan_date, CURDATE()) > 0)
                                    OR (DATEDIFF(user_plans.end_plan_date, CURDATE()) <= 3 and DATEDIFF(user_plans.end_plan_date, CURDATE()) > 0 AND user_plans.frequency IS NOT NULL)
                                    OR (DATEDIFF(user_plans.end_plan_date, CURDATE()) <= 0 and DATEDIFF(user_plans.end_plan_date, CURDATE()) > -30 AND user_plans.frequency IS NOT NULL)
                                )
                                GROUP BY users.cedula, users.nombre, users.apellido, user_plans.end_plan_date, user_plans.frequency
                                ORDER BY user_plans.end_plan_date DESC;"""
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        connection.close()

                        return jsonify(result), 200
                else:
                    print("Database connection failed")
                    return jsonify({'message': 'Database connection failed'}), 500
            except Error as e:
                print( 'Error ' + str(e))
                return jsonify({'message': 'Error' + str(e)}), 500
            
        elif form_id == 'form4':
            user_dni = data['id']
            try:
                connection = database_connection()
                if connection:
                    with connection.cursor() as cursor:
                        cursor.execute("SET NAMES utf8mb4;")
                        cursor.execute("SET CHARACTER SET utf8mb4;")
                        cursor.execute("SET character_set_connection=utf8mb4;")
                        sql = "SELECT users.nombre, users.apellido, user_plans.frequency, user_plans.end_plan_date, user_plans.user_id, user_plans.last_entry FROM users INNER JOIN user_plans on users.id = user_plans.user_id WHERE cedula = (%s) order by end_plan_date desc limit 1"
                        values = (user_dni)
                        cursor.execute(sql, values)
                        result = cursor.fetchall()
                        data = result
                        user_id = result[0][4]
                        frequency = result[0][2]
                        end_date = result[0][3]
                        last_entry = result[0][5]
                        last_entry = last_entry.strftime("%Y-%m-%d")
                        if last_entry != datetime.now().strftime("%Y-%m-%d"):
                            if frequency:
                                sql = "UPDATE user_plans SET frequency = frequency - 1 WHERE user_id = (%s) and end_plan_date = (%s)"
                                values = (user_id, end_date) 
                                cursor.execute(sql,values)
                                connection.commit()
                            else:
                                current_date = datetime.now()
                                sql = "UPDATE user_plans SET last_entry = (%s) WHERE user_id = (%s) and end_plan_date = (%s)"
                                values = (current_date,user_id, end_date) 
                                cursor.execute(sql,values)
                                connection.commit()
                        else:
                            if frequency in [10, 12, 15]:
                                sql = "UPDATE user_plans SET frequency = frequency - 1 WHERE user_id = (%s) and end_plan_date = (%s)"
                                values = (user_id, end_date) 
                                cursor.execute(sql,values)
                                connection.commit()
                    connection.close()
                    return jsonify(data), 200
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
        end_date, frequency = plan_info(plan, user, get_plan_duration)
        
        current_date = datetime.now()
        current_date = current_date.strftime("%Y-%m-%d")
        pago = user['pago']
        
    try:
        connection = database_connection()
        if connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO users (nombre, apellido, edad, cedula, correo, celular, direccion) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                values = (user['nombre'], user['apellido'], user['edad'], user['cedula'].replace(" ", ""), user['correo'], user['telefono'], user['direccion'])
                cursor.execute(sql,values)
                user_id = cursor.lastrowid
                sql = "INSERT INTO user_plans (user_id, plan_id, start_plan_date, end_plan_date, frequency, payment_day, payment_status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                values = (user_id, plan, current_date, end_date, frequency, datetime.now(), pago) 
                cursor.execute(sql,values)
                
            connection.commit()
            connection.close()
            return jsonify({'message': 'User created successfully', 'plan': plan}), 200
        else:
            print("Database connection failed")
            return jsonify({'message': 'Database connection failed'}), 500
    except Error as e:
        print( 'Error ' + str(e), 500)
        if "Duplicate entry" in str(e) and "for key 'users.cedula'" in str(e):
            return jsonify({'message': 'Error' + str(e)}), 493
        else:
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
                        cursor.execute("SET NAMES utf8mb4;")
                        cursor.execute("SET CHARACTER SET utf8mb4;")
                        cursor.execute("SET character_set_connection=utf8mb4;")
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
            plan = data['plan']
            int_plan = int(plan)
            user_dni = data['id']
            end_date, frequency = plan_info(int_plan, data, get_plan_duration)
            pago = data['pago']
            try:
                connection = database_connection()
                if connection:
                    with connection.cursor() as cursor:
                        sql = "INSERT INTO user_plans (user_id, plan_id, start_plan_date, end_plan_date, frequency, payment_day, payment_status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        if pago == 'pendiente':
                            values = (user_dni, plan, datetime.now(), end_date, frequency, None, pago)
                        else:
                            values = (user_dni, plan, datetime.now(), end_date, frequency, datetime.now(), pago)
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
            #formPay --> Confirm payment for an user
        elif data['form_id'] == 'formPay':
            user_id = data['user']
            row_id = data['row']
            try:
                connection = database_connection()
                if connection:
                    with connection.cursor() as cursor:
                        sql = "UPDATE user_plans SET payment_day = (%s), payment_status = 'pagado' WHERE user_id = (%s) and user_plans.id = (%s)"
                        values = (datetime.now(), user_id, row_id)
                        cursor.execute(sql, values)
                        connection.commit()
                        connection.close()
                        return jsonify({'message': 'Payment confirmed successfully'}), 200
                else:
                    return jsonify({'message': 'Database connection failed'}), 500
            except Error as e:
                return jsonify({'message': 'Error' + str(e)}), 500
            #Add days to active plans
        elif data['form_id'] == 'formSumPlans':
            days_to_sum = data['days']
            days_to_sum = int(days_to_sum)
            try:
                connection = database_connection()
                if connection:
                    with connection.cursor() as cursor:
                        sql= """UPDATE user_plans 
                                SET end_plan_date = DATE_ADD(end_plan_date, INTERVAL (%s) DAY) 
                                WHERE (user_id, start_plan_date) IN (SELECT user_id, MAX(start_plan_date) WHERE DATEDIFF(user_plans.end_plan_date, CURDATE()) > 0 AND (user_plans.frequency IS NULL OR user_plans.frequency > 0) GROUP BY user_id)"""
                        cursor.execute(sql, days_to_sum)
                        connection.commit()
                        connection.close()
                        return jsonify({'message': 'Days added successfully'}), 200

            except Error as e:
                return jsonify({'message': 'Error' + str(e)}), 500

            #default_form --> view active plans
        else:
            try:
                connection = database_connection()
                if connection:
                    with connection.cursor() as cursor:
                        cursor.execute("SET NAMES utf8mb4;")
                        cursor.execute("SET CHARACTER SET utf8mb4;")
                        cursor.execute("SET character_set_connection=utf8mb4;")
                        sql = """SELECT *
                                 FROM users
                                 INNER JOIN (SELECT *
                                             FROM user_plans
                                             WHERE (user_id, start_plan_date) IN (SELECT user_id, MAX(start_plan_date) FROM user_plans GROUP BY user_id)) AS user_plans
                                 ON users.id = user_plans.user_id
                                 WHERE DATEDIFF(user_plans.end_plan_date, CURDATE()) > 0 AND (user_plans.frequency IS NULL OR user_plans.frequency > 0)
                                 ORDER BY CASE WHEN user_plans.payment_status = 'pendiente' THEN 0 ELSE 1 END;"""
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        connection.close()
                        return jsonify(result), 200
            except Error as e:
                print( 'Error ' + str(e))
                return jsonify({'message': 'Error' + str(e)}), 500


def serch_email_users():
    try:
        connection = database_connection()
        if connection:
            with connection.cursor() as cursor:
                cursor.execute("SET NAMES utf8mb4;")
                cursor.execute("SET CHARACTER SET utf8mb4;")
                cursor.execute("SET character_set_connection=utf8mb4;")
                sql ="""SELECT users.nombre, users.apellido, users.cedula, user_plans.end_plan_date, user_plans.frequency, users.correo, user_plans.email_status, user_plans.user_id
                                FROM users
                                INNER JOIN ( select * from user_plans where (user_id, start_plan_date) in (select user_id, max(start_plan_date) from user_plans group by user_id)) as user_plans
                                ON users.id = user_plans.user_id
                                WHERE (
                                    (user_plans.frequency <= 3 AND DATEDIFF(user_plans.end_plan_date, CURDATE()) > 0)
                                    OR (user_plans.frequency IS NULL AND DATEDIFF(user_plans.end_plan_date, CURDATE()) <= 0 and DATEDIFF(user_plans.end_plan_date, CURDATE()) >= -4)
                                    OR (user_plans.frequency IS NULL AND DATEDIFF(user_plans.end_plan_date, CURDATE()) <= 3 and DATEDIFF(user_plans.end_plan_date, CURDATE()) > 0)
                                    OR (DATEDIFF(user_plans.end_plan_date, CURDATE()) <= 3 and DATEDIFF(user_plans.end_plan_date, CURDATE()) > 0 AND user_plans.frequency IS NOT NULL)
                                    OR (DATEDIFF(user_plans.end_plan_date, CURDATE()) <= 0 and DATEDIFF(user_plans.end_plan_date, CURDATE()) >= -4 AND user_plans.frequency IS NOT NULL)
                                )
                                GROUP BY users.cedula, users.nombre, users.apellido, user_plans.end_plan_date, user_plans.frequency, users.correo, user_plans.email_status, user_plans.user_id
                                ORDER BY user_plans.end_plan_date DESC;"""
                cursor.execute(sql)
                result = cursor.fetchall()
                connection.close()
                return result
        else:
            print("Database connection failed")
            return jsonify({'message': 'Database connection failed'}), 500
    except Error as e:
        print( 'Error ' + str(e))
        return jsonify({'message': 'Error' + str(e)}), 500
    

def update_email_status(user_id, end_date):
    try:
        connection = database_connection()
        if connection:
            with connection.cursor() as cursor:
                sql = "UPDATE user_plans SET email_status = email_status + 1 WHERE user_id = (%s) and end_plan_date = (%s)"
                values = (user_id, end_date) 
                cursor.execute(sql,values)
                connection.commit()
                connection.close()
                return jsonify({'message': 'User updated successfully'}), 200
        else:
            print("Database connection failed")
            return jsonify({'message': 'Database connection failed'}), 500
    except Error as e:
        print( 'Error ' + str(e))
        return jsonify({'message': 'Error' + str(e)}), 500


@scheduler.task('interval', id='send_email', minutes=50)
def send_all_emails():
    with app.app_context():
        users = serch_email_users()
        print(users)
        current_date = date.today() 
        with mail.connect() as conn:
            for user in users:
                last_day = user[3]
                sessions_left = user[4]
                name = f"{user[0]} {user[1]}"
                dest = user[5]
                if sessions_left:
                    sessions_left = sessions_left
                else:
                    sessions_left = 'No aplica'

                if user[6] == 0:
                    subject = 'Vencimiento próximo del plan'
                    content = f"""<p>Estimado(a) {name},<p></br>
    <p>Gimansio Body Fitness le informa que su plan está <b>próximo a vencer</b>. Recuerde que puede renovar su plan en la caja de nuestras instalaciones o a través de nequi al número xxxxxxxx </p> </br>
    <p>La información de su plan es la siguiente:</p></br>
    <p><b>Fecha de vencimiento:</b> {last_day} </p></br>
    <p><b>Sesiones restantes:</b> {sessions_left} (Sólo para planes de 15, 12 y 10 días)</p></br>


    <p>Feliz día,</p></br>

    <p>Att. Gimansio Body Fitness</p>"""
                    
                    update_email_status(user[7], last_day)
                    msg = Message(subject=subject, recipients=[dest],  sender="bodyfitness12478@gmail.com")
                    msg.html = content
                    conn.send(msg)
                    print('-----------------Email sent-----------------')
                elif user[6] == 1 and (last_day < current_date or sessions_left == 0):
                    subject = 'Plan vencido'
                    content = f"""<p>Estimado(a) {name},<p></br>
    <p>Gimansio Body Fitness le informa que su plan ya se encuentra <b>vencido</b>. Recuerde que puede renovar su plan en la caja de nuestras instalaciones o a través de nequi al número xxxxxxxx </p> </br>
    <p>La información de su plan es la siguiente:</p></br>
    <p><b>Fecha de vencimiento:</b> {last_day} </p></br>
    <p><b>Sesiones restantes:</b> {sessions_left} (Sólo para planes de 15, 12 y 10 días)</p></br>


    <p>Feliz día,</p></br>

    <p>Att. Gimansio Body Fitness</p>"""
                    update_email_status(user[7], last_day)
                    msg = Message(subject=subject, recipients=[dest],  sender="bodyfitness12478@gmail.com")
                    msg.html = content                  
                    conn.send(msg)
                    print('-----------------Email sent-----------------')


                else:
                    pass


if __name__ == '__main__':
    app.run(debug=True, port=10000, use_reloader=False)
  


