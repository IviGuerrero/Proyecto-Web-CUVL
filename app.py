import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

@app.route('/')
def home():
    print(f"Template folder: {app.template_folder}")
    return render_template('home.html')

@app.route('/investing')
def investing():
    return render_template('investing.html')

@app.route('/balanz')
def balanz():
    return render_template('balanz.html')

@app.route('/iol')
def iol():
    return render_template('iol.html')

@app.route('/analisis')
def analisis():
    return render_template('analisis.html')


@app.route('/search', methods=['GET'])
def search():
    cedears = request.args.get('cedears')
    print(f"Search cedears: {cedears}")
    results = search_investments(cedears)
    print(f"Search results: {results}")
    return render_template('search_results.html', cedears=cedears, results=results)

def search_investments(cedears):
    if cedears:
        cedears = cedears.lower()
    else:
        return {}

    data = {
        'AAPL': 'Apple Inc.',
        'TSLA': 'Tesla Motors',
    }
    results = {key: value for key, value in data.items() if cedears in value.lower()}
    return results


@app.route('/trading', methods=['GET'])
def trading():
    return render_template('trading.html')

@app.route('/grafico')
def grafico():
    return render_template('grafico.html')

wallet_data = {
    'AAPL': {'nombre': 'Apple Inc.', 'cantidad': 10, 'precio': 18500},
    'TSLA': {'nombre': 'Tesla Motors.', 'cantidad': 5, 'precio': 16600}
}

@app.route('/wallet')
def wallet():
    total_value = sum(item['cantidad'] * item['precio'] for item in wallet_data.values())
    return render_template('billetera.html', wallet_data=wallet_data, total_value=total_value)

app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return User(id=user[0], username=user[1], password=user[2])
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()
        if user and check_password_hash(user[2], password):
            user_obj = User(id=user[0], username=user[1], password=user[2])
            login_user(user_obj)
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Nombre de usuario o contraseña incorrectos', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash('Usuario registrado exitosamente', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('El usuario ya existe', 'danger')
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada exitosamente', 'info')
    return redirect(url_for('login'))


def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("Base de datos inicializada correctamente")

@app.route('/dashboard')  
def dashboard():
    return render_template('dashboard.html')  

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
