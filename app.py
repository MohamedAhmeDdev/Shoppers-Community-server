from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from model import db, User, Product, Searches, Category, Shop
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from flask_mail import Mail, Message
import secrets
from datetime import timedelta ,datetime
from sqlalchemy import func


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "postgresql://shophorizon_user:jnEYZqJvtDmMpanf7XdqVSuumDZ1s8oe@dpg-cqmv385ds78s739505e0-a.oregon-postgres.render.com/shophorizon?sslmode=require"
)
app.config['SECRET_KEY'] = 'weststsgjgjgjtyb'
app.config['JWT_SECRET_KEY'] = 'trduiguierifd'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'  
app.config['MAIL_PORT'] =  587
app.config['MAIL_USERNAME'] = 'mohamed.ahmed2@student.moringaschool.com'
app.config['MAIL_PASSWORD'] = 'yfwl nuoj oksv woya'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


app.json.compact = False
bcrypt = Bcrypt()
migrate = Migrate(app, db)
db.init_app(app)
CORS(app)
jwt = JWTManager(app)
mail = Mail(app)
api = Api(app)


with app.app_context():
    db.create_all()



class Register(Resource):
    def post(self):
        data = request.get_json()
        existing_user = User.query.filter_by(email=data.get("email")).first()
        if existing_user:
            return {'message': 'Email already exists'}, 400

        # Generate a verification token
        token = secrets.token_urlsafe(16)
      
        
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=hashed_password,
            verification_token=token,
        )
        db.session.add(user)
        db.session.commit()

        # Send verification email
        verification_url = f"{token}"
        msg = Message(
            'Verify your email', 
            recipients=[data['email']],
            sender="eff@gmail.com"
        )
        msg.html = (
            f"<p>Dear {user.first_name} {user.last_name},</p>"
            "<p>Thank you for registering at ShopHorizon. To complete your registration and verify your email address, "
            "please click the link below:</p>"
            f"<p><a href='http://localhost:3000/user/{verification_url}'>Verify your email</a></p>"
            "<p>If you did not register for this account, please ignore this email.</p>"
            "<p>Best regards,<br>The ShopHorizon Team</p>"
        )
        mail.send(msg)

        return {'message': 'User registered successfully. Please check your email to verify your account.'}, 201
    


class VerifyEmail(Resource):
    def get(self, token):
        user = User.query.filter_by(verification_token=token).first()
        if not user:
            return {'message': 'Invalid or expired token'}, 400
        user.is_verified = True
        user.verification_token = None  
        db.session.commit()
        return {'message': 'Registration confirmed successfully'}, 200
    

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            if not user.is_verified:
                return {'message': 'Account not Verified. Please check your email.'}, 403
            token = create_access_token(identity=user.id)
            return {'token': token}, 200
        
        return {'message': 'Invalid credentials'}, 401



class ForgotPassword(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data.get('email')).first()
        if not user:
            return {'message': 'No user found with this email'}, 404

        # Generate password reset token and expiration
        reset_token = secrets.token_urlsafe(16)
        reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
        user.reset_token = reset_token
        user.reset_token_expiry = reset_token_expiry
        db.session.commit()

        # Send reset email
        reset_url = f"http://localhost:3000/resetpassword/{reset_token}"
        msg = Message(
            'Password Reset Request',
            recipients=[data['email']],
            sender="noreply@example.com"
        )
        msg.html = (
            f"<p>Dear {user.first_name},</p>"
            "<p>You requested to reset your password. Please click the link below to reset your password:</p>"
            f"<p><a href='{reset_url}'>Reset Password</a></p>"
            "<p>If you did not request this, please ignore this email.</p>"
            "<p>Best regards,<br>The ShopHorizon Team</p>"
        )
        mail.send(msg)

        return {'message': 'Password reset email sent. Please check your email.'}, 200



class ResetPassword(Resource):
    def post(self, token):
        user = User.query.filter_by(reset_token=token).first()
        print(user)
        if not user or user.reset_token_expiry < datetime.utcnow():
            return {'message': 'token has expired'}, 400

        data = request.get_json()
        password = data.get('password')
        confirm_password = data.get('confirmPassword')

        if password != confirm_password:
            return {'message': 'Passwords do not match'}, 400

        # Update user password (assuming you have a method to hash the password)
        user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        user.reset_token = None
        user.reset_token_expiry = None
        db.session.commit()

        return {'message': 'Password reset successfully'}, 200
    



