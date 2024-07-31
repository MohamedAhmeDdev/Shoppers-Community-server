# Standard library imports

# Remote library imports
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from model import db, User, Product, Searches, Category, Shop



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shophorizon.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

CORS(app)

with app.app_context():
     db.create_all()

@app.route('/')
def index():
     return "Hello, world!"

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