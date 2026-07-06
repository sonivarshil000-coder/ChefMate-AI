from flask import Flask, render_template, request, redirect, url_for , session
import sqlite3

app = Flask(__name__)

app.secret_key = "chefmate_secret_key"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("chefmate.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            session["user"] = user[1]

            return redirect(url_for("dashboard"))

        else:

            return "Invalid Email or Password"

    return render_template("login.html")
@app.route("/dashboard")
def dashboard():

    if "user" not in session:

        return redirect(url_for("login"))

    return render_template("dashboard.html")

@app.route("/signup")
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("chefmate.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (name, email, password)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("signup.html")
@app.route("/logout")
def logout():

    session.pop("user",None)

    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)