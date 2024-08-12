from model import User, db
from flask_restful import Resource
from flask import request, jsonify , make_response
from flasgger import swag_from

class Users(Resource):
    @swag_from({
        'tags': ['User'],
        'description': 'Get all users or create a new user',
        'parameters': [
            {
                'name': 'first_name',
                'in': 'formData',
                'type': 'string',
                'description': 'First name of the user',
                'required': False
            },
            {
                'name': 'last_name',
                'in': 'formData',
                'type': 'string',
                'description': 'Last name of the user',
                'required': False
            },
            {
                'name': 'email',
                'in': 'formData',
                'type': 'string',
                'description': 'Email of the user',
                'required': False
            },
            {
                'name': 'password',
                'in': 'formData',
                'type': 'string',
                'description': 'Password of the user',
                'required': False
            }
        ],
        'responses': {
            '200': {
                'description': 'List of users',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'id': {
                                'type': 'integer',
                                'example': 1
                            },
                            'first_name': {
                                'type': 'string',
                                'example': 'John'
                            },
                            'last_name': {
                                'type': 'string',
                                'example': 'Doe'
                            },
                            'email': {
                                'type': 'string',
                                'example': 'john.doe@example.com'
                            }
                        }
                    }
                }
            },
            '201': {
                'description': 'User created successfully',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {
                            'type': 'string',
                            'example': 'User created successfully'
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
                            'example': 'Invalid input'
                        }
                    }
                }
            }
        }
    })
    def get(self):
        users = User.query.all()
        users = [user.to_dict() for user in users]
        return make_response(jsonify(users), 200)
    
    @swag_from({
        'tags': ['User'],
        'description': 'Create a new user',
        'parameters': [
            {
                'name': 'first_name',
                'in': 'formData',
                'type': 'string',
                'description': 'First name of the user',
                'required': True
            },
            {
                'name': 'last_name',
                'in': 'formData',
                'type': 'string',
                'description': 'Last name of the user',
                'required': True
            },
            {
                'name': 'email',
                'in': 'formData',
                'type': 'string',
                'description': 'Email of the user',
                'required': True
            },
            {
                'name': 'password',
                'in': 'formData',
                'type': 'string',
                'description': 'Password of the user',
                'required': True
            }
        ],
        'responses': {
            '201': {
                'description': 'User created successfully',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {
                            'type': 'string',
                            'example': 'User created successfully'
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
                            'example': 'Invalid input'
                        }
                    }
                }
            }
        }
    })
    def post(self):
        data = request.get_json()
        new_user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            password=data["password"],
            email=data["email"]
        )

        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({'message': 'User created successfully'}), 201)
    
class UserID(Resource):
    @swag_from({
        'tags': ['User'],
        'description': 'Get a user by ID',
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'type': 'integer',
                'description': 'ID of the user to retrieve',
                'required': True
            }
        ],
        'responses': {
            '200': {
                'description': 'User details',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'id': {
                            'type': 'integer',
                            'example': 1
                        },
                        'first_name': {
                            'type': 'string',
                            'example': 'John'
                        },
                        'last_name': {
                            'type': 'string',
                            'example': 'Doe'
                        },
                        'email': {
                            'type': 'string',
                            'example': 'john.doe@example.com'
                        }
                    }
                }
            },
            '404': {
                'description': 'User not found',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {
                            'type': 'string',
                            'example': 'User not found'
                        }
                    }
                }
            }
        }
    })
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            return make_response(jsonify({"message": "User not found"}), 404)
        return make_response(jsonify(user.to_dict()), 200)
    
    @swag_from({
        'tags': ['User'],
        'description': 'Delete a user by ID',
        'parameters': [
            {
                'name': 'id',
                'in': 'path',
                'type': 'integer',
                'description': 'ID of the user to delete',
                'required': True
            }
        ],
        'responses': {
            '200': {
                'description': 'User deleted successfully',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {
                            'type': 'string',
                            'example': 'User deleted successfully'
                        }
                    }
                }
            },
            '404': {
                'description': 'User not found',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {
                            'type': 'string',
                            'example': 'User not found'
                        }
                    }
                }
            }
        }
    })
    def delete(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            return make_response(jsonify({"message": "User not found"}), 404)
        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({"message": "User deleted successfully"}), 200)
