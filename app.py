from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required,current_user
from flask_bcrypt import Bcrypt
from models import db,User
from flask import session
app = Flask(__name__)
app.secret_key = 'key_sessione_user' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
bcrypt = Bcrypt(app)


db.init_app(app)
login_manager = LoginManager() 
login_manager.init_app(app) 
login_manager.login_view = 'login'
@login_manager.user_loader


def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        #Prendere i dati dal database
        username = request.form['username'] 
        password = request.form['password']
        password_hash = bcrypt.generate_password_hash(password)
        if User.query.filter_by(username=username).first():
            return render_template('Login.html', error="Questo username è già in uso.")
        new_user = User(username=username, password=password_hash)
        db.session.add(new_user)
        db.session.commit()
    
        return redirect(url_for('home'))
    return render_template('login.html', error=None)

#Login

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #prende dati dal form
        username = request.form['username'] 
        password = request.form['password']
        #cerca user su db
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        return render_template('Login.html', error="Credenziali non valide.") 
    return render_template('Login.html', error=None)

#Home

@app.route('/home')
@login_required
def home():

    return render_template('index.html', username = current_user.username)

if __name__ == '__main__': 
    
    app.run(debug=True)
