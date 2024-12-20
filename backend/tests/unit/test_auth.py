import json

from tests.fixtures import client, user
from models import User
from src.services.utils import salt_and_hash, create_jwt_token, db_insert
from tests.urls import REGISTER_PATH, LOGIN_PATH, CHANGE_PW_PATH, GET_CODE, FORGOT_PASS

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

def test_register_user_already_exists(client, user):
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
    
def test_login_with_wrong_password(client, user):
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

def test_change_pw_successfully(client, user):
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

# Forgot password 
def test_change_forgot_pass(client, user):
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
    data_reset = {
        "email": "abc@gmail.com",
        "reset_code": f"{user.reset_code}",
        "updated_password": "123abc"
    }
    
    res = client.patch(
        FORGOT_PASS,
        data=json.dumps(data_reset),
        content_type="application/json"
    )
    assert res.status_code == 204

    user = User.query.where(User.email==data["email"]).first()
    assert user.reset_code == None
    assert user.password == salt_and_hash("123abc")



def test_forgot_pw_with_account_that_doesnt_exist(client):
    data = {
        "email": "not_a_test",
    }

    res = client.patch(
        GET_CODE,
        data=json.dumps(data),
        content_type="application/json"
    )
    
    assert res.status_code == 400

def test_forgot_pw_with_wrong_code(client):
    data = {
        "email": "test",
        "password": "abc",
        "updated_password": "abc123"
    }

    res = client.patch(
        GET_CODE,
        data=json.dumps(data),
        content_type="application/json"
    )

    assert res.status_code == 400