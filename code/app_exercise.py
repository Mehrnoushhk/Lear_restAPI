from flask import Flask, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

items = []


class Item(Resource):
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item is not None else 404

    def post(self, name):
        data = request.get_json()
        new_item = {
            'name': name,
            'price': data['price']
        }
        items.append(new_item)


api.add_resource(Item, '/item/<string:name>')
