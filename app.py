from datetime import datetime
from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)

app.secret_key = "secret123" 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")


@app.route("/")
def home():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()   # ✅ get all products

    return render_template("index.html", products=products)

@app.route("/cart")
def cart():
    return render_template("cart.html")


@app.route("/admin")
def admin():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    conn.close()

    return render_template("admin.html", products=products)

from werkzeug.utils import secure_filename

@app.route("/add-product", methods=["POST"])
def add_product():

    name = request.form["name"]
    price = request.form["price"]
    category = request.form["category"]

    image = request.files["image"]
    filename = secure_filename(image.filename)

    image.save(os.path.join("static/images", filename))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO products (name, price, image, category) VALUES (?, ?, ?, ?)",
        (name, price, filename, category)
    )

    conn.commit()
    conn.close()

    return redirect("/admin")

@app.route("/product/<int:id>")
def product_detail(id):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE id=?", (id,))
    product = cursor.fetchone()

    conn.close()

    return render_template("product.html", product=product)


@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
        "INSERT INTO users (username,password) VALUES (?,?)",
        (username,password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username,password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            session["user"] = username
            return redirect("/")
        else:
            return "Invalid login"

    return render_template("login.html")

@app.route("/logout")
def logout():

    session.pop("user",None)

    return redirect("/")

@app.route("/checkout", methods=["POST"])
def checkout():

    if "user" not in session:
        return redirect("/login")

    cart = request.form["cart"]

    items = cart.split(",")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    for item in items:

        name, price = item.split("|")

        cursor.execute(
        "INSERT INTO orders (username,product,price,order_date) VALUES (?,?,?,?)",
        (session["user"], name, price, today)
        )

    conn.commit()
    conn.close()

    return render_template("order_success.html")
@app.route("/orders")
def orders():

    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
    "SELECT * FROM orders WHERE username=?",
    (session["user"],)
    )

    orders = cursor.fetchall()

    conn.close()

    return render_template("orders.html", orders=orders)


@app.route("/admin/orders")
def admin_orders():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders")

    orders = cursor.fetchall()

    conn.close()

    return render_template("admin_orders.html", orders=orders)

@app.route("/search")
def search():

    query = request.args.get("q")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
    "SELECT * FROM products WHERE name LIKE ?",
    ('%' + query + '%',)
    )

    products = cursor.fetchall()

    conn.close()

    return render_template("index.html", products=products)


@app.route("/category/<cat>")
def category(cat):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
    "SELECT * FROM products WHERE category=?",
    (cat,)
    )

    products = cursor.fetchall()

    conn.close()

    return render_template("index.html", products=products)

@app.route("/delete-product/<int:id>")
def delete_product(id):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM products WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/admin")

@app.route("/update-product/<int:id>", methods=["POST"])
def update_product(id):

    name = request.form["name"]
    price = request.form["price"]
    category = request.form["category"]

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
    "UPDATE products SET name=?, price=?, category=? WHERE id=?",
    (name,price,category,id)
    )

    conn.commit()
    conn.close()

    return redirect("/admin")

if __name__ == "__main__":
    app.run(debug=True)