from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Sample product data
products = {
    1: {"name": "Oreo", "price": 10, "quantity": 5},
    2: {"name": "Coca-cola", "price": 15, "quantity": 5},
    3: {"name": "Fox-crystal", "price": 12, "quantity": 5},
    4: {"name": "orange-juice", "price": 30, "quantity": 5},
    5: {"name": "Kitkat", "price": 17, "quantity": 5},
}

total_inserted = 0
selected_product = None
input_history = []

@app.route('/')
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/select_product/<int:product_id>')
def select_product(product_id):
    global selected_product, total_inserted, input_history
    selected_product = product_id
    total_inserted = 0
    input_history = [f"Selected: {products[product_id]['name']}"]
    message = f"Selected: {products[product_id]['name']} - Rs {products[product_id]['price']}"
    return f"{total_inserted}|{message}|{' '.join(input_history)}"

@app.route('/insert_coin/<int:coin>')
def insert_coin(coin):
    global total_inserted, selected_product, input_history

    if selected_product is None:
        return f"{total_inserted}|Please select a product first.|{' '.join(input_history)}"

    total_inserted += coin
    input_history.append(f"Rs {coin}")
    product_info = products[selected_product]

    if total_inserted >= product_info['price']:
        if product_info['quantity'] <= 0:
            return f"{total_inserted}|Product out of stock!|{' '.join(input_history)}"
        else:
            change = total_inserted - product_info['price']
            products[selected_product]['quantity'] -= 1
            input_history.append(f"Dispensed: {product_info['name']}")
            return f"0|Enjoy your {product_info['name']}! Change: Rs {change}|{' '.join(input_history)}"

    return f"{total_inserted}|Total Inserted: Rs {total_inserted}|{' '.join(input_history)}"

@app.route('/reset')
def reset_machine():
    global total_inserted, selected_product, input_history
    total_inserted = 0
    selected_product = None
    input_history = []
    return "Machine reset successfully!"

if __name__ == '__main__':
    app.run(debug=True)
