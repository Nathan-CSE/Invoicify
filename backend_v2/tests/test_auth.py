import pytest
import json

from tests.fixtures import client
from models import db, User

def test_register_successfully(client):
    res = client.post(
        "/register", 
        data=json.dumps({
            "email": "abc",
            "password": "abc"
        }),
        content_type="application/json"
    )

    response_body = json.loads(res.data)

    jwt_cookie = response_body.get('cookie')
    
    assert jwt_cookie is not None, "JWT cookie should be present"

def test_login_successfully(client):
    db.session.add(User(email="abc", password="52149649583e9b39894de20e85c9ae7b3a4c808b5db839b9d95222de2bf0343e38fe266d91dbed4a210f4648130b536a2da28827dcf1816d380b2baa2e364f72"))
    db.session.commit()

    res = client.post(
        "/login",
        data=json.dumps({
            "email": "abc",
            "password": "abc"
        }),
        content_type="application/json"
    )

    assert res.status_code == 200

    response_body = json.loads(res.data)

    jwt_cookie = response_body.get('cookie')
    
    assert jwt_cookie == 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFiYyJ9.qFxd6-caCY6tAj7I6xdCorTootTLa0NeLvFAk-5s4yE'
    
    