import pytest
import json

from tests.fixtures import client
from models import db, User
from src.utils import salt_and_hash, create_jwt_token, query_db

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

    jwt_cookie = response_body.get('cookie')
    assert jwt_cookie is not None, "JWT cookie should be present"

    result = query_db(db.select(User).where(User.email==data["email"]))
    assert len(result) == 1

def test_register_user_already_exists(client):
    db.session.add(User(email="abc@gmail.com", password=salt_and_hash("abc")))
    db.session.commit()

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
    db.session.add(User(email="abc@gmail.com", password=salt_and_hash("abc")))
    db.session.commit()

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
    db.session.add(User(email="abc@gmail.com", password=salt_and_hash("abc")))
    db.session.commit()

    data = {
        "email": "abc@gmail.com",
        "password": "abc123"
    }

    res = client.post(
        CHANGE_PW_PATH,
        data=json.dumps(data),
        content_type="application/json"
    )

    assert res.status_code == 204

    result = query_db(db.select(User).where(User.email==email))
    assert len(result) == 1
    
    user = result[0]
    assert user.password == salt_and_hash(data["password"])

def test_change_pw_with_account_that_doesnt_exist(client):
    data = {
        "email": "abc@gmail.com",
        "password": "abc123"
    }

    res = client.post(
        CHANGE_PW_PATH,
        data=json.dumps(data),
        content_type="application/json"
    )

    assert res.status_code == 400