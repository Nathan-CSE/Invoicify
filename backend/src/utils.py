import os
import hashlib
import jwt

from models import db

def salt_and_hash(data):
    return hashlib.sha512((data + os.getenv("SALT")).encode('UTF-8')).hexdigest()

def create_jwt_token(payload):
    return jwt.encode(payload, os.getenv("JWTSECRET"), algorithm='HS256')

def decode_jwt_token(token):
    return jwt.decode(token, os.getenv("JWTSECRET"), algorithms=["HS256"], options={"verify_exp": False})

def db_insert(model):
    db.session.add(model)
    db.session.commit()