# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from models import db, User  # Importa db e User da models.py
from utilis import get_people_in_space

# Crea l'app Flask
app = Flask(__name__)

# Configura la chiave segreta e il database
app.secret_key = 'key_sessione_user'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Inizializza Bcrypt per la gestione delle password
bcrypt = Bcrypt(app)

# Inizializza l'istanza di SQLAlchemy con l'app Flask
db.init_app(app)  # usa init_app invece di passare db all'inizializzazione diretta

# Inizializza LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Crea le tabelle del database se non esistono già (nel contesto dell'app)
with app.app_context():
    db.create_all()  # Crea le tabelle se non esistono

# Funzione per caricare l'utente
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error="Questo username è già in uso.")
        pw_hash = bcrypt.generate_password_hash(password, 10)
        new_user = User(username=username, password=pw_hash)
        db.session.add(new_user)
        db.session.commit()
        if new_user:
            login_user(new_user)
            return redirect(url_for('home'))
    return render_template('register.html', error=None)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        return render_template('login.html', error="Credenziali non valide.")
    return render_template('login.html', error=None)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    people_in_space = get_people_in_space()
    return render_template('home.html', username=current_user.username, people_in_space=people_in_space)

if __name__ == '__main__':
    app.run(debug=True)
