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
    """
    Decorator that validates the token passed in through the Authorisation header

    Usage:
        - Add above any HTTP method defined in your class
        - E.g.
        =================================
        |   @example_ns.route("/")      |
        |   class ExampleClass():       |
        |       @example_ns.doc(...)    |
        |       @token_required         |
        |       def post(self, user):   |
        |           pass                |
        =================================

    Return Value:
        Returns a User object if the token passed in was validated successfully
        Otherwise, rejects HTTP request with error code 403
    """
    def wrapper(*args, **kwargs):
        try:
            if not (auth_token := request.headers.get("Authorisation")):
                raise InvalidSignatureError()

            decoded = decode_jwt_token(auth_token)
            email = decoded.get("email")

            if not (user:=User.query.filter(User.email==email).first()) or user.token != auth_token:
                raise InvalidSignatureError()

            kwargs["user"] = user
        except Exception as err:
            return {"message": f"Unauthorised request: {err}"}, 403
        return func(*args, **kwargs)
    return wrapper