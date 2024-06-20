from flask import Flask, request, jsonify, make_response
from flask.views import MethodView
from models import db, User
from sqlalchemy import select, exists
import hashlib
import os 
import jwt

class RegisterAPI(MethodView):
    def post(self):
        data = request.json
        
        email = data['email']
        password = data['password']
        
        salt = os.getenv("SALT")
        hashed_password = hashlib.sha512((password + salt).encode('UTF-8')).hexdigest()

        if db.session.execute(db.select(User).filter_by(email=email)).first():
            return jsonify({"message": "email already registered, if you forgotten your password, please reset your password instead."}), 400   
        
        db.session.add(User(email=email, password=hashed_password))
        db.session.commit()
        
        secretJWT = os.getenv("JWTSECRET")
        cookie = jwt.encode({'email': email}, secretJWT, algorithm='HS256')
        
        return jsonify({"message": "User registered successfully.", "cookie": cookie}), 201

class LoginAPI(MethodView):
    def post(self):
        data = request.json
        
        email = data['email']
        password = data['password']
        
        salt = os.getenv("SALT")
        hashed_password = hashlib.sha512((password + salt).encode('UTF-8')).hexdigest()

        sql = db.select(User).where(User.email==email)
        data = db.session.execute(sql).first()
        
        if not data:
            return jsonify({"message": "Your email/ password does not match an entry in our system, create an account instead?"}), 400
        user = data[0]

        if user.password != hashed_password:
            return jsonify({"message": "Your email/ password does not match an entry in our system, create an account instead?"}), 400

        secretJWT = os.getenv("JWTSECRET")
        cookie = jwt.encode({'email': email}, secretJWT, algorithm='HS256')
        return jsonify({"message": "User logged in successfully.", "cookie": cookie}), 200
            
        
        
class ChangePWAPI(MethodView):
    def patch(self):
        data = request.json
        
        email = data['email']
        password = data['password']
        updated_password = data['updated_password']
        
        salt = os.getenv("SALT")
        hashed_password = hashlib.sha512((password + salt).encode('UTF-8')).hexdigest()

        # sql = select(User).where(User.email==email)
        # user = db.session.execute(sql)
        user = User.query.filter_by(email=email).first() #TODO 
    
        if user is None:
            return jsonify({"message": "User not found"}), 404

        if user.first()[0].password != hashed_password:
            return jsonify({"message": "Your password does not match"}), 400
            
        hashed_new = hashlib.sha512((updated_password + salt).encode('UTF-8')).hexdigest()
        user.password = hashed_new

        db.session.commit()
        
        return jsonify({"message": "You have successfully changed your password."}), 200
            
        
      
        