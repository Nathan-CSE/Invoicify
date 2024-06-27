import os
import hashlib
import jwt
from jwt.exceptions import InvalidSignatureError
from flask import request

from models import db, User

def salt_and_hash(data):
    return hashlib.sha512((data + os.getenv("SALT")).encode('UTF-8')).hexdigest()

def create_jwt_token(payload):
    return jwt.encode(payload, os.getenv("JWTSECRET"), algorithm='HS256')

def decode_jwt_token(token):
    return jwt.decode(token, os.getenv("JWTSECRET"), algorithms=["HS256"], options={"verify_exp": False})

def db_insert(model):
    db.session.add(model)
    db.session.commit()

def token_required(func):
    def wrapper(*args, **kwargs):
        try:
            if not (auth_token := request.headers.get("Authorisation")) or auth_token[:6] != "Bearer":
                raise InvalidSignatureError()

            token_str_list = auth_token.split()

            if len(token_str_list) != 2:
                raise InvalidSignatureError()

            auth_token = token_str_list[1]
            decoded = decode_jwt_token(auth_token)
            email = decoded.get("email")

            if not (user:=User.query.filter(User.email==email).first()) or user.token != auth_token:
                raise InvalidSignatureError()
        except InvalidSignatureError as err:
            return {"message": f"Unauthorised request: {err}"}, 403
        return func(*args, **kwargs)
    return wrapper