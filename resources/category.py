from flask import jsonify , request,make_response
from flask_restful import Resource
from model import Category, Product, Shop, db
import cloudinary
import cloudinary.uploader
from flasgger import swag_from


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
    

class CreateCategory(Resource):
    @swag_from({
        'tags': ['Category'],
        'description': 'Create a new category with an image',
        'parameters': [
            {
                'name': 'file',
                'in': 'formData',
                'type': 'file',
                'description': 'Image file for the category',
                'required': True
            },
            {
                'name': 'name',
                'in': 'formData',
                'type': 'string',
                'description': 'Name of the category',
                'required': True
            }
        ],
        'responses': {
            '201': {
                'description': 'Category created successfully',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {
                            'type': 'string',
                            'example': 'File uploaded successfully!'
                        },
                        'url': {
                            'type': 'string',
                            'example': 'https://res.cloudinary.com/your-cloud-name/image/upload/v1234567890/shopHorizon/your-image.jpg'
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
                            'example': 'No file part'
                        }
                    }
                }
            }
        }
    })
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
            
            category_name = request.form.get('name')
            if not category_name:
                return {'message': 'Category name is required'}, 400
            
            existing_category = Category.query.filter_by(name=category_name).first()
            if existing_category:
                return {'message': f'Category "{category_name}" already exists'}, 400
            
            category = Category(name=category_name, category_image=file_url)
            db.session.add(category)
            db.session.commit()
               
            return {'message': 'File uploaded successfully!', 'url': file_url}, 201
        
        return {'message': 'File upload failed'}, 400






class CategoryList(Resource):
    @swag_from({
        'tags': ['Category'],
        'description': 'Get the list of all categories',
        'responses': {
            '200': {
                'description': 'List of categories',
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
                                'example': 'Electronics'
                            },
                            'category_image': {
                                'type': 'string',
                                'example': 'https://res.cloudinary.com/your-cloud-name/image/upload/v1234567890/shopHorizon/your-image.jpg'
                            }
                        }
                    }
                }
            }
        }
    })
    def get(self):
        categories = Category.query.all()
        categories = [category.to_dict() for category in categories]
        return jsonify(categories)




class GetProductsByCategory(Resource):
    def get(self, category_id):
        query = Product.query.filter_by(category_id=category_id).all()
        if not query:
            return {"message": "No products found for this category with the applied filters"}, 404

        products_list = [product.to_dict() for product in query]
        products_by_shop = {}
        product_names = set()

        for product in products_list:
            shop_id = product['shop_id']
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
    


class CategoryID(Resource):
    @swag_from({
        'tags': ['Category'],
        'description': 'Delete a category by its ID',
        'parameters': [
            {
                'name': 'category_id',
                'in': 'path',
                'type': 'integer',
                'description': 'ID of the category to delete',
                'required': True
            }
        ],
        'responses': {
            '200': {
                'description': 'Category deleted successfully',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {
                            'type': 'string',
                            'example': 'Category deleted successfully'
                        }
                    }
                }
            },
            '404': {
                'description': 'Category not found',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {
                            'type': 'string',
                            'example': 'Category not found'
                        }
                    }
                }
            }
        }
    })
    def delete(self, category_id):
        category = Category.query.filter_by(id=category_id).first()
        db.session.delete(category)
        db.session.commit()
        response = make_response({"message": "category deleted successfully"}, 201)
        return response
