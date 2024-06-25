from flask import Flask, request, jsonify, make_response
from flask_restx import Namespace, Resource, fields
import secrets

from models import db, User
from src.services.utils import salt_and_hash, create_jwt_token, db_insert
from src.services.send_mail import auth_request

auth_ns = Namespace('auth', description='Operations related to authentication')

email_field = fields.String(default="jane.smith@example.com", format="email", required=True)
password_field = fields.String(default="password123", format="password", required=True)
updated_password_field = fields.String(default="newpassword123", required=True)

user_authentication_fields = auth_ns.model('UserAuthentication', {
    "email": email_field,
    "password": password_field
})
user_send_code_fields = auth_ns.model("UserSendCode", {
    "email": email_field
})
user_reset_pw_fields = auth_ns.model("UserResetPassword", {
    "email": email_field,
    "reset_code": fields.String(default="XXXXXXXX", required=True),
    "updated_password": updated_password_field
})
user_change_pw_fields = auth_ns.model("UserChangePassword", {
    "email": email_field,
    "password": password_field,
    "updated_password": updated_password_field
})

@auth_ns.route("/register")
class RegisterAPI(Resource):
    @auth_ns.doc(
    description="Registers a new user and returns their JWT token",
    body=user_authentication_fields,
    responses={
        201: 'Created successfully',
        400: 'Bad request',
    })
    def post(self):
        data = request.json
        
        email = data['email']
        password = data['password']
        
        hashed_password = salt_and_hash(password)

        if User.query.where(User.email==email).first():
            return make_response(jsonify({"message": "email already registered, if you forgotten your password, please reset your password instead."}), 400)
        
        token = create_jwt_token({'email': email})

        db_insert(User(email=email, password=hashed_password, token=token))
        
        return make_response(jsonify({"message": "User registered successfully.", "token": token}), 201)

@auth_ns.route("/login")
class LoginAPI(Resource):
    @auth_ns.doc(
    description="Login an existing user and returns their JWT token",
    body=user_authentication_fields,
    responses={
        200: 'Success',
        400: 'Bad request',
    })
    def post(self):
        data = request.json
        
        email = data['email']
        password = data['password']

        hashed_password = salt_and_hash(password)

        if not (user := User.query.where(User.email==email).first()) or user.password != hashed_password:
            return make_response(jsonify({"message": "Your email/ password does not match an entry in our system, create an account instead?"}), 400)

        token = create_jwt_token({'email': email})
        return make_response(jsonify({"message": "User logged in successfully.", "token": token}), 200)
        
@auth_ns.route("/change-pw")
class ChangePWAPI(Resource):
    @auth_ns.doc(
    description="Changes a user's password",
    body=user_change_pw_fields,
    responses={
        200: 'Success',
        400: 'Bad request',
    })
    def patch(self):
        data = request.json
        
        email = data['email']
        password = data['password']
        updated_password = data['updated_password']
        
        hashed_password = salt_and_hash(password)

        user = User.query.filter_by(email=email).first() 
        if user is None:
            return make_response(jsonify({"message": "User not found"}), 400)

        if user.password != hashed_password:
            return make_response(jsonify({"message": "Your password does not match"}), 400)
            
        user.password = salt_and_hash(updated_password)
        db.session.commit()

        return make_response(jsonify({"message": "Your password has been changed successfully"}),200)

@auth_ns.route("/reset-code")
class SendCode(Resource):
    @auth_ns.doc(
    description="Sends an email to the user with a reset code",
    body=user_send_code_fields,
    responses={
        200: 'Sent successfully',
        400: 'Bad request',
    })
    def patch(self):
        data = request.json
        email = data['email']
        user = User.query.filter_by(email=email).first() 
        if user is None:
            return make_response(jsonify({"message": "User not found"}), 400)

        code = secrets.token_hex(8)
        user.reset_code = code
        db.session.commit()
        try:
            auth_request(email, code)
        except:
            print("not a valid email")
        return make_response(jsonify({"message": "Success"}), 200)

@auth_ns.route("/reset-pw")
class ResetPass(Resource):
    @auth_ns.doc(
    description="Resets the users password if the provided reset-code is correct",
    body=user_reset_pw_fields,
    responses={
        204: 'Reset successfully',
        400: 'Bad request',
    })
    def patch(self):
        data = request.json
        email = data['email']
        user = User.query.filter_by(email=email).first() 
        if user is None:
            print("user not found")
            return make_response(jsonify({"message": "User not found"}), 400)
        if user.reset_code == data['reset_code']:
            password = data['updated_password']
            user.password = salt_and_hash(password)
            user.reset_code = None
            db.session.commit()
            return make_response(jsonify({"message": "Your password has been changed successfully"}),204)
        else:
            print("code match")
            print(user.reset_code)
            print(data["reset_code"])
            return make_response(jsonify({"message": "Your code does not match"}), 400)


        


            
        
      
        