class CategoryList(Resource):
    def get(self):
        categories = Category.query.all()
        categories = [category.to_dict() for category in categories]
        return jsonify(categories)




class GetProductsByCategory(Resource):
    def get(self, category_id):
        query = Product.query.filter_by(categoryId=category_id).all()
        if not query:
            return {"message": "No products found for this category with the applied filters"}, 404

        products_list = [product.to_dict() for product in query]
        products_by_shop = {}
        product_names = set()

        for product in products_list:
            shop_id = product['shopId']
            shop = db.session.get(Shop, shop_id)
            if shop:
                shop_name = shop.name
                if shop_name not in products_by_shop:
                    products_by_shop[shop_name] = {'products': []}
                products_by_shop[shop_name]['products'].append(product)
                product_names.add(product['name'])

        product_names = sorted(product_names)
        return {
            "products_by_shop": products_by_shop,
            "product_names": product_names,
        }



class GetQueryProducts(Resource):
    def get(self):
      
        search = request.args.get('query', '').lower()
        print(search)
    
        products = Product.query.all()
       
        if search:
            products = [product for product in products if search in product.name.lower()]
            print(products)
        
        products_list = [product.to_dict() for product in products]
        
        return jsonify(products_list)
    


class FilteredProducts(Resource):

    def get(self):
  
        category_id = request.args.get('category_id', type=int)  
        rating = request.args.get('rating', type=float)
        product = request.args.get('product', type=str)
        mode_of_payment = request.args.get('paymentMethod', type=str)
        min_price = request.args.get('priceMin', type=float)
        max_price = request.args.get('priceMax', type=float)
        print(category_id, mode_of_payment)
     
        rounded_rating = round(rating) if rating is not None else None

     
        query = Product.query
        
      
        if category_id is not None:
            query = query.filter(Product.categoryId == category_id)
        
        if product:
            query = query.filter(Product.name.ilike(f'%{product}%'))
        if mode_of_payment:
            query = query.filter(Product.mode_of_payment.ilike(f'%{mode_of_payment}%'))
        if rounded_rating is not None:
        
            query = query.filter(func.round(Product.ratings) == rounded_rating)
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
      
        products = query.all()
        
        if not products:
            return {"message": "No products found with the applied filters"}, 404
        
        products_list = [product.to_dict() for product in products]
        return {"products": products_list}



class GetQueryProduct(Resource):
    def get(self):
        # Get the search term from the query parameters
        search = request.args.get('query', '').lower()
        print(search)
        
        # Fetch all products from the database
        products = Product.query.all()
        
        # Filter products based on the search term
        if search:
            products = [product for product in products if search in product.name.lower()]
            print(products)
        
        # Convert the products to a list of dictionaries
        products_list = [product.to_dict() for product in products]
        
        return jsonify(products_list)

class FilteredQueryProduct(Resource):
    def get(self):
       
        rating = request.args.get('rating', type=float)
        product_name = request.args.get('product_name', type=str)
        mode_of_payment = request.args.get('paymentMethod', type=str)
        min_price = request.args.get('priceMin', type=float)
        max_price = request.args.get('priceMax', type=float)
        print(mode_of_payment , product_name)
     
        rounded_rating = round(rating) if rating is not None else None

     
        query = Product.query
        
      
        if product_name is not None:
            query = query.filter(Product.name == product_name)
            
        
 
        if mode_of_payment:
            query = query.filter(Product.mode_of_payment.ilike(f'%{mode_of_payment}%'))
        if rounded_rating is not None:
            query = query.filter(func.round(Product.ratings) == rounded_rating)
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
      
        products = query.all()
        
        if not products:
            return {"message": "No products found with the applied filters"}, 404
        
        products_list = [product.to_dict() for product in products]
        return {"products": products_list}



class UserSearchHistory(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity() 
        searches = Searches.query.filter_by(userId=user_id).all()

        search_data = [
            {
                "products": search.products
            } for search in searches
        ]

        response = make_response(search_data, 200)
        return response
    

    

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
api.add_resource(UserSearchHistory, "/searchhistory")


if __name__ == "__main__":
    app.run(port=5555, debug=True)