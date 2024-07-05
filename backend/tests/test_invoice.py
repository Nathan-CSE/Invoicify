import io
import pytest
import json

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
INVOICE_UPLOAD_PATH = "/invoice/validate"

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
        INVOICE_UPLOAD_PATH,
        headers={
            "Authorisation": user.token
        },
        data=data,  
        content_type='multipart/form-data',
        follow_redirects=True
    )
    
    response_body = res.get_json()

    assert res.status_code == 203
    assert response_body['message']["successful"] is False
 
def test_validate_upload_nonXML(client, user):
    data = {}
    data['files'] = [(io.BytesIO(b'fail, not xml'),
        'test.pdf')]
    data['rules'] = 'AUNZ_PEPPOL_1_0_10'
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
        INVOICE_UPLOAD_PATH,
        headers={
            "Authorisation": user.token
        },
        data=data,  
        content_type='multipart/form-data',
        follow_redirects=True
    )
    response_body = res.get_json()

    assert res.status_code == 203
    assert response_body['message']["successful"] is False