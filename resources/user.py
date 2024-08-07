from model import User, db
from flask_restful import Resource
from flask import request, jsonify , make_response

class Users(Resource):
    def get(self):
        users = User.query.all()
        users = [user.to_dict() for user in users]
        return users
    
    def post(self):
        data = request.get_json()
        new_user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        password = data[ "password"],
        email = data["email"]
        )

        db.session.add(new_user)
        db.session.commit()
    
class UserID(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(user), 200)
