import base64
import io

from tests.data import TEST_DATA
from tests.urls import (
    INVOICE_DELETE_PATH, 
    INVOICE_DOWNLOAD_PATH, 
    INVOICE_HISTORY_PATH, 
    INVOICE_SEND_PATH, 
    INVOICE_UPLOAD_CREATE_PATH, 
    INVOICE_UPLOAD_VALIDATE_PATH, 
    INVOICE_VALIDATE_PATH
)
from tests.fixtures import client, user

# Upload JSON Create -> Download (Success)
def test_json_create_download_interaction(client, user):
    data = {
        "files": [(io.BytesIO(TEST_DATA["JSON_STR_1"].encode("utf-8")), 'test.json')]
    }

    res = client.post(
        INVOICE_UPLOAD_CREATE_PATH,
        data=data,
        headers={
            "Authorisation": user.token,
            "Content-Type": "multipart/form-data",
        }
    )    
    assert res.status_code == 200
    assert res.json["data"] == [{"filename": "test.xml", "invoiceId": 1}]
    invoice_id = res.json["data"][0]["invoiceId"]

    res = client.post(
        f"{INVOICE_DOWNLOAD_PATH}/{invoice_id}",
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json",
        }
    )

    assert res.status_code == 200
    assert res.json["message"] == '<?xml version="1.0" encoding="UTF-8"?><Invoice xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"><cbc:CustomizationID>urn:cen.eu:en16931:2017#conformant#urn:fdc:peppol.eu:2017:poacc:billing:international:aunz:3.0</cbc:CustomizationID><cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID><cbc:ID>Invoice03</cbc:ID><cbc:IssueDate>2022-07-31</cbc:IssueDate><cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode><cbc:Note>Adjustment note to reverse prior bill Invoice01. Free text field can bring attention to reason for credit etc.</cbc:Note><cbc:DocumentCurrencyCode>AUD</cbc:DocumentCurrencyCode><cbc:BuyerReference>Simple solar plan</cbc:BuyerReference><cac:InvoicePeriod><cbc:StartDate>2022-06-15</cbc:StartDate><cbc:EndDate>2022-07-15</cbc:EndDate></cac:InvoicePeriod><cac:BillingReference><cac:InvoiceDocumentReference><cbc:ID>Invoice01</cbc:ID><cbc:IssueDate>2022-07-29</cbc:IssueDate></cac:InvoiceDocumentReference></cac:BillingReference><cac:AdditionalDocumentReference><cbc:ID>Invoice03.pdf</cbc:ID><cac:Attachment><cbc:EmbeddedDocumentBinaryObject mimeCode="application/pdf" filename="Invoice03.pdf">UGxhaW4gdGV4dCBpbiBwbGFjZSBvZiBwZGYgYXR0YWNobWVudCBmb3Igc2FtcGxlIGludm9pY2Vz</cbc:EmbeddedDocumentBinaryObject></cac:Attachment></cac:AdditionalDocumentReference><cac:AccountingSupplierParty><cac:Party><cbc:EndpointID schemeID="0151">47555222000</cbc:EndpointID><cac:PostalAddress><cbc:CityName>Harrison</cbc:CityName><cbc:PostalZone>2912</cbc:PostalZone><cbc:CountrySubentity>NSW</cbc:CountrySubentity><cac:Country><cbc:IdentificationCode>AU</cbc:IdentificationCode></cac:Country></cac:PostalAddress><cac:PartyLegalEntity><cbc:RegistrationName>Grey Roo Energy</cbc:RegistrationName><cbc:CompanyID schemeID="0151">47555222000</cbc:CompanyID></cac:PartyLegalEntity></cac:Party></cac:AccountingSupplierParty><cac:AccountingCustomerParty><cac:Party><cbc:EndpointID schemeID="0151">47555222000</cbc:EndpointID><cac:PartyIdentification><cbc:ID>AccountNumber123</cbc:ID></cac:PartyIdentification><cac:PostalAddress><cbc:StreetName>100 Queen Street</cbc:StreetName><cbc:CityName>Sydney</cbc:CityName><cbc:PostalZone>2000</cbc:PostalZone><cbc:CountrySubentity>NSW</cbc:CountrySubentity><cac:Country><cbc:IdentificationCode>AU</cbc:IdentificationCode></cac:Country></cac:PostalAddress><cac:PartyLegalEntity><cbc:RegistrationName>Trotters Incorporated</cbc:RegistrationName><cbc:CompanyID schemeID="0151">91888222000</cbc:CompanyID></cac:PartyLegalEntity><cac:Contact><cbc:Name>Lisa Johnson</cbc:Name></cac:Contact></cac:Party></cac:AccountingCustomerParty><cac:TaxTotal><cbc:TaxAmount currencyID="AUD">-15.94</cbc:TaxAmount><cac:TaxSubtotal><cbc:TaxableAmount currencyID="AUD">-159.43</cbc:TaxableAmount><cbc:TaxAmount currencyID="AUD">-15.94</cbc:TaxAmount><cac:TaxCategory><cbc:ID>S</cbc:ID><cbc:Percent>10</cbc:Percent><cac:TaxScheme><cbc:ID>GST</cbc:ID></cac:TaxScheme></cac:TaxCategory></cac:TaxSubtotal></cac:TaxTotal><cac:LegalMonetaryTotal><cbc:LineExtensionAmount currencyID="AUD">-159.43</cbc:LineExtensionAmount><cbc:TaxExclusiveAmount currencyID="AUD">-159.43</cbc:TaxExclusiveAmount><cbc:TaxInclusiveAmount currencyID="AUD">-175.37</cbc:TaxInclusiveAmount><cbc:PayableAmount currencyID="AUD">-175.37</cbc:PayableAmount></cac:LegalMonetaryTotal><cac:InvoiceLine><cbc:ID>1</cbc:ID><cbc:InvoicedQuantity unitCode="KWH">-325.2</cbc:InvoicedQuantity><cbc:LineExtensionAmount currencyID="AUD">-129.04</cbc:LineExtensionAmount><cac:Item><cbc:Name>Adjustment - reverse prior Electricity charges - all day rate NMI 9000074677</cbc:Name><cac:ClassifiedTaxCategory><cbc:ID>S</cbc:ID><cbc:Percent>10</cbc:Percent><cac:TaxScheme><cbc:ID>GST</cbc:ID></cac:TaxScheme></cac:ClassifiedTaxCategory></cac:Item><cac:Price><cbc:PriceAmount currencyID="AUD">0.3968</cbc:PriceAmount></cac:Price></cac:InvoiceLine><cac:InvoiceLine><cbc:ID>2</cbc:ID><cbc:InvoicedQuantity unitCode="DAY">-31</cbc:InvoicedQuantity><cbc:LineExtensionAmount currencyID="AUD">-30.39</cbc:LineExtensionAmount><cac:Item><cbc:Name>Adjustment - reverse prior Supply charge</cbc:Name><cac:ClassifiedTaxCategory><cbc:ID>S</cbc:ID><cbc:Percent>10</cbc:Percent><cac:TaxScheme><cbc:ID>GST</cbc:ID></cac:TaxScheme></cac:ClassifiedTaxCategory></cac:Item><cac:Price><cbc:PriceAmount currencyID="AUD">0.9803</cbc:PriceAmount></cac:Price></cac:InvoiceLine></Invoice>'

