from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_bcrypt import Bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_mail import Mail, Message
import secrets
from datetime import datetime, timedelta
from model import db, User

bcrypt = Bcrypt()
mail = Mail()






class Register(Resource):
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
        )
        db.session.add(user)
        db.session.commit()

        # Send verification email
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
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            if not user.is_verified:
                return {'message': 'Account not Verified. Please check your email.'}, 403
            token = create_access_token(identity=user.id)
            return {'token': token}, 200
        
        return {'message': 'Invalid credentials'}, 401



class ForgotPassword(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data.get('email')).first()
        if not user:
            return {'message': 'No user found with this email'}, 404

        # Generate password reset token and expiration
        reset_token = secrets.token_urlsafe(16)
        reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
        user.reset_token = reset_token
        user.reset_token_expiry = reset_token_expiry
        db.session.commit()

        # Send reset email
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
    def post(self, token):
        user = User.query.filter_by(reset_token=token).first()
        if not user or user.reset_token_expiry < datetime.utcnow():
            return {'message': 'token has expired'}, 400

        data = request.get_json()
        password = data.get('password')
        confirm_password = data.get('confirmPassword')

        if password != confirm_password:
            return {'message': 'Passwords do not match'}, 400

        # Update user password (assuming you have a method to hash the password)
        user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        user.reset_token = None
        user.reset_token_expiry = None
        db.session.commit()

        return {'message': 'Password reset successfully'}, 200