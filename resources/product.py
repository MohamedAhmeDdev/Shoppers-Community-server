from flask_restful import Resource
from flask import request, jsonify , make_response
from model import Product, Shop, Searches, Category, db
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from sqlalchemy import func
import cloudinary
import cloudinary.uploader


cloudinary.config(
    cloud_name='dows56r9v',
    api_key='352337169378987',
    api_secret='zRPXOHtgbFiTbRoq3q7NGG3hLeg'
)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_image_to_cloudinary(image_path):
    try:
        response = cloudinary.uploader.upload(image_path, folder="shopHorizon")
        return response['secure_url']
    except Exception as e:
        print(f"Error uploading image: {e}")
        return None
    

class CreateProduct(Resource):
    def post(self):
        if 'file' not in request.files:
            return {'message': 'No file part'}, 400
        
        file = request.files['file']
        if file.filename == '':
            return {'message': 'No selected file'}, 400
        
        if file and allowed_file(file.filename):
            if len(file.read()) == 0:
                return {'message': 'Empty file'}, 400
            file.seek(0) 

            result = cloudinary.uploader.upload(file)
            file_url = result['url']
            
            name = request.form.get('name')
            price = request.form.get('price')
            ratings = request.form.get('ratings')
            mode_of_payment = request.form.get('mode_of_payment')
            category_name = request.form.get('category_name')
            shop_name = request.form.get('shop_name')

            if not name:
                return {'message': 'Product name is required'}, 400
            if not category_name:
                return {'message': 'Category name is required'}, 400
            if not shop_name:
                return {'message': 'Shop name is required'}, 400

            category = Category.query.filter_by(name=category_name).first()
            if not category:
                return {'message': 'Invalid category name'}, 400
            print(shop_name)
            shop = Shop.query.filter_by(name=shop_name).first()
            print(shop)
            if not shop:
                return {'message': 'Invalid shop name'}, 400

            product = Product(
                name=name, 
                price=price, 
                ratings=ratings,
                mode_of_payment=mode_of_payment, 
                categoryId=category.id,
                shopId=shop.id, 
                product_image=file_url
            )
            db.session.add(product)
            db.session.commit()
               
            return {'message': 'File uploaded and product created successfully!', 'url': file_url}, 201
        
        return {'message': 'File upload failed'}, 400
    


class UpdateProduct(Resource):
    def put(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            return {'message': 'Product not found'}, 404

        file = request.files.get('file')
        if file:
            if not allowed_file(file.filename):
                return {'message': 'Invalid file type'}, 400
            if len(file.read()) == 0:
                return {'message': 'Empty file'}, 400
            file.seek(0)
            result = cloudinary.uploader.upload(file)
            product.product_image = result['url']

        name = request.form.get('name')
        price = request.form.get('price')
        ratings = request.form.get('ratings')
        mode_of_payment = request.form.get('mode_of_payment')
        category_name = request.form.get('category_name')
        shop_name = request.form.get('shop_name')

        if name:
            product.name = name
        if price:
            try:
                product.price = float(price)
            except (TypeError, ValueError):
                return {'message': 'Price must be a number'}, 400
        if ratings:
            try:
                product.ratings = float(ratings)
            except (TypeError, ValueError):
                return {'message': 'Ratings must be a number'}, 400
        if mode_of_payment:
            product.mode_of_payment = mode_of_payment
        if category_name:
            category = Category.query.filter_by(name=category_name).first()
            if not category:
                return {'message': 'Invalid category name'}, 400
            product.categoryId = category.id
        if shop_name:
            shop = Shop.query.filter_by(name=shop_name).first()
            if not shop:
                return {'message': 'Invalid shop name'}, 400
            product.shopId = shop.id

        db.session.commit()
        return {'message': 'Product updated successfully'}, 200


class FilteredProducts(Resource):

    def get(self):
  
        category_id = request.args.get('category_id', type=int)  
        rating = request.args.get('rating', type=float)
        product = request.args.get('product', type=str)
        mode_of_payment = request.args.get('paymentMethod', type=str)
        min_price = request.args.get('priceMin', type=float)
        max_price = request.args.get('priceMax', type=float)
     
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
        search = request.args.get('query', '').lower()
     
     
        products = Product.query.all()
        
        if search:
            products = [product for product in products if search in product.name.lower()]
    
        products_list = [product.to_dict() for product in products]
        
        return jsonify(products_list)
    

class FilteredQueryProduct(Resource):
    def get(self):
       
        rating = request.args.get('rating', type=float)
        product_name = request.args.get('product_name', type=str)
        mode_of_payment = request.args.get('paymentMethod', type=str)
        min_price = request.args.get('priceMin', type=float)
        max_price = request.args.get('priceMax', type=float)
     
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



class PostSearchHistory(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        print(data)
        
        product_name = data.get('query')

        if not product_name:
            return make_response({"message": "Product name is required"}, 400)

        product = Product.query.filter_by(name=product_name).first()
        
        if product:
            product_id = product.id

            # Check if the search already exists to prevent duplicates
            existing_search = Searches.query.filter_by(userId=user_id, productId=product_id).first()
            if existing_search:
                return make_response({"message": "Search history already exists"}, 200)

            new_search = Searches(userId=user_id, productId=product_id)
            db.session.add(new_search)
            db.session.commit()
            
            response = make_response({"message": "Search history added successfully"}, 201)
        else:
            response = make_response({"message": "Product not found"}, 404)
        
        return response
        
       




class UserSearchHistory(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        searches = Searches.query.filter_by(userId=user_id).all()

        search_data = [
            {
                "productName": search.product.name,
                "productPrice": search.product.price,
                "searchDate": search.created_at, 
                "productImage": search.product.product_image
            } for search in searches
        ]

        return jsonify({"products": search_data})
