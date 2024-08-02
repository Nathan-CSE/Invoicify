import io
import json

from models import Invoice
from tests.fixtures import client, user, user_2, invoice, invoice_2, gui_invoice, gui_invoice_2
from tests.data import TEST_DATA
from tests.urls import (
    INVOICE_CREATE_PATH, 
    INVOICE_UPLOAD_CREATE_PATH, 
    INVOICE_UPLOAD_VALIDATE_PATH, 
    INVOICE_DELETE_PATH, 
    INVOICE_EDIT_PATH, 
    INVOICE_HISTORY_PATH, 
    INVOICE_SAVE_PATH, 
    INVOICE_SEND_PATH, 
    INVOICE_VALIDATE_PATH,
)

def test_invoice_creation_successful(client, user):
    res = client.post(
        INVOICE_CREATE_PATH,
        data=json.dumps(TEST_DATA["JSON"]),
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json",
        }
    )
    response_body = res.get_json()
    assert res.status_code == 201
    assert response_body["data"] == [{"filename": "test.xml", "invoiceId": 1}]
    

def test_invoice_creation_invalid(client, user):
    res = client.post(
        INVOICE_CREATE_PATH,
        data=json.dumps(TEST_DATA["INVALID_JSON"]),
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json",
        }
    )

    response_body = res.get_json()
    assert res.status_code == 400

def test_invoice_creation_unauthorised(client):
    res = client.post(
        INVOICE_CREATE_PATH,
        data=json.dumps(TEST_DATA["JSON"]),
        headers={
            "Authorisation": "blahaofsisja blah blah blah",
            "Content-Type": "application/json",
        }
    )

    assert res.status_code == 403

