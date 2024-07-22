import io
import json

from models import User, Invoice
from src.services.utils import db_insert, salt_and_hash
from tests.fixtures import client, user, user_2, invoice, invoice_2
from tests.data import TEST_DATA

test_json = {
    "invoiceName": "test",
    "invoiceNumber": 1,
    "invoiceIssueDate": "2024-06-25",
    "seller": {
        "ABN": 47555222000,
        "companyName": "Windows to Fit Pty Ltd",
        "address": {
            "streetName": "Test",
            "additionalStreetName": "test",
            "cityName": "test",
            "postalCode": "2912",
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
        "unitCode": "X01",
        "item": "Booty",
        "description": "Pirate",
        "unitPrice": 100.0,
        "GST": 10,
        "totalPrice": 1000.0
    }],
    "totalGST": 100.0,
    "totalTaxable": 900.0,
    "totalAmount": 1000.0
}

test_invalid_json = {
    "invoiceName": "test",
    "invoiceNumber": "1",
    "invoiceIssueDate": "2024-06-25",
    "seller": {
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
        "unitCode": "X01",
        "item": "Booty",
        "description": "Pirate",
        "unitPrice": 100.0,
        "GST": 10,
        "totalPrice": 1000.0
    }],
    "totalGST": 100.0,
    "totalTaxable": 900.0,
    "totalAmount": 1000.0
}

INVOICE_CREATE_PATH = "/invoice/create"
INVOICE_UPLOAD_VALIDATE_PATH = "/invoice/uploadValidate"
INVOICE_UPLOAD_CREATE_PATH = "/invoice/uploadCreate"
INVOICE_SAVE_PATH = "/invoice/save"
INVOICE_EDIT_PATH = "/invoice/edit"
INVOICE_DELETE_PATH = "/invoice/delete"
INVOICE_HISTORY_PATH = "/invoice/history"

def test_invoice_creation_successful(client, user):
    res = client.post(
        INVOICE_CREATE_PATH,
        data=json.dumps(test_json),
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
        data=json.dumps(test_json),
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json",
        }
    )

    response_body = res.get_json()
    assert res.status_code == 201
    assert response_body["data"] == [{"filename": "test.xml", "invoiceId": 1}]

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

