from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="field can't be empty"
    )

    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help="field can't be empty"
    )

    @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'Item not found'},404    

    def post(self,name):
        if ItemModel.find_by_name(name):
            return {'message':'Item with the name {} is already in database'.format(name)},400
        
        data = Item.parser.parse_args()
        
        item = ItemModel(name,data['price'])
        try:
            item.save_to_db()
        except:
            return {'message':'An error occored during the inserting item'},500
        return item.json(),201


    def put(self,name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            item.price = data['price']
        else:
            item = ItemModel(name,data['price'])
        item.save_to_db()
        return item.json()

    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message':'item has been deleted'}
        return {'message':'no item found'}
class ItemList(Resource):
    
    def get(self):
        return {'items':[item.json() for item in ItemModel.query.all()]}