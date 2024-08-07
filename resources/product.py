from flask_restful import Resource
from flask import request, jsonify , make_response
from model import Product, Shop, Searches, db
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from sqlalchemy import func



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

class Products(Resource):
    def get(self):
        products = Product.query.all()
        products = [product.to_dict() for product in products]
        return jsonify(products)
    
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
    
class ProductID(Resource):
    def get(self, id):
        product = Product.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(product), 201)    

    def delete(self, id):
        product = Product.query.filter_by(id=id).first()
        db.session.delete(product)
        db.session.commit()
        response = make_response({"message": "Product deleted successfully"}, 201)
        return response

