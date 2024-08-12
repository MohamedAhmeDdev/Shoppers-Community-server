from flask_restful import Resource
from flask import request, jsonify, make_response
from model import Shop,Product, db

from flask_jwt_extended import jwt_required
from flasgger import swag_from

class ShopList(Resource):
    @swag_from({
        'tags': ['Shop'],
        'description': 'Get a list of all shops',
        'responses': {
            '200': {
                'description': 'List of shops',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'id': {
                                'type': 'integer',
                                'example': 1
                            },
                            'name': {
                                'type': 'string',
                                'example': 'Shop Name'
                            }
                        }
                    }
                }
            }
        }
    })
    def get(self):
        """Get a list of all shops"""
        shops = Shop.query.all()
        shop_list = [shop.to_dict() for shop in shops]
        return jsonify(shop_list)


class ShopCreate(Resource):
    @swag_from({
        'tags': ['Shop'],
        'description': 'Create a new shop',
        'parameters': [
            {
                'name': 'name',
                'in': 'body',
                'type': 'string',
                'description': 'Name of the shop',
                'required': True
            }
        ],
        'responses': {
            '201': {
                'description': 'Shop created successfully',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {
                            'type': 'string',
                            'example': 'Shop created successfully.'
                        }
                    }
                }
            },
            '400': {
                'description': 'Bad request',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {
                            'type': 'string',
                            'example': 'Name is a required field.'
                        }
                    }
                }
            },
            '409': {
                'description': 'Conflict',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {
                            'type': 'string',
                            'example': 'Shop with this name already exists.'
                        }
                    }
                }
            }
        }
    })
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
    @swag_from({
        'tags': ['Shop'],
        'description': 'Get all products in a specific shop',
        'parameters': [
            {
                'name': 'shop_id',
                'in': 'path',
                'type': 'integer',
                'description': 'ID of the shop to retrieve products for',
                'required': True
            }
        ],
        'responses': {
            '200': {
                'description': 'List of products for the shop',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'id': {
                                'type': 'integer',
                                'example': 1
                            },
                            'name': {
                                'type': 'string',
                                'example': 'Product Name'
                            },
                            'price': {
                                'type': 'number',
                                'format': 'float',
                                'example': 19.99
                            }
                        }
                    }
                }
            },
            '404': {
                'description': 'Shop not found',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {
                            'type': 'string',
                            'example': 'Shop not found.'
                        }
                    }
                }
            }
        }
    })
    def get(self, shop_id):
        shop = Shop.query.get(shop_id)
        if not shop:
            return make_response({"message": "Shop not found."}, 404)
        
        products = Product.query.filter_by(shop_id=shop_id).all()
        product_list = [product.to_dict() for product in products]

        return jsonify(product_list)