# Upload PDF Create -> Download (Success)
# TODO: Reenable on final push
def _test_pdf_create_download_interaction(client, user):
    data = {
        "files": [(io.BytesIO(base64.b64decode(TEST_DATA["PDF_1"])), 'test.pdf')]
    }

    res = client.post(
        INVOICE_UPLOAD_CREATE_PATH,
        data=data,
        headers={
            "Authorisation": user.token,
            "Content-Type": "multipart/form-data",
        }
    )    
    assert res.status_code == 200
    assert res.json["data"] == [{"filename": "test.xml", "invoiceId": 1}]
    invoice_id = res.json["data"][0]["invoiceId"]

    res = client.post(
        f"{INVOICE_DOWNLOAD_PATH}/{invoice_id}",
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json",
        }
    )

    assert res.status_code == 200
    assert res.json["message"] == '<?xml version="1.0" encoding="UTF-8"?><Invoice xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"><cbc:CustomizationID>urn:cen.eu:en16931:2017#conformant#urn:fdc:peppol.eu:2017:poacc:billing:international:aunz:3.0</cbc:CustomizationID><cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID><cbc:VendorName>DEMO - Sliced Invoices</cbc:VendorName><cbc:VendorAddress>Suite 5A-1204, 123 Somewhere Street, Your City AZ 12345</cbc:VendorAddress><cbc:CustomerName>Test Business</cbc:CustomerName><cbc:InvoiceDate>January 25, 2016</cbc:InvoiceDate><cbc:TotalAmount>$93.50</cbc:TotalAmount><cbc:TotalTaxorVAT>$8.50</cbc:TotalTaxorVAT><cbc:PaymentTerms>Payment is due within 30 days from date of invoice. Late payment is subject to fees of 5% per month.</cbc:PaymentTerms><cbc:PurchaseOrderReference>12345</cbc:PurchaseOrderReference><cbc:BillingName>Test Business</cbc:BillingName><cbc:BillingAddress>123 Somewhere St, Melbourne, VIC 3000</cbc:BillingAddress><cac:InvoiceLine><cbc:Description>Web Design</cbc:Description><cbc:Quantity>1.00</cbc:Quantity><cbc:UnitPrice>$85.00</cbc:UnitPrice><cbc:Tax>$8.50</cbc:Tax><cbc:Amount>$93.50</cbc:Amount></cac:InvoiceLine></Invoice>'

