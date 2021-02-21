from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Вы успешно вошли!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Неверный пароль.', category='error')
        else:
            flash('Пользователя не существует.', category='error')
    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Пользователь с таким электронным адресом уже существует.', category='error')
        elif len(name) < 3:
            flash('Имя должно быть длинее, чем 2 символа.', category='error')
        elif len(password1) < 5:
            flash('Пароль должен быть длинее, чем 4 символа.', category='error')
        elif password1 != password2:
            flash('Пароли не совпадают.', category='error')
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Аккаунт создан!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)