def test_invoice_save_successful(client, user):
    data = {
        "name": "Testing123",
        "fields": {
            "field 1": "hi"
        }
    }

    res = client.post(
        INVOICE_SAVE_PATH,
        data=json.dumps(data),
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 201
    assert len(Invoice.query.all()) > 0

def test_invoice_save_invalid_fields_type(client, user):
    data = {
        "name": "Testing123",
        # should be json
        "fields": "test"
    }

    res = client.post(
        INVOICE_SAVE_PATH,
        data=json.dumps(data),
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 400

def test_invoice_save_invalid_name_type(client, user):
    data = {
        # should be str
        "name": 5,
        "fields": {
            "field 1": "hi"
        }
    }

    res = client.post(
        INVOICE_SAVE_PATH,
        data=json.dumps(data),
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 400

def test_send_fail(client, user):
    data = {
        "xml_id": 1,
        "target_email": "test"
    }
    res = client.post(
        INVOICE_SEND_PATH,
        data = json.dumps(data),
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json"
        }
    )
    assert res.status_code == 400

def test_send_suc(client, user, invoice_2):
    res = client.post(
        f"{INVOICE_SEND_PATH}?xml_id={invoice_2.id}&target_email=",
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json"
        }
    )
    # if there is a successful email it would be 200 but I dont want to send emails for testing purposes.
    assert res.status_code == 200

def test_invoice_edit_successful(client, user, gui_invoice):
    data = {
        "name": "Testing123",
        "fields": TEST_DATA["JSON"],
        "rule": "AUNZ_PEPPOL_SB_1_0_10"
    }

    res = client.put(
        f"{INVOICE_EDIT_PATH}/{gui_invoice.id}",
        data=json.dumps(data),
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json"
        }
    )
    assert res.status_code == 204
    assert gui_invoice.name == "Testing123"
    assert gui_invoice.fields == {'ID': '1', 'IssueDate': '2024-06-25', 'InvoiceTypeCode': '380', 'Note': 'Taxinvoice', 'DocumentCurrencyCode': 'AUD', 'BuyerReference': 'test', 'AccountingSupplierParty': {'Party': {'EndpointID': {'schemeID': '0151', '@value': '47555222000'}, 'PartyName': {'Name': 'Windows to Fit Pty Ltd'}, 'PostalAddress': {'StreetName': 'Test', 'AdditionalStreetName': 'test', 'CityName': 'test', 'PostalZone': '2912', 'Country': {'IdentificationCode': 'AU'}}, 'PartyLegalEntity': {'RegistrationName': 'Windows to Fit Pty Ltd', 'CompanyID': {'schemeID': '0151', '@value': '47555222000'}}, 'PartyTaxScheme': {'CompanyID': '47555222000', 'TaxScheme': {'ID': 'GST'}}}}, 'AccountingCustomerParty': {'Party': {'EndpointID': {'schemeID': '0151', '@value': '47555222000'}, 'PartyName': {'Name': 'Henry Averies'}, 'PostalAddress': {'StreetName': 'Jam', 'AdditionalStreetName': 'a man', 'CityName': 'of fortune', 'PostalZone': '1994', 'Country': {'IdentificationCode': 'AU'}}, 'PartyLegalEntity': {'RegistrationName': 'Henry Averies', 'CompanyID': {'schemeID': '0151', '@value': '47555222000'}}, 'PartyTaxScheme': {'TaxScheme': {'CompanyID': '47555222000', 'ID': 'GST'}}}}, 'TaxTotal': {'TaxAmount': {'currencyID': 'AUD', '@value': '20'}, 'TaxSubtotal': {'TaxableAmount': {'currencyID': 'AUD', '@value': '100.0'}, 'TaxAmount': {'currencyID': 'AUD', '@value': '20'}, 'TaxCategory': {'ID': 'S', 'Percent': '20', 'TaxScheme': {'ID': 'GST'}}}}, 'LegalMonetaryTotal': {'LineExtensionAmount': {'currencyID': 'AUD', '@value': '900.0'}, 'TaxExclusiveAmount': {'currencyID': 'AUD', '@value': '900.0'}, 'TaxInclusiveAmount': {'currencyID': 'AUD', '@value': '1000.0'}, 'PayableAmount': {'currencyID': 'AUD', '@value': '1000.0'}}, 'InvoiceLine': {'ID': '0', 'InvoicedQuantity': {'unitCode': 'X01', '@value': '10'}, 'LineExtensionAmount': {'currencyID': 'AUD', '@value': '1000.0'}, 'Item': {'Description': 'Pirate', 'Name': 'Booty', 'ClassifiedTaxCategory': {'ID': 'GST', 'Percent': '10', 'TaxScheme': {'ID': 'GST'}}}, 'Price': {'PriceAmount': {'currencyID': 'AUD', '@value': '110.0'}}}}
    assert gui_invoice.rule == "AUNZ_PEPPOL_SB_1_0_10"
    assert gui_invoice.completed_ubl == None
    assert gui_invoice.is_gui == True
    assert gui_invoice.is_ready == False

