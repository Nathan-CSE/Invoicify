import base64
import io
import json

from models import Invoice
from tests.fixtures import client, user, user_2, invoice, invoice_2, gui_invoice, gui_invoice_2
from tests.data import TEST_DATA
from tests.urls import (
    INVOICE_CREATE_PATH,
    INVOICE_DOWNLOAD_PATH, 
    INVOICE_UPLOAD_CREATE_PATH, 
    INVOICE_UPLOAD_VALIDATE_PATH, 
    INVOICE_DELETE_PATH, 
    INVOICE_EDIT_PATH, 
    INVOICE_HISTORY_PATH, 
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
        f"{INVOICE_SEND_PATH}?xml_id={invoice_2.id}&target_email=TEST",
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
    assert gui_invoice.fields == {'ID': '1', 'IssueDate': '2024-06-25', 'InvoiceTypeCode': '380', 'Note': 'Taxinvoice', 'DocumentCurrencyCode': 'AUD', 'BuyerReference': 'test', 'AccountingSupplierParty': {'Party': {'EndpointID': {'schemeID': '0151', '@value': '47555222000'}, 'PartyName': {'Name': 'Windows to Fit Pty Ltd'}, 'PostalAddress': {'StreetName': 'Test', 'AdditionalStreetName': 'test', 'CityName': 'test', 'PostalZone': '2912', 'Country': {'IdentificationCode': 'AU'}}, 'PartyLegalEntity': {'RegistrationName': 'Windows to Fit Pty Ltd', 'CompanyID': {'schemeID': '0151', '@value': '47555222000'}}, 'PartyTaxScheme': {'CompanyID': '47555222000', 'TaxScheme': {'ID': 'GST'}}}}, 'AccountingCustomerParty': {'Party': {'EndpointID': {'schemeID': '0151', '@value': '47555222000'}, 'PartyName': {'Name': 'Henry Averies'}, 'PostalAddress': {'StreetName': 'Jam', 'AdditionalStreetName': 'a man', 'CityName': 'of fortune', 'PostalZone': '1994', 'Country': {'IdentificationCode': 'AU'}}, 'PartyLegalEntity': {'RegistrationName': 'Henry Averies', 'CompanyID': {'schemeID': '0151', '@value': '47555222000'}}, 'PartyTaxScheme': {'TaxScheme': {'CompanyID': '47555222000', 'ID': 'GST'}}}}, 'TaxTotal': {'TaxAmount': {'currencyID': 'AUD', '@value': '10'}, 'TaxSubtotal': {'TaxableAmount': {'currencyID': 'AUD', '@value': '100'}, 'TaxAmount': {'currencyID': 'AUD', '@value': '10'}, 'TaxCategory': {'ID': 'S', 'Percent': '10', 'TaxScheme': {'ID': 'GST'}}}}, 'LegalMonetaryTotal': {'LineExtensionAmount': {'currencyID': 'AUD', '@value': '1000'}, 'TaxExclusiveAmount': {'currencyID': 'AUD', '@value': '1000'}, 'TaxInclusiveAmount': {'currencyID': 'AUD', '@value': '1100'}, 'PayableAmount': {'currencyID': 'AUD', '@value': '1100'}}, 'InvoiceLine': {'ID': '0', 'InvoicedQuantity': {'unitCode': 'X01', '@value': '10'}, 'LineExtensionAmount': {'currencyID': 'AUD', '@value': '1100'}, 'Item': {'Description': 'Pirate', 'Name': 'Booty', 'ClassifiedTaxCategory': {'ID': 'GST', 'Percent': '10', 'TaxScheme': {'ID': 'GST'}}}, 'Price': {'PriceAmount': {'currencyID': 'AUD', '@value': '110'}}}}
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
    
def test_download(client, user, invoice):
    res = client.post(
        f"{INVOICE_DOWNLOAD_PATH}/{invoice.id}",
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json",
        }
    )
    assert res.status_code == 200
    assert res.json["message"] == '<?xml version="1.0" encoding="UTF-8"?><Invoice xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"><cbc:CustomizationID>urn:cen.eu:en16931:2017#conformant#urn:fdc:peppol.eu:2017:poacc:billing:international:aunz:3.0</cbc:CustomizationID><cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID><cbc:ID>Invoice03</cbc:ID><cbc:IssueDate>2022-07-31</cbc:IssueDate><cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode><cbc:Note>Adjustment note to reverse prior bill Invoice01. Free text field can bring attention to reason for credit etc.</cbc:Note><cbc:DocumentCurrencyCode>AUD</cbc:DocumentCurrencyCode><cbc:BuyerReference>Simple solar plan</cbc:BuyerReference><cac:InvoicePeriod><cbc:StartDate>2022-06-15</cbc:StartDate><cbc:EndDate>2022-07-15</cbc:EndDate></cac:InvoicePeriod><cac:BillingReference><cac:InvoiceDocumentReference><cbc:ID>Invoice01</cbc:ID><cbc:IssueDate>2022-07-29</cbc:IssueDate></cac:InvoiceDocumentReference></cac:BillingReference><cac:AdditionalDocumentReference><cbc:ID>Invoice03.pdf</cbc:ID><cac:Attachment><cbc:EmbeddedDocumentBinaryObject mimeCode="application/pdf" filename="Invoice03.pdf">UGxhaW4gdGV4dCBpbiBwbGFjZSBvZiBwZGYgYXR0YWNobWVudCBmb3Igc2FtcGxlIGludm9pY2Vz</cbc:EmbeddedDocumentBinaryObject></cac:Attachment></cac:AdditionalDocumentReference><cac:AccountingSupplierParty><cac:Party><cbc:EndpointID schemeID="0151">47555222000</cbc:EndpointID><cac:PostalAddress><cbc:CityName>Harrison</cbc:CityName><cbc:PostalZone>2912</cbc:PostalZone><cbc:CountrySubentity>NSW</cbc:CountrySubentity><cac:Country><cbc:IdentificationCode>AU</cbc:IdentificationCode></cac:Country></cac:PostalAddress><cac:PartyLegalEntity><cbc:RegistrationName>Grey Roo Energy</cbc:RegistrationName><cbc:CompanyID schemeID="0151">47555222000</cbc:CompanyID></cac:PartyLegalEntity></cac:Party></cac:AccountingSupplierParty><cac:AccountingCustomerParty><cac:Party><cbc:EndpointID schemeID="0151">47555222000</cbc:EndpointID><cac:PartyIdentification><cbc:ID>AccountNumber123</cbc:ID></cac:PartyIdentification><cac:PostalAddress><cbc:StreetName>100 Queen Street</cbc:StreetName><cbc:CityName>Sydney</cbc:CityName><cbc:PostalZone>2000</cbc:PostalZone><cbc:CountrySubentity>NSW</cbc:CountrySubentity><cac:Country><cbc:IdentificationCode>AU</cbc:IdentificationCode></cac:Country></cac:PostalAddress><cac:PartyLegalEntity><cbc:RegistrationName>Trotters Incorporated</cbc:RegistrationName><cbc:CompanyID schemeID="0151">91888222000</cbc:CompanyID></cac:PartyLegalEntity><cac:Contact><cbc:Name>Lisa Johnson</cbc:Name></cac:Contact></cac:Party></cac:AccountingCustomerParty><cac:TaxTotal><cbc:TaxAmount currencyID="AUD">-15.94</cbc:TaxAmount><cac:TaxSubtotal><cbc:TaxableAmount currencyID="AUD">-159.43</cbc:TaxableAmount><cbc:TaxAmount currencyID="AUD">-15.94</cbc:TaxAmount><cac:TaxCategory><cbc:ID>S</cbc:ID><cbc:Percent>10</cbc:Percent><cac:TaxScheme><cbc:ID>GST</cbc:ID></cac:TaxScheme></cac:TaxCategory></cac:TaxSubtotal></cac:TaxTotal><cac:LegalMonetaryTotal><cbc:LineExtensionAmount currencyID="AUD">-159.43</cbc:LineExtensionAmount><cbc:TaxExclusiveAmount currencyID="AUD">-159.43</cbc:TaxExclusiveAmount><cbc:TaxInclusiveAmount currencyID="AUD">-175.37</cbc:TaxInclusiveAmount><cbc:PayableAmount currencyID="AUD">-175.37</cbc:PayableAmount></cac:LegalMonetaryTotal><cac:InvoiceLine><cbc:ID>1</cbc:ID><cbc:InvoicedQuantity unitCode="KWH">-325.2</cbc:InvoicedQuantity><cbc:LineExtensionAmount currencyID="AUD">-129.04</cbc:LineExtensionAmount><cac:Item><cbc:Name>Adjustment - reverse prior Electricity charges - all day rate NMI 9000074677</cbc:Name><cac:ClassifiedTaxCategory><cbc:ID>S</cbc:ID><cbc:Percent>10</cbc:Percent><cac:TaxScheme><cbc:ID>GST</cbc:ID></cac:TaxScheme></cac:ClassifiedTaxCategory></cac:Item><cac:Price><cbc:PriceAmount currencyID="AUD">0.3968</cbc:PriceAmount></cac:Price></cac:InvoiceLine><cac:InvoiceLine><cbc:ID>2</cbc:ID><cbc:InvoicedQuantity unitCode="DAY">-31</cbc:InvoicedQuantity><cbc:LineExtensionAmount currencyID="AUD">-30.39</cbc:LineExtensionAmount><cac:Item><cbc:Name>Adjustment - reverse prior Supply charge</cbc:Name><cac:ClassifiedTaxCategory><cbc:ID>S</cbc:ID><cbc:Percent>10</cbc:Percent><cac:TaxScheme><cbc:ID>GST</cbc:ID></cac:TaxScheme></cac:ClassifiedTaxCategory></cac:Item><cac:Price><cbc:PriceAmount currencyID="AUD">0.9803</cbc:PriceAmount></cac:Price></cac:InvoiceLine></Invoice>'

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

def test_uploadcreate_pdf(client, user):
    data = {}
    data['files'] = [(io.BytesIO(base64.b64decode(TEST_DATA["PDF_1"])), 'test.pdf')]

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