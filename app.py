from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
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

class CategoryList(Resource):
    def get(self):
        categories = Category.query.all()
        categories = [category.to_dict() for category in categories]
        return jsonify(categories)




class SearchHistory(Resource):
    def get(self):
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




class ProductsByCategory(Resource):
    def get(self, category_id):
        query = Product.query.filter_by(categoryId=category_id).all()
        
        if not query:
            return {"message": "No products found for this category with the applied filters"}, 404

        products_list = [product.to_dict() for product in query]
        
        # Group products by shop
        products_by_shop = {}
        product_names = set()

        for product in products_list:
            shop_id = product['shopId']
            shop = db.session.get(Shop, shop_id)

            
            if shop:
                shop_name = shop.name
                
                if shop_name not in products_by_shop:
                    products_by_shop[shop_name] = {
                        'products': []
                    }
                
                products_by_shop[shop_name]['products'].append(product)
                product_names.add(product['name'])

        product_names = sorted(product_names)

        return {
            "products_by_shop": products_by_shop,
            "product_names": product_names,
        }

class FilteredProducts(Resource):
    def get(self):
        # Get filter parameters from request args
        price_min = request.args.get('price_min', type=float)
        price_max = request.args.get('price_max', type=float)
        rating_min = request.args.get('rating_min', type=float)
        rating_max = request.args.get('rating_max', type=float)
        name = request.args.get('name', type=str)
        mode_of_payment = request.args.get('mode_of_payment', type=str)
        
        # Build query with filters
        query = Product.query

        if price_min is not None:
            query = query.filter(Product.price >= price_min)
        if price_max is not None:
            query = query.filter(Product.price <= price_max)
        if rating_min is not None:
            query = query.filter(Product.ratings >= rating_min)
        if rating_max is not None:
            query = query.filter(Product.ratings <= rating_max)
        if name:
            query = query.filter(Product.name.ilike(f'%{name}%'))
        if mode_of_payment:
            query = query.filter(Product.mode_of_payment.ilike(f'%{mode_of_payment}%'))

        products = query.all()
        
        if not products:
            return {"message": "No products found with the applied filters"}, 404

        products_list = [product.to_dict() for product in products]

        return {
            "products": products_list
        }

api.add_resource(SearchHistory, "/searchhistory")
api.add_resource(CategoryList, '/categories')
api.add_resource(ProductsByCategory, '/categories/<int:category_id>/')
api.add_resource(FilteredProducts, '/filtered-products')

if __name__ == "__main__":
    app.run(port=5555, debug=True)
