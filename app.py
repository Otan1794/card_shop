import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from api import searchPrice, searchCard, login_required


# Configure application
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///final-project.db")
card_name = ""

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    if(session):
        cart_content = db.execute("SELECT * FROM cart WHERE user_id = ?", session["user_id"])
        total_qty = sum(row["qty"] for row in cart_content)
        return render_template("index.html", cart_content=cart_content, total_qty=total_qty)
    else:
        return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
def price():
    if request.method == "POST":
        card = request.form.get("card")
        card_dataPrice = searchPrice(card)
        card_dataInfo = searchCard(card)
        global card_name
        card_name = card
        if card_dataPrice == -1 or card_dataInfo == -1:
            if(session):
                cart_content = db.execute("SELECT * FROM cart WHERE user_id = ?", session["user_id"])
                total_qty = sum(row["qty"] for row in cart_content)
                return render_template("index.html", cart_content=cart_content, total_qty=total_qty) #error handle
            else:
                return render_template("index.html")
        else:
            card_dataPrice = sorted(card_dataPrice, key=lambda d: d["set"])
            if(session):
                cart_content = db.execute("SELECT * FROM cart WHERE user_id = ?", session["user_id"])
                total_qty = sum(row["qty"] for row in cart_content)
                return render_template("search.html", card_dataPrice=card_dataPrice, card_img=card_dataInfo["img_url"], card_name=card_dataInfo["name"],
                                    card_type=card_dataInfo["type"], card_race=card_dataInfo["race"], cart_content=cart_content, total_qty=total_qty)
            else:
                return render_template("search.html", card_dataPrice=card_dataPrice, card_img=card_dataInfo["img_url"], card_name=card_dataInfo["name"],
                                    card_type=card_dataInfo["type"], card_race=card_dataInfo["race"])
    else:
        return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("user"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("index.html") #error handle

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        cart_content = db.execute("SELECT * FROM cart WHERE user_id = ?", session["user_id"])
        total_qty = sum(row["qty"] for row in cart_content)
        return render_template("index.html", cart_content=cart_content, total_qty=total_qty)
    else:
        return render_template("index.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("user")
        email = request.form.get("email")
        password = request.form.get("pass")
        repass = request.form.get("repass")
        users = db.execute("SELECT username FROM users;")
        emails = db.execute("SELECT email FROM users;")
        user_values_db = [dictionary["username"] for dictionary in users]
        email_values_db = [dictionary["email"] for dictionary in emails]
        if password != repass:
            return render_template("index.html") #error handle
        elif username in user_values_db or email in email_values_db:
            return render_template("index.html") #error handle
        else:
            hash_db = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hash, email) VALUES (?, ?, ?);", username, hash_db, email)
            return render_template("index.html") #add feedback of successful registration
    else:
        return render_template("index.html")

@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    if request.method == "POST":
        cart_content = db.execute("SELECT * FROM cart WHERE user_id = ?", session["user_id"])
        return render_template("checkout.html", cart_content=cart_content)
    else:
        cart_content = db.execute("SELECT * FROM cart WHERE user_id = ?", session["user_id"])
        totalPrice = 0
        for row in cart_content:
            totalPrice += (row["ppc"] * row["qty"])
        print(totalPrice)
        return render_template("checkout.html", cart_content=cart_content, totalPrice=totalPrice)

@app.route("/addcart", methods=["GET", "POST"])
@login_required
def addcart():
    if request.method == "POST":
        global card_name
        card_dataInfo = searchCard(card_name)
        name = card_dataInfo["name"]
        img_url = card_dataInfo["img_url"]
        card_tag = request.form.get("print_tag")
        rarity = request.form.get("rarity")
        price = request.form.get("avg_price")
        quantity = request.form.get("quantity")
        print(session["user_id"])
        #add condition where card already exists in card for qty
        db.execute("INSERT INTO cart (card, card_set, rarity, qty, ppc, user_id, img_url) VALUES (?, ?, ?, ?, ?, ?, ?);", name, card_tag, rarity, quantity, price, session["user_id"], img_url)
        return redirect("/") #add feedback of successful add to cart
    else:
        return render_template("index.html")

@app.route("/updatequantity", methods=["POST"])
def updatequantity():
    action = request.form.get("action")
    item_id = request.form.get("item_id")
    if action == "increase":
        db.execute("UPDATE cart SET qty = qty + 1 WHERE id = ?", item_id)
    elif action == "decrease":
        db.execute("UPDATE cart SET qty = qty - 1 WHERE id = ?", item_id)
    updated_quantity = db.execute("SELECT qty FROM cart WHERE id = ?", item_id)
    cart_content = db.execute("SELECT * FROM cart WHERE user_id = ?", session["user_id"])
    total_qty = sum(row["qty"] for row in cart_content)
    ppc = db.execute("SELECT ppc FROM cart WHERE id = ?", item_id)
    return jsonify(success=True, quantity=updated_quantity, itemID=item_id, totalQty=total_qty, ppc=ppc)







