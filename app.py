from flask import Flask
from flask_jwt import JWT, jwt_required
from flask_restful import Resource, Api
from werkzeug.datastructures import Authorization
from resources.item import Item, ItemList
from security import authenticate, identity
from resources.user import UserRegistor

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "farhan"
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegistor, '/registor')

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(debug=True)
