from flask import Flask, request, jsonify
from flask.views import MethodView
from models import session, User
from sqlalchemy import select
import hashlib
import os 

class RegisterAPI(MethodView):
    def post(self):
        data = request.json
        
        user = data['username']
        password = data['password']
        
        salt = os.getenv("SALT")
        hashed_password = hashlib.sha512((password + salt).encode('UTF-8')).hexdigest()

        session.add(User(username=user, password=hashed_password))
        session.commit()
        
        return jsonify({"message": "User registered successfully."}), 201

class LoginAPI(MethodView):
    def post(self):
        data = request.json
        
        username = data['username']
        password = data['password']
        
        salt = os.getenv("SALT")
        hashed_password = hashlib.sha512((password + salt).encode('UTF-8')).hexdigest()

        # user = User.query().get(username=username)
        sql = select(User).where(User.username==username)
        user = session.execute(sql)
   
        if user.first()[0].password == hashed_password:
            return jsonify({"message": "User logged in successfully."}), 200
            
        return jsonify({"message": "you fucking idiot."}), 400
        
      
        