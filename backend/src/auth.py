from flask import Flask, request, jsonify, make_response
from flask.views import MethodView
from flask_restx import Namespace, Resource
from models import db, User
from sqlalchemy import select, exists
from src.utils import salt_and_hash, create_jwt_token, query_db

auth_ns = Namespace('auth', description='Operations related to authentication')

@auth_ns.route("/register")
class RegisterAPI(Resource):
    def post(self):
        data = request.json
        
        email = data['email']
        password = data['password']
        
        hashed_password = salt_and_hash(password)

        if query_db(db.select(User).where(User.email==email)):
            return make_response(jsonify({"message": "email already registered, if you forgotten your password, please reset your password instead."}), 400)
        
        db.session.add(User(email=email, password=hashed_password))
        db.session.commit()
        
        token = create_jwt_token({'email': email})
        
        return make_response(jsonify({"message": "User registered successfully.", "token": token}), 201)

@auth_ns.route("/login")
class LoginAPI(Resource):
    def post(self):
        data = request.json
        
        email = data['email']
        password = data['password']

        hashed_password = salt_and_hash(password)

        if not (result := query_db(db.select(User).where(User.email==email))) or result[0].password != hashed_password:
            return make_response(jsonify({"message": "Your email/ password does not match an entry in our system, create an account instead?"}), 400)

        token = create_jwt_token({'email': email})
        return make_response(jsonify({"message": "User logged in successfully.", "token": token}), 200)
            
        
        
@auth_ns.route("/change-pw")
class ChangePWAPI(Resource):
    def patch(self):
        data = request.json
        
        email = data['email']
        password = data['password']
        updated_password = data['updated_password']
        
        hashed_password = salt_and_hash(password)

        user = User.query.filter_by(email=email).first() 
    
        if user is None:
            return make_response(jsonify({"message": "User not found"}), 400)

        if user.first()[0].password != hashed_password:
            return make_response(jsonify({"message": "Your password does not match"}), 400)
            
        user.password = salt_and_hash(updated_password)

        db.session.commit()
        
        return make_response(jsonify({}),204)
            
        
      
        