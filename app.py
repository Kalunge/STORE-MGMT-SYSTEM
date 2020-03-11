from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identify


app = Flask(__name__)
api = Api(app)
jwt = JWT(app, authenticate, identify)

items = []



class Item(Resource):
    def get(self, name):
        item = next(filter(lambda x :x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x :x['name'] == name, items), None):
            return {'message' : f'an item with the name {name} already exists'}, 400
        data = request.get_json()
        new_item = {
            'name':name, 'price' : data['price']
        }
        items.append(new_item)

        return new_item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'item deleted successfully'}

    def put(self, name):
        data = request.get_json()
        item = next(filter(lambda x :x['name'] == name, items), None)
        if item:
            item.update(data)
        else:
            item = {
                'name' : name, 'price' : data['price']
            }
            items.append(item)
            return {'item' : item}
            
class ItemList(Resource):
    def get(self):
        pass

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')



app.run(debug=True)