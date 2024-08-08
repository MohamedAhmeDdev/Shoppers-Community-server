from flask_restful import Resource
from flask import request, jsonify, make_response
from model import Shop,Product, db

from flask_jwt_extended import jwt_required


class ShopList(Resource):
    def get(self):
        shops = Shop.query.all()
        shop_list = [shop.to_dict() for shop in shops]
        return jsonify(shop_list)


class ShopCreate(Resource):
    def post(self):
        data = request.get_json()

        name = data.get('name')
       

        if not name :
            return make_response({"message": "Name required fields."}, 400)

        new_shop = Shop(name=name)
        db.session.add(new_shop)
        db.session.commit()

        return make_response({"message": "Shop created successfully."}, 201)


class ShopProducts(Resource):
    @jwt_required()
    def get(self, shop_id):
        shop = Shop.query.get(shop_id)
        if not shop:
            return make_response({"message": "Shop not found."}, 404)
        
        products = Product.query.filter_by(shopId=shop_id).all()
        product_list = [product.to_dict() for product in products]

        return jsonify(product_list)