from model import User, db
from flask_restful import Resource
from flask import request, jsonify , make_response

class Users(Resource):
    def get(self):
        users = User.query.all()
        users = [user.to_dict() for user in users]
        return users

    

