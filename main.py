from flask import Flask, render_template, request

import pymysql



app = Flask(__name__)


def database_connection():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='ken_1002161089',
                                 db='body_fitness')
    return connection




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
        print(request.form)
        return render_template('registro.html')




if __name__ == '__main__':
    app.run(debug=True, port=10000)