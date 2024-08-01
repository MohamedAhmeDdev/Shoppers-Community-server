# Standard library imports

# Remote library imports
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api,Resource
from model import db, User, Product, Searches, Category, Shop
from flask_bcrypt import Bcrypt
import jwt
import datetime


app = Flask(_name_)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shophorizon.db'
app.config['SECRET_KEY'] = 'weststsgjgjgjtyb'
app.json.compact = False
bcrypt = Bcrypt()

migrate = Migrate(app, db)
db.init_app(app)

CORS(app)

api = Api(app)

with app.app_context():
     db.create_all()





class Register(Resource):
    def post(self):
        data = request.get_json()
        existing_user = User.query.filter_by(email=data.get("email")).first()
        if existing_user:
            return {'message': 'Email already exists'}, 400
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user = User(first_name=data['first_name'], last_name=data['last_name'], email=data['email'], password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return {'message': 'User registered successfully'}, 201

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            token = jwt.encode({
                'user_id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, app.config['SECRET_KEY'], algorithm='HS256')
            return {'token': token}, 200
        else:
            return {'message': 'Invalid credentials'}, 401





api.add_resource(Register, "/register")
api.add_resource(Login, "/login")



if _name_ == "_main_":
    app.run(port=5555, debug=True)