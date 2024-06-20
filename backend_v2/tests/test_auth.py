import pytest
import json

from tests.fixtures import client
from models import db, User
from src.utils import salt_and_hash, create_jwt_token

REGISTER_URI = "/auth/register"
LOGIN_URI = "/auth/login"

def test_register_successfully(client):
    res = client.post(
        REGISTER_URI, 
        data=json.dumps({
            "email": "abc@gmail.com",
            "password": "abc"
        }),
        content_type="application/json"
    )

    response_body = json.loads(res.data)

    jwt_cookie = response_body.get('cookie')
    assert jwt_cookie is not None, "JWT cookie should be present"

def test_register_user_already_exists(client):
    db.session.add(User(email="abc@gmail.com", password=salt_and_hash("abc")))
    db.session.commit()

    res = client.post(
        REGISTER_URI, 
        data=json.dumps({
            "email": "abc@gmail.com",
            "password": "abc"
        }),
        content_type="application/json"
    )

    assert res.status_code == 400

def test_login_successfully(client):
    db.session.add(User(email="abc@gmail.com", password=salt_and_hash("abc")))
    db.session.commit()

    data = {
        "email": "abc@gmail.com",
        "password": "abc"
    }

    res = client.post(
        LOGIN_URI,
        data=json.dumps(data),
        content_type="application/json"
    )

    assert res.status_code == 200

    response_body = json.loads(res.data)

    jwt_cookie = response_body.get('cookie')
    assert jwt_cookie == create_jwt_token({"email": data["email"]})
    
def test_login_with_wrong_password(client):
    db.session.add(User(email="abc@gmail.com", password=salt_and_hash("abc")))
    db.session.commit()

    data = {
        "email": "abc@gmail.com",
        "password": "abc123"
    }

    res = client.post(
        LOGIN_URI,
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
        LOGIN_URI,
        data=json.dumps(data),
        content_type="application/json"
    )

    assert res.status_code == 400