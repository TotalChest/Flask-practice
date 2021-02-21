from flask import Blueprint, render_template, request, flash, redirect, url_for


auth = Blueprint('auth', __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@auth.route("/logout")
def logout():
    return "<h1>LOGOUT</h1>"


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('pasword2')

        if len(name) < 3:
            flash("Имя должно быть длинее, чем 2 символа.", category="error")
        elif len(password1) < 5:
            flash("Пароль должен быть длинее, чем 4 символа.", category="error")
        elif password1 != password2:
            flash("Пароли не совпадают.", category="error")
        else:
            flash("Аккаунт создан!", category="success")

    return render_template("signup.html")