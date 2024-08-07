from flask_restful import Resource
from flask import request, jsonify, make_response
from model import Shop, db

from flask_jwt_extended import jwt_required

@jwt_required()
class ShopList(Resource):
    def get(self):
        shops = Shop.query.all()
        shop_list = [shop.to_dict() for shop in shops]
        return jsonify(shop_list)

@jwt_required()
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