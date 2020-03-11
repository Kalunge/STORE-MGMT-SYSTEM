from flask import Flask, request
from flask_restful import Resource, Api, reqparse
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
        parser = reqparse.RequestParser()
        parser.add_argument('price',
            type=float,
            required=True,
            help='this field cannot be left empty')
        data = parser.parse_args()

        new_item = {
            'name':name, 'price' : data['price']
        }
        items.append(new_item)

        return new_item, 201

    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'item deleted successfully'}

    # @jwt_required()
    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('price',
            type = float,
            required=True,
            help='this field canmot be left blank'
        )
        data = parser.parse_args()
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
        return {'items' : items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')



app.run(debug=True)