from flask import Flask, request, jsonify
from flask.views import MethodView
from models import session, User
from sqlalchemy import select, exists
import hashlib
import os 

class RegisterAPI(MethodView):
    def post(self):
        data = request.json
        
        username = data['username']
        password = data['password']
        
        salt = os.getenv("SALT")
        hashed_password = hashlib.sha512((password + salt).encode('UTF-8')).hexdigest()

        # check if user is already registered
        (ret, ), = session.query(exists().where(User.username==username))
        if ret:
            return jsonify({"message": "Username already registered, if you forgotten your password, please reset your password instead."}), 400
            
        
        session.add(User(username=username, password=hashed_password))
        session.commit()
        
        return jsonify({"message": "User registered successfully."}), 201

class LoginAPI(MethodView):
    def post(self):
        data = request.json
        
        username = data['username']
        password = data['password']
        
        salt = os.getenv("SALT")
        hashed_password = hashlib.sha512((password + salt).encode('UTF-8')).hexdigest()

        sql = select(User).where(User.username==username)
        user = session.execute(sql)
   
        if user.first()[0].password == hashed_password:
            return jsonify({"message": "User logged in successfully."}), 200
            
        return jsonify({"message": "Your username/ password does not match an entry in our system, create an account instead?"}), 400
        
        
class ChangePWAPI(MethodView):
    def patch(self):
        data = request.json
        
        username = data['username']
        password = data['password']
        updated_password = data['updated_password']
        
        salt = os.getenv("SALT")
        hashed_password = hashlib.sha512((password + salt).encode('UTF-8')).hexdigest()

        sql = select(User).where(User.username==username)
        user = session.execute(sql)
   
        if user.first()[0].password == hashed_password:
            hashed_new = hashlib.sha512((updated_password + salt).encode('UTF-8')).hexdigest()
            
            
            return jsonify({"message": "You have successfully changed your password."}), 200
            
        return jsonify({"message": "Your password does not match"}), 400
      
        