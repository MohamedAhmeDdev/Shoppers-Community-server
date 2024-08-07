from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from flask_mail import Mail, Message
import psycopg2
import secrets
from datetime import timedelta, datetime
from sqlalchemy import func
from config import (
    SECRET_KEY, JWT_SECRET_KEY, DATABASE_URI, MAIL_SERVER, MAIL_PORT, 
    MAIL_USERNAME, MAIL_PASSWORD, MAIL_USE_TLS, MAIL_USE_SSL
)
from model import db, User, Product, Searches, Category, Shop
from resources.auth import Register, Login, VerifyEmail, ForgotPassword, ResetPassword
from resources.category import CategoryList, GetProductsByCategory
from resources.product import FilteredProducts, GetQueryProduct, FilteredQueryProduct, PostSearchHistory, UserSearchHistory
from resources.shop import ShopList, ShopCreate

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = MAIL_USE_SSL

app.json.compact = False
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
db.init_app(app)
CORS(app)
jwt = JWTManager(app)
mail = Mail(app)
api = Api(app)

with app.app_context():
    db.create_all()

# Database connection setup
def get_db_connection():
    conn = psycopg2.connect(
        host="dpg-cqnm7gjv2p9s73afrvug-a.oregon-postgres.render.com",
        database="shops_db_0mhk",
        user="shops_db_0mhk_user",
        password="MrPxVSEUPz4aJ2pgI0JF2EnYz01cOEHF",
         sslmode='require' 
    )
    return conn

@app.teardown_appcontext
def close_connection(exception):
    conn = get_db_connection()
    if conn is not None:
        conn.close()



    

api.add_resource(Register, "/register")
api.add_resource(Login, "/login")
api.add_resource(VerifyEmail, '/verify/<string:token>')
api.add_resource(ForgotPassword, '/forgot-password')
api.add_resource(ResetPassword, '/reset-password/<string:token>')
api.add_resource(CategoryList, '/categories')
api.add_resource(GetProductsByCategory, '/categories/<int:category_id>/')
api.add_resource(FilteredProducts, '/filtered-products')
api.add_resource(GetQueryProduct, '/search')
api.add_resource(FilteredQueryProduct, '/filterequery')
api.add_resource(PostSearchHistory, "/post-search-history")
api.add_resource(UserSearchHistory, "/searchhistory")
api.add_resource(ShopList,"/shop")
api.add_resource(ShopCreate,"/create-shop")

if __name__ == "__main__":
    app.run(port=5555, debug=True)