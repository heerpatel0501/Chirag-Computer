from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect('database.db')

    conn.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price TEXT,
        ram TEXT,
        storage TEXT,
        processor TEXT,
        image TEXT
    )''')

    conn.execute('''CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        review TEXT
    )''')

    conn.close()

init_db()

# ---------- HOME ----------
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')

    products = conn.execute("SELECT * FROM products").fetchall()
    reviews = conn.execute("SELECT * FROM reviews").fetchall()

    conn.close()

    return render_template('index.html', products=products, reviews=reviews)

# ---------- ADD PRODUCT (ADMIN) ----------
@app.route('/add', methods=['POST'])
def add_product():
    name = request.form['name']
    price = request.form['price']
    ram = request.form['ram']
    storage = request.form['storage']
    processor = request.form['processor']
    file = request.files['image']

    filename = file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    conn = sqlite3.connect('database.db')
    conn.execute(
        "INSERT INTO products (name, price, ram, storage, processor, image) VALUES (?, ?, ?, ?, ?, ?)",
        (name, price, ram, storage, processor, filepath)
    )
    conn.commit()
    conn.close()

    return redirect('/')

# ---------- ADD REVIEW ----------
@app.route('/add_review', methods=['POST'])
def add_review():
    name = request.form['name']
    review = request.form['review']

    conn = sqlite3.connect('database.db')
    conn.execute(
        "INSERT INTO reviews (name, review) VALUES (?, ?)",
        (name, review)
    )
    conn.commit()
    conn.close()

    return redirect('/')

# ---------- RUN ----------
if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)