# Upload JSON Create -> Validate (Success) -> Send (Success)
def test_json_create_validate_send_interaction(client, user):
    data = {
        "files": [(io.BytesIO(TEST_DATA["JSON_STR_1"].encode("utf-8")), 'test.json')]
    }

    res = client.post(
        INVOICE_UPLOAD_CREATE_PATH,
        data=data,
        headers={
            "Authorisation": user.token,
            "Content-Type": "multipart/form-data",
        }
    )    
    assert res.status_code == 200
    assert res.json["data"] == [{"filename": "test.xml", "invoiceId": 1}]
    invoice_id = res.json["data"][0]["invoiceId"]

    res = client.get(
        f"{INVOICE_VALIDATE_PATH}?rules=AUNZ_PEPPOL_1_0_10&id={invoice_id}",
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200
    assert res.json["validationOutcome"][0]["validated"]

    res = client.post(
        f"{INVOICE_SEND_PATH}?xml_id={invoice_id}&target_email=TEST",
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200

# Upload JSON Create -> Validate (Fail) -> Send (Fail)
def test_json_create_validate_fail_send_fail_interaction(client, user):
    data = {
        "files": [(io.BytesIO(TEST_DATA["FAILED_JSON_STR_1"].encode("utf-8")), 'test.json')]
    }

    res = client.post(
        INVOICE_UPLOAD_CREATE_PATH,
        data=data,
        headers={
            "Authorisation": user.token,
            "Content-Type": "multipart/form-data",
        }
    )    
    assert res.status_code == 200
    assert res.json["data"] == [{"filename": "test.xml", "invoiceId": 1}]
    invoice_id = res.json["data"][0]["invoiceId"]

    res = client.get(
        f"{INVOICE_VALIDATE_PATH}?rules=AUNZ_PEPPOL_1_0_10&id={invoice_id}",
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200
    assert not res.json["validationOutcome"][0]["validated"]

    res = client.post(
        f"{INVOICE_SEND_PATH}?xml_id={invoice_id}&target_email=TEST",
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 400

# Upload PDF Create -> Validate (Fail) -> Send (Fail)
# TODO: Reenable
def _test_pdf_create_validate_fail_send_fail_interaction(client, user):
    data = {
        "files": [(io.BytesIO(base64.b64decode(TEST_DATA["PDF_1"])), 'test.pdf')]
    }

    res = client.post(
        INVOICE_UPLOAD_CREATE_PATH,
        data=data,
        headers={
            "Authorisation": user.token,
            "Content-Type": "multipart/form-data",
        }
    )    
    assert res.status_code == 200
    assert res.json["data"] == [{"filename": "test.xml", "invoiceId": 1}]
    invoice_id = res.json["data"][0]["invoiceId"]

    res = client.get(
        f"{INVOICE_VALIDATE_PATH}?rules=AUNZ_PEPPOL_1_0_10&id={invoice_id}",
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200
    assert not res.json["validationOutcome"][0]["validated"]

    res = client.post(
        f"{INVOICE_SEND_PATH}?xml_id={invoice_id}&target_email=TEST",
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 400

# Upload XML Validate (Success) -> Send (Success)
def test_xml_validate_send_interaction(client, user):
    data = {
        "rules": "AUNZ_PEPPOL_1_0_10",
        "files": [(io.BytesIO(TEST_DATA['GOOD_XML'].encode('UTF-8')), 'test.xml')]
    }

    res = client.post(
        INVOICE_UPLOAD_VALIDATE_PATH,
        headers={
            "Authorisation": user.token
        },
        data=data,  
        content_type='multipart/form-data',
    )
    
    assert res.status_code == 200
    assert res.json["validationOutcome"][0]["validated"]
    invoice_id = res.json['validationOutcome'][0]['invoiceId']

    res = client.post(
        f"{INVOICE_SEND_PATH}?xml_id={invoice_id}&target_email=TEST",
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200

# Upload XML Validate (Fail) -> Send (Fail)
def test_xml_validate_fail_send_fail_interaction(client, user):
    data = {
        "rules": "AUNZ_PEPPOL_1_0_10",
        "files": [(io.BytesIO(TEST_DATA['BAD_XML'].encode('UTF-8')), 'test.xml')]
    }

    res = client.post(
        INVOICE_UPLOAD_VALIDATE_PATH,
        headers={
            "Authorisation": user.token
        },
        data=data,  
        content_type='multipart/form-data',
    )
    
    assert res.status_code == 200
    assert not res.json["validationOutcome"][0]["validated"]
    invoice_id = res.json['validationOutcome'][0]['invoiceId']

    res = client.post(
        f"{INVOICE_SEND_PATH}?xml_id={invoice_id}&target_email=TEST",
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 400

# JSON Create -> History (Confirm 1 exists) -> Delete -> History (Confirm 0 exists)
def test_json_create_history_delete_history_interaction(client, user):
    data = {
        "files": [(io.BytesIO(TEST_DATA["JSON_STR_1"].encode("utf-8")), 'test.json')]
    }

    res = client.post(
        INVOICE_UPLOAD_CREATE_PATH,
        data=data,
        headers={
            "Authorisation": user.token,
            "Content-Type": "multipart/form-data",
        }
    )    
    assert res.status_code == 200
    assert res.json["data"] == [{"filename": "test.xml", "invoiceId": 1}]
    invoice_id = res.json["data"][0]["invoiceId"]

    res = client.get(
        INVOICE_HISTORY_PATH,
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200
    assert len(res.json) == 1

    res = client.delete(
        f"{INVOICE_DELETE_PATH}/{invoice_id}",
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200

    res = client.get(
        INVOICE_HISTORY_PATH,
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200
    assert len(res.json) == 0

# PDF Create -> History (Confirm 1 exists) -> Delete -> History (Confirm 0 exists)
# TODO: Reenable
def _test_pdf_create_history_delete_history_interaction(client, user):
    data = {
        "files": [(io.BytesIO(base64.b64decode(TEST_DATA["PDF_1"])), 'test.pdf')]
    }

    res = client.post(
        INVOICE_UPLOAD_CREATE_PATH,
        data=data,
        headers={
            "Authorisation": user.token,
            "Content-Type": "multipart/form-data",
        }
    )    
    assert res.status_code == 200
    assert res.json["data"] == [{"filename": "test.xml", "invoiceId": 1}]
    invoice_id = res.json["data"][0]["invoiceId"]

    res = client.get(
        INVOICE_HISTORY_PATH,
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200
    assert len(res.json) == 1

    res = client.delete(
        f"{INVOICE_DELETE_PATH}/{invoice_id}",
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200

    res = client.get(
        INVOICE_HISTORY_PATH,
        headers={
            "Authorisation": user.token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200
    assert len(res.json) == 0