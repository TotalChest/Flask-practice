from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'pet'
app.permanent_session_lifetime = timedelta(minutes=10)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    password = db.Column(db.String(64))
    email = db.Column(db.String(64))

    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email


messages = ["Hello!", "Hi", "How r u?", "Fine.."]


@app.route("/")
def home():
   return render_template("index.html")

@app.route("/chat")
def chat():
    return render_template("chat.html", messages=messages)

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user_name = request.form["un"]
        found_user = users.query.filter_by(name=user_name).first()
        if found_user:
            if found_user.password == request.form["pw"]:
                session.permanent = True
                session["user"] = user_name
                session["email"] = found_user.email
                flash(f"You have been logged in, {session['user']}", "info")
                return redirect(url_for("user"))
            else:
                flash(f"Wrong login or password", "info")
                return render_template("login.html")
        else:
            session["user"] = user_name
            usr = users(user_name, request.form["pw"], "")
            db.session.add(usr)
            db.session.commit()
            flash(f"You have been logged in, {session['user']}", "info")
            return redirect(url_for("user"))
    else:
        return render_template("login.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/allusers")
def allusers():
    return render_template("allusers.html", users=users.query.all())

@app.route("/user", methods=["GET", "POST"])
def user():
    email = None
    if "user" in session:
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=session["user"]).first()
            found_user.email = email
            db.session.commit()
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", user=session["user"], email=email)
    else:
        flash(f"You are not log in", "info")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        flash(f"You have been logged out, {session['user']}", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    db.create_all()
    app.run(host="localhost", port=8080, debug=True)
