from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'VerySecret'
api = Api(app)
jwt = JWT(app, authenticate, identity)

items = []


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        name='price',
        required=True,
        help='This filed should not left blank!'
    )

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404
        

    def post(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item == None:
            data = Item.parser.parse_args()
            item = {
                'name': name,
                'price': data['price']}
            items.append(item)
            return item, 201
        return {'error': f'item {item["name"]} already exist'}, 400

    def delete(self, name):
        for item in items:
            if item['name'] == name:
                items.remove(item)
                return {'message': f'Item {name} has removed successfuly'}
        return {'error': f'item {name} does not exist'}, 404

    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item:
            item.update(data)
        else:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        return item




class ItemList(Resource):
    def get(self):
        return {'items list': items}



api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')


if __name__ == '__main__':
    app.run(debug=True)