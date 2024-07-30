# Standard library imports

# Remote library imports
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api,Resource
from model import db, User, Product, Searches, Category, Shop



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shophorizon.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

CORS(app)

api = Api(app)

with app.app_context():
     db.create_all()

@app.route('/')
def index():
     return "Hello, world!"

class Products(Resource):
     def get(self):
          products = Product.query.all()
          products = [product.to_dict() for product in products]
          return products
     
     def post(self):
          data = request.get_json()
          new_product = Product(
               name = data.get("name"),
               price = data.get("price"),
               ratings = data.get("ratings"),
               mode_of_payment = data.get("mode_of_payment"),
               categoryId = data.get("categoryId"),
               shopId = data.get("shopId"),
               product_image = data.get("product_image")
          )

          db.session.add(new_product)
          db.session.commit()
          return make_response(new_product.to_dict(), 200)
          
api.add_resource(Products, '/products')


if __name__ == "__main__":
    app.run(port=5555, debug=True)