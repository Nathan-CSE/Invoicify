import pytest
import json

from tests.fixtures import client
from models import db, User

def test_register_successfully(client):
    res = client.post(
        "/register", 
        data=json.dumps({
            "username": "abc",
            "password": "abc"
        }),
        content_type="application/json"
    )

    assert res.status_code == 201

def test_login_successfully(client):
    db.session.add(User(username="abc", password="52149649583e9b39894de20e85c9ae7b3a4c808b5db839b9d95222de2bf0343e38fe266d91dbed4a210f4648130b536a2da28827dcf1816d380b2baa2e364f72"))
    db.session.commit()

    res = client.post(
        "/login",
        data=json.dumps({
            "username": "abc",
            "password": "abc"
        }),
        content_type="application/json"
    )


    assert res.status_code == 200
