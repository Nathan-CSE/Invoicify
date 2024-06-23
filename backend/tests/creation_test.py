import pytest
import json

from tests.fixtures import client

INVOICE_CREATION_PATH: "/invoiceCreation/gui"

def test_gui_to_xml_success(client):
    data = {
        "seller_company_name": "Example Company",
        "seller_abn": "1234567890",
        "seller_street_name": "Example",
        "seller_city_name": "Sydney",
        "seller_postal_code": "2000",
        "seller_country": "Australia",
        "seller_tax_scheme": "GST",

        "customer_company_name": "Customer Co.",
        "customer_abn": "9876543210",
        "customer_street_name": "Customer",
        "customer_city_name": "Melbourne",
        "customer_postal_code": "3000",
        "customer_country": "Australia",
        "customer_tax_scheme": "GST",

        "taxed_amount": 130,   
        "taxable_amount": 160,

        "items": [
            {"quantity": 1, "unit_code": "ABC", "item_name": "Item 1", "description": "Description 1", "price": 100},
            {"quantity": 2, "unit_code": "DEF", "item_name": "Item 2", "description": "Description 2", "price": 200}
        ]
    }
  
    res = client.post(
        INVOICE_CREATION_PATH,
        data=json.dumps(data),
        content_type="application/json"
    )
  
    assert res.status_code == 201

def test_gui_to_xml_missing_multiple_fields(client):
    data = {
        "seller_company_name": "Example Company",
        "seller_street_name": "Example",
        "seller_city_name": "Sydney",
        "seller_postal_code": "2000",
        "seller_country": "Australia",
        "seller_tax_scheme": "GST",

        "customer_company_name": "Customer Co.",
        "customer_abn": "9876543210",
        "customer_city_name": "Melbourne",
        "customer_postal_code": "3000",
        "customer_country": "Australia",
        "customer_tax_scheme": "GST",
 
        "taxable_amount": 160,

        "items": [
            {"quantity": 1, "unit_code": "ABC", "item_name": "Item 1", "description": "Description 1", "price": 100},
            {"quantity": 2, "unit_code": "DEF", "item_name": "Item 2", "description": "Description 2", "price": 200}
        ]
    }
  
    res = client.post(
        INVOICE_CREATION_PATH,
        data=json.dumps(data),
        content_type="application/json"
    )
  
    assert res.status_code == 400

def test_gui_to_xml_missing_one_field(client):
    data = {
        "seller_abn": "1234567890",
        "seller_street_name": "Example",
        "seller_city_name": "Sydney",
        "seller_postal_code": "2000",
        "seller_country": "Australia",
        "seller_tax_scheme": "GST",

        "customer_company_name": "Customer Co.",
        "customer_abn": "9876543210",
        "customer_street_name": "Customer",
        "customer_city_name": "Melbourne",
        "customer_postal_code": "3000",
        "customer_country": "Australia",
        "customer_tax_scheme": "GST",

        "taxed_amount": 130,   
        "taxable_amount": 160,

        "items": [
            {"quantity": 1, "unit_code": "ABC", "item_name": "Item 1", "description": "Description 1", "price": 100},
            {"quantity": 2, "unit_code": "DEF", "item_name": "Item 2", "description": "Description 2", "price": 200}
        ]
    }
  
    res = client.post(
        INVOICE_CREATION_PATH,
        data=json.dumps(data),
        content_type="application/json"
    )
  
    assert res.status_code == 400

def test_gui_to_xml_missing_all_fields(client):
    data = {}
  
    res = client.post(
        INVOICE_CREATION_PATH,
        data=json.dumps(data),
        content_type="application/json"
    )
  
    assert res.status_code == 400

def test_gui_to_xml_extra_fields(client):
    data = {
        "seller_abn": "1234567890",
        "seller_street_name": "Example",
        "seller_city_name": "Sydney",
        "seller_postal_code": "2000",
        "seller_country": "Australia",
        "seller_tax_scheme": "GST",
        "seller_account_details": "132-565",

        "customer_company_name": "Customer Co.",
        "customer_abn": "9876543210",
        "customer_street_name": "Customer",
        "customer_city_name": "Melbourne",
        "customer_postal_code": "3000",
        "customer_country": "Australia",
        "customer_tax_scheme": "GST",
        "customer_deadline": "23-01-2025",

        "taxed_amount": 130,   
        "taxable_amount": 160,

        "items": [
            {"quantity": 1, "unit_code": "ABC", "item_name": "Item 1", "description": "Description 1", "price": 100},
            {"quantity": 2, "unit_code": "DEF", "item_name": "Item 2", "description": "Description 2", "price": 200}
        ]
    }
  
    res = client.post(
        INVOICE_CREATION_PATH,
        data=json.dumps(data),
        content_type="application/json"
    )
  
    assert res.status_code == 400