# Standard library imports

# Remote library imports
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
# from flask_restful import Api,Resource
from model import db, User, Product, Searches, Category, Shop



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shophorizon.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

CORS(app)

# api = Api(app)

with app.app_context():
     db.create_all()

@app.route('/')
def index():
     return "Hello, world!"

@app.route('/products', methods = ['GET'])
def all_products():
     products =[]
     for product in Product.query.all():
          product_dict ={
               "name":product.name,
               "price":product.price,
               "ratings":product.ratings,
               "mode_of_payment":product.mode_of_payment,
               "categoryId":product.categoryId,
               "shopId":product.id,
               "product_image":product.product_image
          }
          products.append(product_dict)
     response = make_response(
          products, 200
     )
     return response
     


@app.route("/searchhistory", methods = ['GET'])
def searches():
     searches = []
     for search in Searches.query.all():
          search_dict = {
               "products": search.products
          }
          searches.append(search_dict)
     response = make_response(
          searches, 200
     )
     return response


if __name__ == "__main__":
    app.run(port=5555, debug=True)