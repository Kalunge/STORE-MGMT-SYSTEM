from flask import Flask, request, jsonify


app = Flask(__name__)
app.secret_key = 'muthomi'

stores = [
    {
        'name':'Bookstore',
        'items':[
            {
                'name':'Bible',
                'price':45.99
            }
        ]
    }
]


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message':'welcome to the store management system homepage'})


# create a store
@app.route('/store', methods=['POST'])
def create_store():
    requested_data = request.get_json()
    new_store = {
        'name':requested_data['name'],
        'items':[]
    }

    stores.append(new_store)

    return jsonify({'stores':stores})


@app.route('/store/<string:name>', methods=['GET']) #get store from db
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'store':store})
    return jsonify(message='The store you are looking for is not available')


@app.route('/store', methods=['GET']) #retireve a list od stores
def get_stores():
    return jsonify({'stores':stores})



@app.route('/store/<string:name>/item', methods=['POST']) #create item
def create_item_in_store(name):
    for store in stores:
        request_data = request.get_json()
        if store['name'] == name:
            new_item = {
                'name':request_data['name'],
                'price':request_data['price']
            }
            store['items'].append(new_item)
            
            return jsonify({'item':new_item})

    return jsonify('Store unavailable')


@app.route('/store/<string:name>/item', methods=['GET']) 
def get_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items':store['items']})
    return jsonify('Store not found')



app.run(port=5000)