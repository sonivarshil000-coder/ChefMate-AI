from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import google.generativeai as genai
from config import GEMINI_API_KEY
from parser import format_recipe

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")
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

            return redirect(url_for("ai_home"))

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

@app.route("/question1")
def question1():

    return render_template("question1.html")
@app.route("/ai-home")
def ai_home():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("ai_home.html")
@app.route("/chat", methods=["POST"])
@app.route("/chat", methods=["POST"])
def chat():

    if "user" not in session:
        return redirect(url_for("login"))

    session["recipe_request"] = request.form["message"]

    return render_template(
        "chat.html",
        user_message=session["recipe_request"]
    )
@app.route("/question", methods=["POST"])
@app.route("/question", methods=["POST"])
@app.route("/question", methods=["POST"])
def question():

    people = request.form["people"]

    session["people"] = people

    return render_template("food_type.html")
@app.route("/food-type", methods=["POST"])
def food_type():

    session["food_type"] = request.form["food_type"]

    return render_template("cuisine.html")
@app.route("/cuisine", methods=["POST"])
def cuisine():

    session["cuisine"] = request.form["cuisine"]

    return render_template("budget.html")

@app.route("/budget", methods=["POST"])
def budget():

    session["budget"] = request.form["budget"]

    return render_template("time.html")
@app.route("/time", methods=["POST"])
def time():

    session["time"] = request.form["time"]

    recipe = generate_recipe()

    formatted_recipe = format_recipe(recipe)

    return render_template(
        "recipe.html",
        recipe=formatted_recipe
    )
def generate_recipe():

    prompt = f"""
You are an expert chef.

User Requirements:

Recipe Request: {session['recipe_request']}
Cooking For: {session['people']}
Food Type: {session['food_type']}
Cuisine: {session['cuisine']}
Budget: {session['budget']}
Cooking Time: {session['time']}

IMPORTANT RULES:

- If Food Type is Vegetarian, NEVER include:
  - Egg
  - Chicken
  - Fish
  - Mutton
  - Beef
  - Pork
  - Seafood

- Only use 100% vegetarian ingredients.

Return the answer in this format:

Recipe Name:

Ingredients:

Instructions:

Cooking Time:
"""

    response = model.generate_content(prompt)

    return response.text

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)