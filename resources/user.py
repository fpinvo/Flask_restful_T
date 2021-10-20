import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel



class UserRegistor(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="User required."
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="passowrd required."
    )

    def post(self):
        data = UserRegistor.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message':'username {} already created!'.format(data['username'])}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message':'User created successfully.'},201