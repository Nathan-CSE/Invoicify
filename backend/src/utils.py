import os
import hashlib
import jwt

def salt_and_hash(data):
    return hashlib.sha512((data + os.getenv("SALT")).encode('UTF-8')).hexdigest()

def create_jwt_token(payload):
    return jwt.encode(payload, os.getenv("JWTSECRET"), algorithm='HS256')
