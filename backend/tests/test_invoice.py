import pytest
import json
import os

from werkzeug.datastructures import FileStorage

from tests.fixtures import client
from models import User
from src.services.create_xml import create_xml
from src.services.utils import db_insert, salt_and_hash

test_json = {
    "invoiceName": "test",
    "invoiceNumber": "1",
    "invoiceIssueDate": "2024-06-25",
    "seller": {
        "ABN": 47555222000,
        "companyName": "Windows to Fit Pty Ltd",
        "address": {
            "streetName": "Test",
            "additionalStreetName": "test",
            "cityName": "test",
            "postalCode": 2912,
            "country": "AU"
        }
    },
    "buyer": {
        "ABN": 47555222000,
        "companyName": "Henry Averies",
        "address": {
            "streetName": "Jam",
            "additionalStreetName": "a man",
            "cityName": "of fortune",
            "postalCode": 1994,
            "country": "AU"
        }
    },
    "invoiceItems": [{
        "quantity": 10,
        "unitCode": 1,
        "item": "Booty",
        "description": "Pirate",
        "unitPrice": 100.0,
        "GST": "GST",
        "totalPrice": 1000.0
    }],
    "totalGST": 100.0,
    "totalTaxable": 900.0,
    "totalAmount": 1000.0
}

INVOICE_CREATE_PATH = "/invoice/create"
INVOICE_UPLOAD_PATH = "/invoice/validatenewupload"

def test_invoice_creation_service(client):
    assert create_xml(test_json)["successful"] == True

def test_invoice_creation_successful(client):
    user_data = {
        "email": "abc@gmail.com", 
        "password": salt_and_hash("abc"), 
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFiY0BnbWFpbC5jb20ifQ.t5iNUNMkVVEVGNcPx8UdmwWgIMJ22j36xn4kXB-e-qM"
    }
    
    db_insert(User(**user_data))

    res = client.post(
        INVOICE_CREATE_PATH,
        data=json.dumps(test_json),
        headers={
            "Authorisation": user_data['token'],
            "Content-Type": "application/json",
        }
    )

    assert res.status_code == 201

def test_invoice_creation_unauthorised(client):
    res = client.post(
        INVOICE_CREATE_PATH,
        data=json.dumps(test_json),
        headers={
            "Authorisation": "blahaofsisja blah blah blah",
            "Content-Type": "application/json",
        }
    )

    assert res.status_code == 403
    
@pytest.fixture
def user(client):
    user = User(email="abc@gmail.com", password=salt_and_hash("abc"), token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFiY0BnbWFpbC5jb20ifQ.t5iNUNMkVVEVGNcPx8UdmwWgIMJ22j36xn4kXB-e-qM")
    
    db_insert(user)
    return user

def test_validate_success(client, user):
    data = {}
    file = FileStorage(
        stream=open("auinvoice.xml", "rb"),
        filename="auinvoice.xml",
        content_type="application/xml",
    )
    data['files'] = [file]
    res = client.post(
        INVOICE_UPLOAD_PATH,
        headers={
            "Authorisation": user.token
        },
        data=data,  
        content_type='multipart/form-data',
        follow_redirects=True
    )
    response_body = res.get_json()

    assert res.status_code == 200
    assert response_body['message'] == 'XMLs created'