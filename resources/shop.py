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
       
        if not name:
            return make_response({"message": "Name is a required field."}, 400)

        existing_shop = Shop.query.filter_by(name=name).first()
        if existing_shop:
            return make_response({"message": "Shop with this name already exists."}, 409)

        new_shop = Shop(name=name)
        db.session.add(new_shop)
        db.session.commit()

        return {"message": "Shop created successfully."}, 201



class ShopProducts(Resource):
    def get(self, shop_id):
        print(shop_id)
        shop = Shop.query.get(shop_id)
        print
        if not shop:
            return make_response({"message": "Shop not found."}, 404)
        
        products = Product.query.filter_by(shop_id=shop_id).all()
        product_list = [product.to_dict() for product in products]

        return jsonify(product_list)