from flask import Flask, jsonify, request, render_template
import nlpcloud, os
from flask_cors import CORS
import json
import braintree

app = Flask(__name__)
app = Flask(__name__, template_folder='templates')

CORS(app)

# Initialize the NLP Cloud client
client = nlpcloud.Client("nllb-200-3-3b", os.getenv('TRANSLATOR_API_KEY'))

# client2 = currencyapicom.Client(os.getenv('CURRENCY_API_KEY'))
# result = client2.latest('USD',currencies=['AUD','EUR'])
# print(result)

# Sample data for demonstration (replace this with your actual data storage logic)
# menu_items = [
#     {"id": 1, "name": "Popcorn", "price": 5.99},
#     {"id": 2, "name": "Cookies", "price": 3.99},
#     {"id": 3, "name": "Sprite", "price": 10.99},
#      Add more menu items as needed
# ]
from menus import menu_items_AA, menu_items_Frontier, menu_items_Southwest, menu_items_Delta, menu_items_Spirit, menu_items_BritishAirways,menu_items_Alaska, menu_items_Allegiant,all_menu_items


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/confirmation")
def confirmation():
    return render_template("confirmation_page.html")

@app.route('/menuAA', methods=['GET'])
def get_menu_AA():
    airline_name = "American Airlines"
    return render_template('menu.html', menu_items=menu_items_AA, airline_name=airline_name)
@app.route('/menuDelta', methods=['GET'])
def get_menu_Delta():
    airline_name = "Delta Airlines"
    return render_template('menu.html', menu_items=menu_items_Delta, airline_name=airline_name)
@app.route('/menuSouthwest', methods=['GET'])
def get_menu_Southwest():
    airline_name = "Southwest Airlines"
    return render_template('menu.html', menu_items=menu_items_Southwest, airline_name=airline_name)
@app.route('/menuSpirit', methods=['GET'])
def get_menu_Spirit():
    airline_name = "Spirit Airlines"
    return render_template('menu.html', menu_items=menu_items_Spirit, airline_name=airline_name)
@app.route('/menuFrontier', methods=['GET'])
def get_menu_Frontier():
    airline_name = "Frontier Airlines"
    return render_template('menu.html', menu_items=menu_items_Frontier, airline_name=airline_name)
@app.route('/menuAlaska', methods=['GET'])
def get_menu_Alaska():
    airline_name = "Alaska Airlines"
    return render_template('menu.html', menu_items=menu_items_Alaska, airline_name=airline_name)
@app.route('/menuBritish', methods=['GET'])
def get_menu_British():
    airline_name = "British Airways"
    return render_template('menu.html', menu_items=menu_items_BritishAirways, airline_name=airline_name)
@app.route('/menuAllegiant', methods=['GET'])
def get_menu_Allegiant():
    airline_name = "Allegiant Airways"
    return render_template('menu.html', menu_items=menu_items_Allegiant, airline_name=airline_name)

@app.route('/translate', methods=['GET'])
def translate():
    translated_menu = []
    for item in menu_items_AA:
        try:
            translated_name = client.translation(item['name'], source='eng_Latn', target='spa_Latn')  # Translate from English to Spanish
            translated_item = {"name": translated_name, "price": item['price']}
            translated_menu.append(translated_item)
        except Exception as e:
            print(f"Error translating item '{item['name']}': {e}")
    return render_template('menu.html', menu_items=translated_menu)


selected_menu_items = []



# Configure Braintree API credentials (replace with your actual credentials)
# braintree.Configuration.configure(
#     braintree.Environment.Sandbox,
#     merchant_id='jjhycvgsf33h3hzv',
#     public_key='rs36fybb4dg368vb',
#     private_key='56612fc4d57d57164d6e7c31b298b900'
# )

# @app.route('/check')
# def index():
#     return render_template('test.html')

# @app.route('/client_token', methods=['GET'])
# def generate_client_token():



#     client_token = braintree.ClientToken.generate()
#     return jsonify({'client_token': client_token})

# @app.route('/process_payment', methods=['POST'])
# def process_payment():
#     nonce = request.json['paymentMethodNonce']
#     result = braintree.Transaction.sale({
#         "amount": "10.00",  # Replace with the actual amount
#         "payment_method_nonce": nonce,
#         "options": {
#             "submit_for_settlement": True
#         }
#     })

 


@app.route('/submit', methods=['POST'])
def submit_order():
    menu_item_ids = request.form.getlist('menu_item')
    global selected_menu_items
    selected_menu_items = []

    for menu_item_id in menu_item_ids:
        selected_item = next((item for item in all_menu_items if item['id'] == int(menu_item_id)), None)
        if selected_item:
            selected_menu_items.append(selected_item)

    total_amount = calculate_order_amount(menu_item_ids)
    total_price = total_amount / 100 
    return render_template('order.html', order_items=selected_menu_items, total_price=total_price)

def calculate_order_amount(selected_item_ids):
    total_amount = 0
    for item_id in selected_item_ids:
        selected_item = next((item for item in all_menu_items if item['id'] == int(item_id)), None)
        if selected_item:
            total_amount += selected_item['price']
    return total_amount * 100
    
if __name__ == '__main__':
    app.run(debug=True)
