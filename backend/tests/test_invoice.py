import pytest
import json
from src.services.create_xml import create_xml
from tests.fixtures import client

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
            "postalCode": "1994",
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

def test_invoice_creation(client):
    assert create_xml(test_json)["successful"] == True