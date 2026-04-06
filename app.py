from flask import Flask, request, redirect, url_for, session, flash, render_template_string
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'change-me-in-production'

# Простая "база данных" в памяти
users = {}

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id, password_hash):
        self.id = id
        self.password_hash = password_hash

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id, users[user_id])
    return None

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email not in users:
            users[email] = generate_password_hash(password)
            flash('Регистрация успешна!')
            return redirect(url_for('login'))
        flash('Пользователь уже существует')
    return render_template_string('''
        <form method="POST">
            Email: <input name="email"><br>
            Пароль: <input name="password" type="password"><br>
            <input type="submit" value="Зарегистрироваться">
        </form>
    ''')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email in users and check_password_hash(users[email], password):
            user = User(email, users[email])
            login_user(user)
            return redirect(url_for('protected'))
        flash('Неверный логин или пароль')
    return render_template_string('''
        <form method="POST">
            Email: <input name="email"><br>
            Пароль: <input name="password" type="password"><br>
            <input type="submit" value="Войти">
        </form>
    ''')

@app.route('/protected')
@login_required
def protected():
    return 'Доступ разрешён! Это защищённая страница.'

@app.route('/change-password', methods=['POST'])
@login_required
def change_password():
    new_password = request.form.get('new_password')
    users[session.get('_user_id')] = generate_password_hash(new_password)
    flash('Пароль изменён')
    return redirect(url_for('protected'))

if __name__ == '__main__':
    app.run(debug=True)