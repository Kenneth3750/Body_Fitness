from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/registro.html')
def registro():
    return render_template('registro.html')



app.run(debug=True, port=10000)