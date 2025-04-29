# app.py

from flask import (
    Flask, render_template, request, redirect,
    url_for, session, abort
)
from flask_session import Session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

# ─── Application Setup ────────────────────────────────────────────────────────
app = Flask(__name__)
app.config.update(
    SECRET_KEY='a-very-secret-key',
    SESSION_TYPE='filesystem',

    # MySQL credentials
    MYSQL_HOST='localhost',
    MYSQL_USER='root',
    MYSQL_PASSWORD='Twisted@love25',
    MYSQL_DB='plants_and_pots'
)

# ─── Initialize Extensions ────────────────────────────────────────────────────
Session(app)
mysql = MySQL(app)


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname    = request.form['username']
        pwd_hash = generate_password_hash(request.form['password'])

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (uname, pwd_hash)
        )
        mysql.connection.commit()
        cur.close()

        session['user'] = uname
        return redirect(url_for('plants'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd   = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT password_hash FROM users WHERE username = %s",
            (uname,)
        )
        row = cur.fetchone()
        cur.close()

        if row and check_password_hash(row[0], pwd):
            session['user'] = uname
            return redirect(url_for('plants'))

        return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')


@app.route('/plants')
def plants():
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT id, name, description, price, image_url, stock_qty FROM plants"
    )
    plant_rows = cur.fetchall()
    cur.close()
    return render_template('plants.html', plants=plant_rows)


@app.route('/plant/<int:plant_id>')
def detail(plant_id):
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT id, name, description, price, image_url, stock_qty "
        "FROM plants WHERE id = %s",
        (plant_id,)
    )
    plant = cur.fetchone()
    cur.close()

    if not plant:
        abort(404)

    return render_template('detail.html', plant=plant)


@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    plant_id = request.form.get('plant_id')
    qty      = int(request.form.get('qty', 1))

    cart = session.get('cart', {})
    cart[plant_id] = cart.get(plant_id, 0) + qty
    session['cart'] = cart

    return redirect(url_for('view_cart'))


@app.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    items = []
    total = 0.0

    cur = mysql.connection.cursor()
    for pid, qty in cart.items():
        cur.execute(
            "SELECT name, price, image_url FROM plants WHERE id = %s",
            (pid,)
        )
        row = cur.fetchone()
        if row:
            name, price_dec, img = row
            price = float(price_dec)           # cast Decimal→float
            line  = price * qty
            items.append({
                'id':    pid,
                'name':  name,
                'price': price,
                'img':   img,
                'qty':   qty,
                'line':  line
            })
            total += line
    cur.close()

    return render_template('cart.html', items=items, total=total)


@app.route('/checkout')
def checkout():
    session.pop('cart', None)
    return (
        "<h1>Thank you for your purchase!</h1>"
        "<p><a href='/plants'>Continue Shopping</a></p>"
    )


# ─── Main ─────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)