def test_invoice_edit_invoice_does_not_exist(client, user):
    data = {
        "name": "Testing123",
        "fields": {
            "field 1": "hi"
        },
        "rule": "AUNZ_PEPPOL_1_0_10"
    }

    res = client.put(
        f"{INVOICE_EDIT_PATH}/1",
        data=json.dumps(data),
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 404

def test_invoice_edit_invoice_does_not_belong_to_user(client, user_2, invoice):
    data = {
        "name": "Testing123",
        "fields": {
            "field 1": "hi"
        },
        "rule": "AUNZ_PEPPOL_1_0_10"
    }

    res = client.put(
        f"{INVOICE_EDIT_PATH}/{invoice.id}",
        data=json.dumps(data),
        headers={
            "Authorisation": user_2.token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 404

def test_invoice_edit_invoice_resets_is_ready_and_completed_ubl_if_fields_or_rule_changes(client, user, gui_invoice_2):
    test_json_2 = TEST_DATA["JSON"]
    test_json_2["invoiceName"] = "Test invoice 2"

    data = {
        "name": "test-invoice",
        "fields": TEST_DATA["JSON"],
        "rule": "AUNZ_PEPPOL_1_0_10"
    }

    res = client.put(
        f"{INVOICE_EDIT_PATH}/{gui_invoice_2.id}",
        data=json.dumps(data),
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 204
    assert gui_invoice_2.completed_ubl == None
    assert gui_invoice_2.is_ready == False

    data = {
        "name": "test-invoice",
        "fields": test_json_2,
        "rule": "AUNZ_PEPPOL_SB_1_0_10"
    }

    res = client.put(
        f"{INVOICE_EDIT_PATH}/{gui_invoice_2.id}",
        data=json.dumps(data),
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 204
    assert gui_invoice_2.completed_ubl == None
    assert gui_invoice_2.is_ready == False

def test_invoice_delete_successful(client, user, invoice):
    res = client.delete(
        f"{INVOICE_DELETE_PATH}/{invoice.id}",
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200
    assert Invoice.query.filter(Invoice.id==invoice.id).first() == None

def test_invoice_delete_invoice_does_not_exist(client, user):
    res = client.delete(
        f"{INVOICE_DELETE_PATH}/1",
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 404

def test_invoice_delete_invoice_does_not_belong_to_user(client, user_2, invoice):
    res = client.delete(
        f"{INVOICE_DELETE_PATH}/{invoice.id}",
        headers={
            "Authorisation": user_2.token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 404

def test_invoice_history_successful(client, user, invoice):
    res = client.get(
        INVOICE_HISTORY_PATH,
        headers={
            "Authorisation": user.token,
        }
    )

    assert res.status_code == 200
    assert len(res.json) == 1

def test_invoice_history_successful_is_ready(client, user, invoice_2):
    res = client.get(
        f"{INVOICE_HISTORY_PATH}?is_ready=true",
        headers={
            "Authorisation": user.token,
        }
    )

    assert res.status_code == 200
    assert len(res.json) == 1

    res = client.get(
        f"{INVOICE_HISTORY_PATH}?is_ready=True",
        headers={
            "Authorisation": user.token,
        }
    )

    assert res.status_code == 200
    assert len(res.json) == 1

def test_invoice_history_successful_is_not_ready(client, user, invoice):
    res = client.get(
        f"{INVOICE_HISTORY_PATH}?is_ready=false",
        headers={
            "Authorisation": user.token,
        }
    )

    assert res.status_code == 200
    assert len(res.json) == 1

    res = client.get(
        f"{INVOICE_HISTORY_PATH}?is_ready=False",
        headers={
            "Authorisation": user.token,
        }
    )

    assert res.status_code == 200
    assert len(res.json) == 1

def test_invoice_history_only_returns_their_own_invoices(client, user, user_2, invoice, invoice_2):
    res = client.get(
        INVOICE_HISTORY_PATH,
        headers={
            "Authorisation": user.token,
        }
    )

    assert res.status_code == 200
    assert len(res.json) == 2

    res = client.get(
        INVOICE_HISTORY_PATH,
        headers={
            "Authorisation": user_2.token,
        }
    )

    assert res.status_code == 200
    assert len(res.json) == 0

def test_invoice_history_handles_invalid_query_param(client, user):
    res = client.get(
        f"{INVOICE_HISTORY_PATH}?is_ready=yo",
        headers={
            "Authorisation": user.token,
        }
    )

    assert res.status_code == 400
    

def test_validate_upload_success(client, user):
    data = {}
    data['rules'] = 'AUNZ_PEPPOL_1_0_10'
    data['files'] = [(io.BytesIO(TEST_DATA['GOOD_XML'].encode('UTF-8')),
        'test.xml')]
    res = client.post(
        INVOICE_UPLOAD_VALIDATE_PATH,
        headers={
            "Authorisation": user.token
        },
        data=data,  
        content_type='multipart/form-data',
        follow_redirects=True
    )
    response_body = res.get_json()
    
    assert res.status_code == 200
    assert response_body['validationOutcome'][0]['validated'] == True
    assert response_body['validationOutcome'][0]['invoiceId'] == 1
    

def test_validate_upload_fail_rules(client, user):
    data = {}
    data['rules'] = 'AUNZ_PEPPOL_SB_1_0_10'
    data['files'] = [(io.BytesIO(TEST_DATA['GOOD_XML'].encode('UTF-8')),
        'test.xml')]
    res = client.post(
        INVOICE_UPLOAD_VALIDATE_PATH,
        headers={
            "Authorisation": user.token
        },
        data=data,  
        content_type='multipart/form-data',
        follow_redirects=True
    )
    
    response_body = res.get_json()

    assert res.status_code == 200
    assert response_body['validationOutcome'][0]['validated'] == False
    assert response_body['validationOutcome'][0]['invoiceId'] == -1
    
 
def test_validate_upload_nonXML(client, user):
    data = {}
    data['files'] = [(io.BytesIO(b'fail, not xml'),
        'test.pdf')]
    data['rules'] = 'AUNZ_PEPPOL_1_0_10'
    res = client.post(
        INVOICE_UPLOAD_VALIDATE_PATH,
        headers={
            "Authorisation": user.token
        },
        data=data,  
        content_type='multipart/form-data',
        follow_redirects=True
    )
    response_body = res.get_json()

    assert res.status_code == 400
    assert response_body['message'] == "One or more of the files uploaded is not a XML, please upload XMLs only"
    
def test_validate_upload_unsucessful(client, user):
    data = {}
    data['files'] = [(io.BytesIO(TEST_DATA["BAD_XML"].encode('UTF-8')),
        'test.xml')]
    data['rules'] = 'AUNZ_PEPPOL_1_0_10'
    res = client.post(
        INVOICE_UPLOAD_VALIDATE_PATH,
        headers={
            "Authorisation": user.token
        },
        data=data,  
        content_type='multipart/form-data',
        follow_redirects=True
    )

    response_body = res.get_json()

    assert res.status_code == 200
    assert response_body['validationOutcome'][0]['invoiceId'] == -1
    assert response_body['validationOutcome'][0]['validated'] == False
    
def test_validate_upload_multiple_mixed_result(client, user):
    data = {}
    data['files'] = [(io.BytesIO(TEST_DATA['BAD_XML'].encode('UTF-8')),
        'test.xml'), (io.BytesIO(TEST_DATA['GOOD_XML'].encode('UTF-8')),
        'good.xml')]
    data['rules'] = 'AUNZ_PEPPOL_1_0_10'
    res = client.post(
        INVOICE_UPLOAD_VALIDATE_PATH,
        headers={
            "Authorisation": user.token
        },
        data=data,  
        content_type='multipart/form-data',
        follow_redirects=True
    )

    response_body = res.get_json()
    assert res.status_code == 200
    assert response_body['validationOutcome'][0]['validated'] == False
    assert response_body['validationOutcome'][0]['invoiceId'] == -1
    assert response_body['validationOutcome'][1]['validated'] == True
    assert response_body['validationOutcome'][1]['invoiceId'] == 1
    

def test_uploadcreate_json(client, user):
    data = {}
    data['files'] = [(io.BytesIO(TEST_DATA["JSON_STR_1"].encode("utf-8")), 'test.json')]

    res = client.post(
        INVOICE_UPLOAD_CREATE_PATH,
        headers={
            "Authorisation": user.token
        },
        data=data,  
        content_type='multipart/form-data',
        follow_redirects=True
    )

    response_body = res.get_json()
    assert res.status_code == 200
    assert response_body['message'] == "Invoice(s) created successfully"
    assert (len(response_body['data']) == 1)

# TODO: RE-ENABLE ON FINAL PUSH
# def test_uploadcreate_pdf(client, user):
#     data = {}
#     data['files'] = [(io.BytesIO(base64.b64decode(TEST_DATA["PDF_1"])), 'test.pdf')]

#     res = client.post(
#         INVOICE_UPLOAD_CREATE_PATH,
#         headers={
#             "Authorisation": user.token
#         },
#         data=data,  
#         content_type='multipart/form-data',
#         follow_redirects=True
#     )

#     response_body = res.get_json()
#     assert res.status_code == 200
#     assert response_body['message'] == "Invoice(s) created successfully"
#     assert (len(response_body['data']) == 1)
    

def test_uploadcreate_invalid_and_valid_json(client, user):
    data = {}
    data['files'] = [(io.BytesIO(TEST_DATA["JSON_STR_1"].encode("utf-8")), 'test.json'),(io.BytesIO(TEST_DATA["FAILED_JSON_STR_1"].encode("utf-8")), 'test.json')]

    res = client.post(
        INVOICE_UPLOAD_CREATE_PATH,
        headers={
            "Authorisation": user.token
        },
        data=data,  
        content_type='multipart/form-data',
        follow_redirects=True
    )
    
    response_body = res.get_json()
    assert res.status_code == 200
    assert response_body['message'] == "Invoice(s) created successfully"
    assert (len(response_body['data']) == 2)
    

def test_uploadcreate_invalidfile(client, user):
    data = {}
    data['files'] = [(io.BytesIO(b'fail, not pdf/json'),
        'test.txt')]

    res = client.post(
        INVOICE_UPLOAD_CREATE_PATH,
        headers={
            "Authorisation": user.token
        },
        data=data,  
        content_type='multipart/form-data',
        follow_redirects=True
    )
    
    response_body = res.get_json()
    assert res.status_code == 400
    assert response_body['message'] == "the file uploaded is not a pdf/json, please upload a valid file"
    
def test_uploadcreate_invalidjson(client, user):
    data = {}
    data['files'] = [(io.BytesIO(TEST_DATA["FAILED_JSON_STR_1"].encode("utf-8")), 'test.json')]
    
    res = client.post(
        INVOICE_UPLOAD_CREATE_PATH,
        headers={
            "Authorisation": user.token
        },
        data=data,  
        content_type='multipart/form-data',
        follow_redirects=True
    )

    response_body = res.get_json()
    assert res.status_code == 200
    assert response_body['message'] == "Invoice(s) created successfully"
    assert (len(response_body['data']) == 1)
    
def test_validate_id_successful(client, user, invoice):
    res = client.get(
        f"{INVOICE_VALIDATE_PATH}?id={invoice.id}&rules=AUNZ_PEPPOL_1_0_10",
        headers={
            "Authorisation": user.token
        },
        follow_redirects=True
    )

    response_body = res.get_json()
    assert res.status_code == 200
    assert response_body['validationOutcome'][0]['invoiceId'] == 1
    assert response_body['validationOutcome'][0]['validated'] == True

def test_validate_id_unsucessful(client,user,invoice_2):
    res = client.get(
        f"{INVOICE_VALIDATE_PATH}?id={invoice_2.id}&rules=AUNZ_PEPPOL_1_0_10",
        headers={
            "Authorisation": user.token
        },
        follow_redirects=True
    )

    response_body = res.get_json()
    assert res.status_code == 200
    assert response_body['validationOutcome'][0]['invoiceId'] == 1
    assert response_body['validationOutcome'][0]['validated'] == False

def test_validate_id_invalid_rule_fail(client,user,invoice):
    res = client.get(
        f"{INVOICE_VALIDATE_PATH}?id={invoice.id}&rules=BLAHBLAH",
        headers={
            "Authorisation": user.token
        },
        follow_redirects=True
    )

    assert res.status_code == 400

def test_validate_id_unsucessful_invoice_does_not_exist(client,user):
    res = client.get(
        f"{INVOICE_VALIDATE_PATH}?id=9999&rules=AUNZ_PEPPOL_1_0_10",
        headers={
            "Authorisation": user.token
        },
        follow_redirects=True
    )

    assert res.status_code == 400   


def test_validate_multiple_id(client,user, invoice, invoice_2):
    res = client.get(
        f"{INVOICE_VALIDATE_PATH}?id={invoice.id},{invoice_2.id}&rules=AUNZ_PEPPOL_1_0_10",
        headers={
            "Authorisation": user.token
        },
        follow_redirects=True
    )

    response_body = res.get_json()
    assert res.status_code == 200
    assert response_body['validationOutcome'][0]['invoiceId'] == 1
    assert response_body['validationOutcome'][0]['validated'] == True
    assert response_body['validationOutcome'][1]['invoiceId'] == 2
    assert response_body['validationOutcome'][1]['validated'] == False