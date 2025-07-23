from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
DB_NAME = 'bill_db.sqlite'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/generate_bill', methods=['POST'])
def generate_bill():
    customer_name = request.form['customer_name']
    product_ids = request.form.getlist('product_id')
    quantities = request.form.getlist('quantity')

    conn = get_db_connection()
    total_price = 0.0
    items = []

    for pid, qty in zip(product_ids, quantities):
        qty = int(qty)
        if qty <= 0:
            continue
        product = conn.execute("SELECT * FROM products WHERE id = ?", (pid,)).fetchone()
        if product:
            price = product['price'] * qty
            total_price += price
            items.append({
                'product_id': pid,
                'name': product['name'],
                'quantity': qty,
                'unit_price': product['price'],
                'total_price': price
            })

    cursor = conn.cursor()
    cursor.execute("INSERT INTO bills (customer_name, total) VALUES (?, ?)", (customer_name, total_price))
    bill_id = cursor.lastrowid

    for item in items:
        cursor.execute("INSERT INTO bill_items (bill_id, product_id, quantity, price) VALUES (?, ?, ?, ?)",
                       (bill_id, item['product_id'], item['quantity'], item['total_price']))

    conn.commit()
    conn.close()

    return render_template('bill.html', customer=customer_name, items=items, total=total_price)

if __name__ == '__main__':
    app.run(debug=True)
