from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_bcrypt import Bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_mail import Mail, Message
import secrets
from datetime import datetime, timedelta
from model import db, User
from flasgger import swag_from

bcrypt = Bcrypt()
mail = Mail()






class Register(Resource):
    @swag_from({
        'tags': ['Auth'],
        'description': 'Register a new user',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'example': {
                        'first_name': 'John',
                        'last_name': 'Doe',
                        'email': 'johndoe@example.com',
                        'password': 'password123',
                        'role': 'user'
                    }
                }
            }
        ],
        'responses': {
            201: {
                'description': 'User registered successfully',
                'schema': {
                    'example': {
                        'message': 'User registered successfully. Please check your email to verify your account.'
                    }
                }
            },
            400: {
                'description': 'Email already exists',
                'schema': {
                    'example': {
                        'message': 'Email already exists'
                    }
                }
            }
        }
    })
    def post(self):
        data = request.get_json()
        existing_user = User.query.filter_by(email=data.get("email")).first()
        if existing_user:
            return {'message': 'Email already exists'}, 400
        
        token = secrets.token_urlsafe(16)
      
        
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=hashed_password,
            verification_token=token,
            role=data['role'],
        )
        db.session.add(user)
        db.session.commit()


        verification_url = f"{token}"
        msg = Message(
            'Verify your email', 
            recipients=[data['email']],
            sender="eff@gmail.com"
        )
        msg.html = (
            f"<p>Dear {user.first_name} {user.last_name},</p>"
            "<p>Thank you for registering at ShopHorizon. To complete your registration and verify your email address, "
            "please click the link below:</p>"
            f"<p><a href='https://shoppers-community.vercel.app/user/{verification_url}'>Verify your email</a></p>"
            "<p>If you did not register for this account, please ignore this email.</p>"
            "<p>Best regards,<br>The ShopHorizon Team</p>"
        )
        mail.send(msg)

        return {'message': 'User registered successfully. Please check your email to verify your account.'}, 201
    


class VerifyEmail(Resource):
    def get(self, token):
        user = User.query.filter_by(verification_token=token).first()
        if not user:
            return {'message': 'Invalid or expired token'}, 400
        user.is_verified = True
        user.verification_token = None  
        db.session.commit()
        return {'message': 'Registration confirmed successfully'}, 200
    

class Login(Resource):
    @swag_from({
        'tags': ['Auth'],
        'description': 'Login a user',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'example': {
                        'email': 'johndoe@example.com',
                        'password': 'password123'
                    }
                }
            }
        ],
        'responses': {
            200: {
                'description': 'User logged in successfully',
                'schema': {
                    'example': {
                        'token': 'your-jwt-token',
                        'role': 'user'
                    }
                }
            },
            401: {
                'description': 'Invalid credentials',
                'schema': {
                    'example': {
                        'message': 'Invalid credentials'
                    }
                }
            },
            403: {
                'description': 'Account not verified',
                'schema': {
                    'example': {
                        'message': 'Account not Verified. Please check your email.'
                    }
                }
            }
        }
    })
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            if not user.is_verified:
                return {'message': 'Account not Verified. Please check your email.'}, 403
            token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
            return {'token': token, 'role': user.role}, 200
        
        return {'message': 'Invalid credentials'}, 401



class ForgotPassword(Resource):
    @swag_from({
        'tags': ['Auth'],
        'description': 'Request a password reset',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'example': {
                        'email': 'johndoe@example.com'
                    }
                }
            }
        ],
        'responses': {
            200: {
                'description': 'Password reset email sent successfully',
                'schema': {
                    'example': {
                        'message': 'Password reset email sent. Please check your email.'
                    }
                }
            },
            404: {
                'description': 'No user found with this email',
                'schema': {
                    'example': {
                        'message': 'No user found with this email'
                    }
                }
            }
        }
    })
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data.get('email')).first()
        if not user:
            return {'message': 'No user found with this email'}, 404

       
        reset_token = secrets.token_urlsafe(16)
        reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
        user.reset_token = reset_token
        user.reset_token_expiry = reset_token_expiry
        db.session.commit()

       
        reset_url = f"https://shoppers-community.vercel.app/resetpassword/{reset_token}"
        msg = Message(
            'Password Reset Request',
            recipients=[data['email']],
            sender="noreply@example.com"
        )
        msg.html = (
            f"<p>Dear {user.first_name},</p>"
            "<p>You requested to reset your password. Please click the link below to reset your password:</p>"
            f"<p><a href='{reset_url}'>Reset Password</a></p>"
            "<p>If you did not request this, please ignore this email.</p>"
            "<p>Best regards,<br>The ShopHorizon Team</p>"
        )
        mail.send(msg)

        return {'message': 'Password reset email sent. Please check your email.'}, 200



class ResetPassword(Resource):
    @swag_from({
        'tags': ['Auth'],
        'description': 'Request a password reset',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'example': {
                        'email': 'johndoe@example.com'
                    }
                }
            }
        ],
        'responses': {
            200: {
                'description': 'Password reset email sent successfully',
                'schema': {
                    'example': {
                        'message': 'Password reset email sent. Please check your email.'
                    }
                }
            },
            404: {
                'description': 'No user found with this email',
                'schema': {
                    'example': {
                        'message': 'No user found with this email'
                    }
                }
            }
        }
    })
    def post(self, token):
        user = User.query.filter_by(reset_token=token).first()
        if not user or user.reset_token_expiry < datetime.utcnow():
            return {'message': 'token has expired'}, 400

        data = request.get_json()
        password = data.get('password')
        confirm_password = data.get('confirmPassword')

        if password != confirm_password:
            return {'message': 'Passwords do not match'}, 400

        user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        user.reset_token = None
        user.reset_token_expiry = None
        db.session.commit()

        return {'message': 'Password reset successfully'}, 200