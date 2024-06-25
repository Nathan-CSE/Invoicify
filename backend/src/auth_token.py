from flask import request
from jwt.exceptions import InvalidSignatureError

from src.utils import decode_jwt_token
from models import User

def token_required(func):
    def wrapper(*args, **kwargs):
        try:
            if not (auth_token := request.headers.get("Authorisation")):
                raise InvalidSignatureError()

            decoded = decode_jwt_token(auth_token)
            email = decoded.get("email")

            if not (user:=User.query.filter(User.email==email).first()) or user.token != auth_token:
                raise InvalidSignatureError()
        except InvalidSignatureError as err:
            return {"message": f"Unauthorised request: {err}"}, 403
        return func(*args, **kwargs)
    return wrapper