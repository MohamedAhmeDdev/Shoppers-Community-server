from flask import jsonify
from flask_restful import Resource
from model import Category, Product, Shop, db

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