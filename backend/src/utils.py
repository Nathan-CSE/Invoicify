import os
import hashlib
import jwt

from models import db

def salt_and_hash(data):
    return hashlib.sha512((data + os.getenv("SALT")).encode('UTF-8')).hexdigest()

def create_jwt_token(payload):
    return jwt.encode(payload, os.getenv("JWTSECRET"), algorithm='HS256')

def query_db(sql):
    """
    Takes in a query
    i.e. db.select(User).where(User.email==data["email"])

    Returns a list containing the objects queried
    """
    return db.session.execute(sql).scalars().all()