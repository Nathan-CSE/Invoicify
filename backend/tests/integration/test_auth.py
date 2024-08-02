import json

from tests.fixtures import client, user
from tests.urls import REGISTER_PATH, LOGIN_PATH, CHANGE_PW_PATH, GET_CODE, FORGOT_PASS
from models import User
from src.services.utils import salt_and_hash

def test_register_login_interaction(client):
    data = {
        "email": "abc@gmail.com",
        "password": "abc"
    }
    res = client.post(
        REGISTER_PATH, 
        data=json.dumps(data),
        content_type="application/json"
    )

    register_response = res.json
    assert res.status_code == 201

    res = client.post(
        LOGIN_PATH,
        data=json.dumps(data),
        content_type="application/json"
    )

    assert res.status_code == 200
    
    login_response = res.json

    assert login_response["token"] == register_response["token"]

def test_register_reset_pw_interaction(client):
    data = {
        "email": "abc@gmail.com",
        "password": "abc"
    }
    res = client.post(
        REGISTER_PATH, 
        data=json.dumps(data),
        content_type="application/json"
    )

    assert res.status_code == 201

    data = {
        "email": "abc@gmail.com"
    }

    res = client.patch(
        GET_CODE,
        data=json.dumps(data),
        content_type="application/json"
    )
    assert res.status_code == 200

    user = User.query.where(User.email==data["email"]).first()
    assert user.reset_code

    data = {
        "email": "abc@gmail.com",
        "reset_code": f"{user.reset_code}",
        "updated_password": "123abc"
    }
    
    res = client.patch(
        FORGOT_PASS,
        data=json.dumps(data),
        content_type="application/json"
    )
    assert res.status_code == 204

    user = User.query.where(User.email==data["email"]).first()
    assert user.reset_code == None
    assert user.password == salt_and_hash("123abc")

def test_register_change_pw_interaction(client):
    data = {
        "email": "abc@gmail.com",
        "password": "abc"
    }
    res = client.post(
        REGISTER_PATH, 
        data=json.dumps(data),
        content_type="application/json"
    )

    assert res.status_code == 201

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