def test_invoice_edit_successful(client, user, invoice):
    data = {
        "name": "Testing123",
        "fields": {
            "field 1": "hi"
        },
        "rule": "AUNZ_PEPPOL_SB_1_0_10"
    }

    res = client.put(
        f"{INVOICE_EDIT_PATH}/{invoice.id}",
        data=json.dumps(data),
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 204
    assert invoice.name == "Testing123"
    assert invoice.fields == {
        "field 1": "hi"
    }
    assert invoice.rule == "AUNZ_PEPPOL_SB_1_0_10"
    assert invoice.completed_ubl == None
    assert invoice.is_ready == False

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

def test_invoice_edit_invoice_resets_is_ready_and_completed_ubl_if_fields_or_rule_changes(client, user, invoice_2):
    data = {
        "name": "test-invoice",
        "fields": {
            "field 1": "hi"
        },
        "rule": "AUNZ_PEPPOL_1_0_10"
    }

    res = client.put(
        f"{INVOICE_EDIT_PATH}/{invoice_2.id}",
        data=json.dumps(data),
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 204
    assert invoice_2.completed_ubl == None
    assert invoice_2.is_ready == False

    data = {
        "name": "test-invoice",
        "fields": {
            "yo": "Yo"
        },
        "rule": "AUNZ_PEPPOL_SB_1_0_10"
    }

    res = client.put(
        f"{INVOICE_EDIT_PATH}/{invoice_2.id}",
        data=json.dumps(data),
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 204
    assert invoice_2.completed_ubl == None
    assert invoice_2.is_ready == False

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
    data['files'] = [(io.BytesIO(b'''<?xml version="1.0" encoding="UTF-8"?>
        <!-- Example of a simple invoice with 'mixed' taxable and non-taxable supplies including a non-taxable solar rebate (e.g. micro-business not registered for GST) -->
        <Invoice xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2">
            <cbc:CustomizationID>urn:cen.eu:en16931:2017#conformant#urn:fdc:peppol.eu:2017:poacc:billing:international:aunz:3.0</cbc:CustomizationID>
            <cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID>
            <cbc:ID>Invoice01</cbc:ID>
            <cbc:IssueDate>2022-07-29</cbc:IssueDate>
            <cbc:DueDate>2022-08-30</cbc:DueDate>
            <cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
            <cbc:Note>Tax invoice. Please note you have $384.24 OVERDUE from prior bills.</cbc:Note> <!-- Free text field can bring attention to prior unpaid amount etc. -->
            <cbc:DocumentCurrencyCode>AUD</cbc:DocumentCurrencyCode>
            <cbc:BuyerReference>Simple solar plan</cbc:BuyerReference> <!-- Purchase Order and/or Buyer Reference MUST be provided -->
            <cac:InvoicePeriod>
                <!-- Period is optional at the invoice and line levels -->
                <cbc:StartDate>2022-06-15</cbc:StartDate>
                <cbc:EndDate>2022-07-15</cbc:EndDate>
            </cac:InvoicePeriod>
            <cac:AdditionalDocumentReference>
                <!-- Multiple attachments and external links may optionally be included -->
                <cbc:ID>Invoice01.pdf</cbc:ID>
                <cac:Attachment>
                    <!-- For brevity, this sample Attachment is not representative of an embedded pdf -->
                    <cbc:EmbeddedDocumentBinaryObject mimeCode="application/pdf" filename="Invoice01.pdf">UGxhaW4gdGV4dCBpbiBwbGFjZSBvZiBwZGYgYXR0YWNobWVudCBmb3Igc2FtcGxlIGludm9pY2Vz</cbc:EmbeddedDocumentBinaryObject>
                </cac:Attachment>
            </cac:AdditionalDocumentReference>
            <cac:AccountingSupplierParty>
                <!-- Seller details -->
                <cac:Party>
                    <cbc:EndpointID schemeID="0151">47555222000</cbc:EndpointID> <!-- Seller 'Peppol ID' -->
                    <cac:PostalAddress>
                        <cbc:CityName>Harrison</cbc:CityName>
                        <cbc:PostalZone>2912</cbc:PostalZone>
                        <cbc:CountrySubentity>NSW</cbc:CountrySubentity>
                        <cac:Country>
                            <cbc:IdentificationCode>AU</cbc:IdentificationCode>
                        </cac:Country>
                    </cac:PostalAddress>
                    <cac:PartyLegalEntity>
                        <cbc:RegistrationName>Grey Roo Energy</cbc:RegistrationName>
                        <cbc:CompanyID schemeID="0151">47555222000</cbc:CompanyID> <!-- Seller ABN -->
                    </cac:PartyLegalEntity>
                </cac:Party>
            </cac:AccountingSupplierParty>
            <cac:AccountingCustomerParty>
                <!-- Buyer/customer details -->
                <cac:Party>
                    <cbc:EndpointID schemeID="0151">91888222000</cbc:EndpointID> <!-- Buyer/customer 'Peppol ID' -->
                    <cac:PartyIdentification>
                        <cbc:ID>AccountNumber123</cbc:ID> <!-- Buyer/customer account number, assigned by the supplier -->
                    </cac:PartyIdentification>
                    <cac:PostalAddress>
                        <cbc:StreetName>100 Queen Street</cbc:StreetName>
                        <cbc:CityName>Sydney</cbc:CityName>
                        <cbc:PostalZone>2000</cbc:PostalZone>
                        <cbc:CountrySubentity>NSW</cbc:CountrySubentity>
                        <cac:Country>
                            <cbc:IdentificationCode>AU</cbc:IdentificationCode>
                        </cac:Country>
                    </cac:PostalAddress>
                    <cac:PartyLegalEntity>
                        <cbc:RegistrationName>Trotters Incorporated</cbc:RegistrationName>
                        <cbc:CompanyID schemeID="0151">91888222000</cbc:CompanyID> <!-- Buyer/customer ABN -->
                    </cac:PartyLegalEntity>
                    <cac:Contact>
                        <cbc:Name>Lisa Johnson</cbc:Name>
                    </cac:Contact>
                </cac:Party>
            </cac:AccountingCustomerParty>
            <cac:TaxTotal>
                <cbc:TaxAmount currencyID="AUD">15.94</cbc:TaxAmount>
                <cac:TaxSubtotal>
                    <!-- Subtotal for 'S' Standard-rated tax category of 10% GST -->
                    <cbc:TaxableAmount currencyID="AUD">159.43</cbc:TaxableAmount>
                    <cbc:TaxAmount currencyID="AUD">15.94</cbc:TaxAmount>
                    <cac:TaxCategory>
                        <cbc:ID>S</cbc:ID>
                        <cbc:Percent>10</cbc:Percent>
                        <cac:TaxScheme>
                            <cbc:ID>GST</cbc:ID>
                        </cac:TaxScheme>
                    </cac:TaxCategory>
                </cac:TaxSubtotal>
                <cac:TaxSubtotal>
                    <!-- Subtotal for 'Z' Zero-rated tax category of 0% GST -->
                    <cbc:TaxableAmount currencyID="AUD">-13.5</cbc:TaxableAmount>
                    <cbc:TaxAmount currencyID="AUD">0.00</cbc:TaxAmount>
                    <cac:TaxCategory>
                        <cbc:ID>Z</cbc:ID>
                        <cbc:Percent>0</cbc:Percent>
                        <cac:TaxScheme>
                            <cbc:ID>GST</cbc:ID>
                        </cac:TaxScheme>
                    </cac:TaxCategory>
                </cac:TaxSubtotal>
            </cac:TaxTotal>
            <cac:LegalMonetaryTotal>
                <cbc:LineExtensionAmount currencyID="AUD">145.93</cbc:LineExtensionAmount>
                <cbc:TaxExclusiveAmount currencyID="AUD">145.93</cbc:TaxExclusiveAmount>
                <cbc:TaxInclusiveAmount currencyID="AUD">161.87</cbc:TaxInclusiveAmount>
                <cbc:PayableAmount currencyID="AUD">161.87</cbc:PayableAmount> <!-- New charges invoiced (excluding prior unpaid amount) -->
            </cac:LegalMonetaryTotal>
            <cac:InvoiceLine>
                <!-- Line with 10% GST -->
                <cbc:ID>1</cbc:ID>
                <cbc:InvoicedQuantity unitCode="KWH">325.2</cbc:InvoicedQuantity>
                <cbc:LineExtensionAmount currencyID="AUD">129.04</cbc:LineExtensionAmount>
                <cac:Item>
                    <cbc:Name>Electricity charges - all day rate NMI 9000074677</cbc:Name>
                    <cac:ClassifiedTaxCategory>
                        <cbc:ID>S</cbc:ID>
                        <cbc:Percent>10</cbc:Percent> <!-- 10% GST -->
                        <cac:TaxScheme>
                            <cbc:ID>GST</cbc:ID>
                        </cac:TaxScheme>
                    </cac:ClassifiedTaxCategory>
                </cac:Item>
                <cac:Price>
                    <cbc:PriceAmount currencyID="AUD">0.3968</cbc:PriceAmount>
                </cac:Price>
            </cac:InvoiceLine>
            <cac:InvoiceLine>
                <!-- Line with credit value and zero GST -->
                <cbc:ID>2</cbc:ID>
                <cbc:InvoicedQuantity unitCode="KWH">-150</cbc:InvoicedQuantity>
                <cbc:LineExtensionAmount currencyID="AUD">-13.5</cbc:LineExtensionAmount>
                <cac:Item>
                    <cbc:Name>Solar feed-in rebate NMI 9000074677</cbc:Name>
                    <cac:ClassifiedTaxCategory>
                        <cbc:ID>Z</cbc:ID>
                        <cbc:Percent>0</cbc:Percent> <!-- 0% GST -->
                        <cac:TaxScheme>
                            <cbc:ID>GST</cbc:ID>
                        </cac:TaxScheme>
                    </cac:ClassifiedTaxCategory>
                </cac:Item>
                <cac:Price>
                    <cbc:PriceAmount currencyID="AUD">0.09</cbc:PriceAmount>
                </cac:Price>
            </cac:InvoiceLine>
            <cac:InvoiceLine>
                <!-- Line with 10% GST -->
                <cbc:ID>3</cbc:ID>
                <cbc:InvoicedQuantity unitCode="DAY">31</cbc:InvoicedQuantity>
                <cbc:LineExtensionAmount currencyID="AUD">30.39</cbc:LineExtensionAmount>
                <cac:Item>
                    <cbc:Name>Supply charge</cbc:Name>
                    <cac:ClassifiedTaxCategory>
                        <cbc:ID>S</cbc:ID>
                        <cbc:Percent>10</cbc:Percent> <!-- 10% GST -->
                        <cac:TaxScheme>
                            <cbc:ID>GST</cbc:ID>
                        </cac:TaxScheme>
                    </cac:ClassifiedTaxCategory>
                </cac:Item>
                <cac:Price>
                    <cbc:PriceAmount currencyID="AUD">0.9803</cbc:PriceAmount>
                </cac:Price>
            </cac:InvoiceLine>
        </Invoice>
        '''),
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
    assert response_body['message'] == "Invoice validated sucessfully"
    

def test_validate_upload_fail_rules(client, user):
    data = {}
    data['rules'] = 'AUNZ_PEPPOL_SB_1_0_10'
    data['files'] = [(io.BytesIO(b'''<?xml version="1.0" encoding="UTF-8"?>
        <!-- Example of a simple invoice with 'mixed' taxable and non-taxable supplies including a non-taxable solar rebate (e.g. micro-business not registered for GST) -->
        <Invoice xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2">
            <cbc:CustomizationID>urn:cen.eu:en16931:2017#conformant#urn:fdc:peppol.eu:2017:poacc:billing:international:aunz:3.0</cbc:CustomizationID>
            <cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID>
            <cbc:ID>Invoice01</cbc:ID>
            <cbc:IssueDate>2022-07-29</cbc:IssueDate>
            <cbc:DueDate>2022-08-30</cbc:DueDate>
            <cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
            <cbc:Note>Tax invoice. Please note you have $384.24 OVERDUE from prior bills.</cbc:Note> <!-- Free text field can bring attention to prior unpaid amount etc. -->
            <cbc:DocumentCurrencyCode>AUD</cbc:DocumentCurrencyCode>
            <cbc:BuyerReference>Simple solar plan</cbc:BuyerReference> <!-- Purchase Order and/or Buyer Reference MUST be provided -->
            <cac:InvoicePeriod>
                <!-- Period is optional at the invoice and line levels -->
                <cbc:StartDate>2022-06-15</cbc:StartDate>
                <cbc:EndDate>2022-07-15</cbc:EndDate>
            </cac:InvoicePeriod>
            <cac:AdditionalDocumentReference>
                <!-- Multiple attachments and external links may optionally be included -->
                <cbc:ID>Invoice01.pdf</cbc:ID>
                <cac:Attachment>
                    <!-- For brevity, this sample Attachment is not representative of an embedded pdf -->
                    <cbc:EmbeddedDocumentBinaryObject mimeCode="application/pdf" filename="Invoice01.pdf">UGxhaW4gdGV4dCBpbiBwbGFjZSBvZiBwZGYgYXR0YWNobWVudCBmb3Igc2FtcGxlIGludm9pY2Vz</cbc:EmbeddedDocumentBinaryObject>
                </cac:Attachment>
            </cac:AdditionalDocumentReference>
            <cac:AccountingSupplierParty>
                <!-- Seller details -->
                <cac:Party>
                    <cbc:EndpointID schemeID="0151">47555222000</cbc:EndpointID> <!-- Seller 'Peppol ID' -->
                    <cac:PostalAddress>
                        <cbc:CityName>Harrison</cbc:CityName>
                        <cbc:PostalZone>2912</cbc:PostalZone>
                        <cbc:CountrySubentity>NSW</cbc:CountrySubentity>
                        <cac:Country>
                            <cbc:IdentificationCode>AU</cbc:IdentificationCode>
                        </cac:Country>
                    </cac:PostalAddress>
                    <cac:PartyLegalEntity>
                        <cbc:RegistrationName>Grey Roo Energy</cbc:RegistrationName>
                        <cbc:CompanyID schemeID="0151">47555222000</cbc:CompanyID> <!-- Seller ABN -->
                    </cac:PartyLegalEntity>
                </cac:Party>
            </cac:AccountingSupplierParty>
            <cac:AccountingCustomerParty>
                <!-- Buyer/customer details -->
                <cac:Party>
                    <cbc:EndpointID schemeID="0151">91888222000</cbc:EndpointID> <!-- Buyer/customer 'Peppol ID' -->
                    <cac:PartyIdentification>
                        <cbc:ID>AccountNumber123</cbc:ID> <!-- Buyer/customer account number, assigned by the supplier -->
                    </cac:PartyIdentification>
                    <cac:PostalAddress>
                        <cbc:StreetName>100 Queen Street</cbc:StreetName>
                        <cbc:CityName>Sydney</cbc:CityName>
                        <cbc:PostalZone>2000</cbc:PostalZone>
                        <cbc:CountrySubentity>NSW</cbc:CountrySubentity>
                        <cac:Country>
                            <cbc:IdentificationCode>AU</cbc:IdentificationCode>
                        </cac:Country>
                    </cac:PostalAddress>
                    <cac:PartyLegalEntity>
                        <cbc:RegistrationName>Trotters Incorporated</cbc:RegistrationName>
                        <cbc:CompanyID schemeID="0151">91888222000</cbc:CompanyID> <!-- Buyer/customer ABN -->
                    </cac:PartyLegalEntity>
                    <cac:Contact>
                        <cbc:Name>Lisa Johnson</cbc:Name>
                    </cac:Contact>
                </cac:Party>
            </cac:AccountingCustomerParty>
            <cac:TaxTotal>
                <cbc:TaxAmount currencyID="AUD">15.94</cbc:TaxAmount>
                <cac:TaxSubtotal>
                    <!-- Subtotal for 'S' Standard-rated tax category of 10% GST -->
                    <cbc:TaxableAmount currencyID="AUD">159.43</cbc:TaxableAmount>
                    <cbc:TaxAmount currencyID="AUD">15.94</cbc:TaxAmount>
                    <cac:TaxCategory>
                        <cbc:ID>S</cbc:ID>
                        <cbc:Percent>10</cbc:Percent>
                        <cac:TaxScheme>
                            <cbc:ID>GST</cbc:ID>
                        </cac:TaxScheme>
                    </cac:TaxCategory>
                </cac:TaxSubtotal>
                <cac:TaxSubtotal>
                    <!-- Subtotal for 'Z' Zero-rated tax category of 0% GST -->
                    <cbc:TaxableAmount currencyID="AUD">-13.5</cbc:TaxableAmount>
                    <cbc:TaxAmount currencyID="AUD">0.00</cbc:TaxAmount>
                    <cac:TaxCategory>
                        <cbc:ID>Z</cbc:ID>
                        <cbc:Percent>0</cbc:Percent>
                        <cac:TaxScheme>
                            <cbc:ID>GST</cbc:ID>
                        </cac:TaxScheme>
                    </cac:TaxCategory>
                </cac:TaxSubtotal>
            </cac:TaxTotal>
            <cac:LegalMonetaryTotal>
                <cbc:LineExtensionAmount currencyID="AUD">145.93</cbc:LineExtensionAmount>
                <cbc:TaxExclusiveAmount currencyID="AUD">145.93</cbc:TaxExclusiveAmount>
                <cbc:TaxInclusiveAmount currencyID="AUD">161.87</cbc:TaxInclusiveAmount>
                <cbc:PayableAmount currencyID="AUD">161.87</cbc:PayableAmount> <!-- New charges invoiced (excluding prior unpaid amount) -->
            </cac:LegalMonetaryTotal>
            <cac:InvoiceLine>
                <!-- Line with 10% GST -->
                <cbc:ID>1</cbc:ID>
                <cbc:InvoicedQuantity unitCode="KWH">325.2</cbc:InvoicedQuantity>
                <cbc:LineExtensionAmount currencyID="AUD">129.04</cbc:LineExtensionAmount>
                <cac:Item>
                    <cbc:Name>Electricity charges - all day rate NMI 9000074677</cbc:Name>
                    <cac:ClassifiedTaxCategory>
                        <cbc:ID>S</cbc:ID>
                        <cbc:Percent>10</cbc:Percent> <!-- 10% GST -->
                        <cac:TaxScheme>
                            <cbc:ID>GST</cbc:ID>
                        </cac:TaxScheme>
                    </cac:ClassifiedTaxCategory>
                </cac:Item>
                <cac:Price>
                    <cbc:PriceAmount currencyID="AUD">0.3968</cbc:PriceAmount>
                </cac:Price>
            </cac:InvoiceLine>
            <cac:InvoiceLine>
                <!-- Line with credit value and zero GST -->
                <cbc:ID>2</cbc:ID>
                <cbc:InvoicedQuantity unitCode="KWH">-150</cbc:InvoicedQuantity>
                <cbc:LineExtensionAmount currencyID="AUD">-13.5</cbc:LineExtensionAmount>
                <cac:Item>
                    <cbc:Name>Solar feed-in rebate NMI 9000074677</cbc:Name>
                    <cac:ClassifiedTaxCategory>
                        <cbc:ID>Z</cbc:ID>
                        <cbc:Percent>0</cbc:Percent> <!-- 0% GST -->
                        <cac:TaxScheme>
                            <cbc:ID>GST</cbc:ID>
                        </cac:TaxScheme>
                    </cac:ClassifiedTaxCategory>
                </cac:Item>
                <cac:Price>
                    <cbc:PriceAmount currencyID="AUD">0.09</cbc:PriceAmount>
                </cac:Price>
            </cac:InvoiceLine>
            <cac:InvoiceLine>
                <!-- Line with 10% GST -->
                <cbc:ID>3</cbc:ID>
                <cbc:InvoicedQuantity unitCode="DAY">31</cbc:InvoicedQuantity>
                <cbc:LineExtensionAmount currencyID="AUD">30.39</cbc:LineExtensionAmount>
                <cac:Item>
                    <cbc:Name>Supply charge</cbc:Name>
                    <cac:ClassifiedTaxCategory>
                        <cbc:ID>S</cbc:ID>
                        <cbc:Percent>10</cbc:Percent> <!-- 10% GST -->
                        <cac:TaxScheme>
                            <cbc:ID>GST</cbc:ID>
                        </cac:TaxScheme>
                    </cac:ClassifiedTaxCategory>
                </cac:Item>
                <cac:Price>
                    <cbc:PriceAmount currencyID="AUD">0.9803</cbc:PriceAmount>
                </cac:Price>
            </cac:InvoiceLine>
        </Invoice>
        '''),
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

    assert res.status_code == 203
 
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
    assert response_body['message'] == "test.pdf is not a XML, please upload a valid file"
    
def test_validate_upload_unsucessful(client, user):
    data = {}
    data['files'] = [(io.BytesIO(b'''<?xml version="1.0" encoding="UTF-8"?>
        <!-- Example of a simple invoice with 'mixed' taxable and non-taxable supplies including a non-taxable solar rebate (e.g. micro-business not registered for GST) -->
        <Invoice xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2">
            <cbc:CustomizationID>urn:cen.eu:en16931:2017#conformant#urn:fdc:peppol.eu:2017:poacc:billing:international:aunz:3.0</cbc:CustomizationID>
            <cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID>
            <cbc:ID>Invoice01</cbc:ID>
            <cbc:IssueDate>2022-07-29</cbc:IssueDate>
            <cbc:DueDate>2022-08-30</cbc:DueDate>
        </Invoice>
        '''),
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

    assert res.status_code == 203

def test_uploadcreate_json(client, user):
    data = {}
    data['files'] = [(io.BytesIO(TEST_DATA["JSON_STR_1"].encode("utf-8")), 'test.json')]
    
    # data['rules'] = 'AUNZ_PEPPOL_1_0_10'

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
    print(response_body)
    
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
    
    

