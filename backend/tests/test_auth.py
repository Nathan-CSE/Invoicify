import pytest
import json

from tests.fixtures import client
from models import db, User
from src.utils import salt_and_hash, create_jwt_token, db_insert

REGISTER_PATH = "/auth/register"
LOGIN_PATH = "/auth/login"
CHANGE_PW_PATH = "/auth/change-pw"

def test_register_successfully(client):
    data = {
        "email": "abc@gmail.com",
        "password": "abc"
    }
    res = client.post(
        REGISTER_PATH, 
        data=json.dumps(data),
        content_type="application/json"
    )

    response_body = json.loads(res.data)

    jwt_token = response_body.get('token')
    assert jwt_token is not None, "JWT token should be present"

    user = User.query.where(User.email==data["email"]).first()
    assert user

def test_register_user_already_exists(client):
    db_insert(User(email="abc@gmail.com", password=salt_and_hash("abc"), token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFiY0BnbWFpbC5jb20ifQ.t5iNUNMkVVEVGNcPx8UdmwWgIMJ22j36xn4kXB-e-qM"))

    res = client.post(
        REGISTER_PATH, 
        data=json.dumps({
            "email": "abc@gmail.com",
            "password": "abc"
        }),
        content_type="application/json"
    )

    assert res.status_code == 400

def test_login_successfully(client):
    db_insert(User(email="abc@gmail.com", password=salt_and_hash("abc"), token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFiY0BnbWFpbC5jb20ifQ.t5iNUNMkVVEVGNcPx8UdmwWgIMJ22j36xn4kXB-e-qM"))

    data = {
        "email": "abc@gmail.com",
        "password": "abc"
    }

    res = client.post(
        LOGIN_PATH,
        data=json.dumps(data),
        content_type="application/json"
    )

    assert res.status_code == 200

    response_body = json.loads(res.data)

    jwt_token = response_body.get('token')
    assert jwt_token == create_jwt_token({"email": data["email"]})
    
def test_login_with_wrong_password(client):
    db_insert(User(email="abc@gmail.com", password=salt_and_hash("abc"), token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFiY0BnbWFpbC5jb20ifQ.t5iNUNMkVVEVGNcPx8UdmwWgIMJ22j36xn4kXB-e-qM"))

    data = {
        "email": "abc@gmail.com",
        "password": "abc123"
    }

    res = client.post(
        LOGIN_PATH,
        data=json.dumps(data),
        content_type="application/json"
    )

    assert res.status_code == 400

def test_login_with_account_that_doesnt_exist(client):
    data = {
        "email": "abc@gmail.com",
        "password": "abc"
    }

    res = client.post(
        LOGIN_PATH,
        data=json.dumps(data),
        content_type="application/json"
    )

    assert res.status_code == 400

def test_change_pw_successfully(client):
    db_insert(User(email="abc@gmail.com", password=salt_and_hash("abc"), token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFiY0BnbWFpbC5jb20ifQ.t5iNUNMkVVEVGNcPx8UdmwWgIMJ22j36xn4kXB-e-qM"))

    data = {
        "email": "abc@gmail.com",
        "password": "abc",
        "updated_password": "abc123"
    }

    res = client.patch(
        CHANGE_PW_PATH,
        data=json.dumps(data),
        content_type="application/json"
    )

    assert res.status_code == 200

    user = User.query.where(User.email==data["email"]).first()
    assert user.password == salt_and_hash(data["updated_password"])

def test_change_pw_with_account_that_doesnt_exist(client):
    data = {
        "email": "abc@gmail.com",
        "password": "abc",
        "updated_password": "abc123"
    }

    res = client.patch(
        CHANGE_PW_PATH,
        data=json.dumps(data),
        content_type="application/json"
    )

    assert res.status_code == 400