import base64
import io
import json
import copy

from tests.data import TEST_DATA
from tests.fixtures import client
from tests.urls import (
    INVOICE_CREATE_PATH,
    INVOICE_DELETE_PATH,
    INVOICE_DOWNLOAD_PATH, 
    INVOICE_EDIT_PATH, 
    INVOICE_HISTORY_PATH, 
    INVOICE_SEND_PATH,
    INVOICE_UPLOAD_CREATE_PATH,
    INVOICE_UPLOAD_VALIDATE_PATH, 
    INVOICE_VALIDATE_PATH, 
    REGISTER_PATH
)

# Register -> GUI Create -> Download -> History (Confirm 1 Exist) -> Validate (Fail) -> Edit -> Validate (Success) -> Send (Success) -> Delete -> History (Confirm 0 exists)
def test_gui_create_sequence(client):
    data = {
        "email": "abc@gmail.com",
        "password": "abc"
    }
    
    res = client.post(
        REGISTER_PATH, 
        data=json.dumps(data),
        content_type="application/json"
    )

    assert res.status_code == 201
    user_token = res.json["token"]

    data = copy.deepcopy(TEST_DATA["JSON"])
    data["seller"]["ABN"] = 123123

    res = client.post(
        INVOICE_CREATE_PATH,
        data=json.dumps(data),
        headers={
            "Authorisation": user_token,
            "Content-Type": "application/json",
        }
    )    
    assert res.status_code == 201
    assert res.json["data"] == [{"filename": "test.xml", "invoiceId": 1}]
    invoice_id = res.json["data"][0]["invoiceId"]

    res = client.post(
        f"{INVOICE_DOWNLOAD_PATH}/{invoice_id}",
        headers={
            "Authorisation": user_token,
            "Content-Type": "application/json",
        }
    )
    assert res.status_code == 200
    assert res.json["message"] == '<?xml version="1.0" encoding="UTF-8"?><Invoice xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"><cbc:CustomizationID>urn:cen.eu:en16931:2017#conformant#urn:fdc:peppol.eu:2017:poacc:billing:international:aunz:3.0</cbc:CustomizationID><cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID><cbc:ID>1</cbc:ID><cbc:IssueDate>2024-06-25</cbc:IssueDate><cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode><cbc:Note>Taxinvoice</cbc:Note><cbc:DocumentCurrencyCode>AUD</cbc:DocumentCurrencyCode><cbc:BuyerReference>test</cbc:BuyerReference><cac:AccountingSupplierParty><cac:Party><cbc:EndpointID schemeID="0151">123123</cbc:EndpointID><cac:PartyName><cbc:Name>Windows to Fit Pty Ltd</cbc:Name></cac:PartyName><cac:PostalAddress><cbc:StreetName>Test</cbc:StreetName><cbc:AdditionalStreetName>test</cbc:AdditionalStreetName><cbc:CityName>test</cbc:CityName><cbc:PostalZone>2912</cbc:PostalZone><cac:Country><cbc:IdentificationCode>AU</cbc:IdentificationCode></cac:Country></cac:PostalAddress><cac:PartyLegalEntity><cbc:RegistrationName>Windows to Fit Pty Ltd</cbc:RegistrationName><cbc:CompanyID schemeID="0151">123123</cbc:CompanyID></cac:PartyLegalEntity><cac:PartyTaxScheme><cbc:CompanyID>123123</cbc:CompanyID><cac:TaxScheme><cbc:ID>GST</cbc:ID></cac:TaxScheme></cac:PartyTaxScheme></cac:Party></cac:AccountingSupplierParty><cac:AccountingCustomerParty><cac:Party><cbc:EndpointID schemeID="0151">47555222000</cbc:EndpointID><cac:PartyName><cbc:Name>Henry Averies</cbc:Name></cac:PartyName><cac:PostalAddress><cbc:StreetName>Jam</cbc:StreetName><cbc:AdditionalStreetName>a man</cbc:AdditionalStreetName><cbc:CityName>of fortune</cbc:CityName><cbc:PostalZone>1994</cbc:PostalZone><cac:Country><cbc:IdentificationCode>AU</cbc:IdentificationCode></cac:Country></cac:PostalAddress><cac:PartyLegalEntity><cbc:RegistrationName>Henry Averies</cbc:RegistrationName><cbc:CompanyID schemeID="0151">47555222000</cbc:CompanyID></cac:PartyLegalEntity><cac:PartyTaxScheme><cac:TaxScheme><cbc:CompanyID>47555222000</cbc:CompanyID><cbc:ID>GST</cbc:ID></cac:TaxScheme></cac:PartyTaxScheme></cac:Party></cac:AccountingCustomerParty><cac:TaxTotal><cbc:TaxAmount currencyID="AUD">10</cbc:TaxAmount><cac:TaxSubtotal><cbc:TaxableAmount currencyID="AUD">100</cbc:TaxableAmount><cbc:TaxAmount currencyID="AUD">10</cbc:TaxAmount><cac:TaxCategory><cbc:ID>S</cbc:ID><cbc:Percent>10</cbc:Percent><cac:TaxScheme><cbc:ID>GST</cbc:ID></cac:TaxScheme></cac:TaxCategory></cac:TaxSubtotal></cac:TaxTotal><cac:LegalMonetaryTotal><cbc:LineExtensionAmount currencyID="AUD">1000</cbc:LineExtensionAmount><cbc:TaxExclusiveAmount currencyID="AUD">1000</cbc:TaxExclusiveAmount><cbc:TaxInclusiveAmount currencyID="AUD">1100</cbc:TaxInclusiveAmount><cbc:PayableAmount currencyID="AUD">1100</cbc:PayableAmount></cac:LegalMonetaryTotal><cac:InvoiceLine><cbc:ID>0</cbc:ID><cbc:InvoicedQuantity unitCode="X01">10</cbc:InvoicedQuantity><cbc:LineExtensionAmount currencyID="AUD">1100</cbc:LineExtensionAmount><cac:Item><cbc:Description>Pirate</cbc:Description><cbc:Name>Booty</cbc:Name><cac:ClassifiedTaxCategory><cbc:ID>GST</cbc:ID><cbc:Percent>10</cbc:Percent><cac:TaxScheme><cbc:ID>GST</cbc:ID></cac:TaxScheme></cac:ClassifiedTaxCategory></cac:Item><cac:Price><cbc:PriceAmount currencyID="AUD">110</cbc:PriceAmount></cac:Price></cac:InvoiceLine></Invoice>'

    res = client.get(
        INVOICE_HISTORY_PATH,
        headers={
            "Authorisation": user_token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200
    assert len(res.json) == 1

    res = client.get(
        f"{INVOICE_VALIDATE_PATH}?rules=AUNZ_PEPPOL_1_0_10&id={invoice_id}",
        headers={
            "Authorisation": user_token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200
    assert not res.json["validationOutcome"][0]["validated"]

    data = {
        "name": "Should work now",
        "fields": TEST_DATA["JSON"],
        "rule": "AUNZ_PEPPOL_1_0_10"
    }

    res = client.put(
        f"{INVOICE_EDIT_PATH}/{invoice_id}",
        data=json.dumps(data),
        headers={
            "Authorisation": user_token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 204

    res = client.get(
        f"{INVOICE_VALIDATE_PATH}?rules=AUNZ_PEPPOL_1_0_10&id={invoice_id}",
        headers={
            "Authorisation": user_token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200
    assert res.json["validationOutcome"][0]["validated"]

    res = client.post(
        f"{INVOICE_SEND_PATH}?xml_id={invoice_id}&target_email=TEST",
        headers={
            "Authorisation": user_token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200

    res = client.delete(
        f"{INVOICE_DELETE_PATH}/{invoice_id}",
        headers={
            "Authorisation": user_token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200

    res = client.get(
        INVOICE_HISTORY_PATH,
        headers={
            "Authorisation": user_token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200
    assert len(res.json) == 0


# Register -> Upload JSON Create -> Download -> History (Confirm 1 Exist) -> Validate (Success) -> Send (Success) -> Delete -> History (Confirm 0 exists)
def test_json_create_sequence(client):
    data = {
        "email": "abc@gmail.com",
        "password": "abc"
    }
    
    res = client.post(
        REGISTER_PATH, 
        data=json.dumps(data),
        content_type="application/json"
    )

    assert res.status_code == 201
    user_token = res.json["token"]

    data['files'] = [(io.BytesIO(TEST_DATA["JSON_STR_1"].encode("utf-8")), 'test.json')]

    res = client.post(
        INVOICE_UPLOAD_CREATE_PATH,
        data=data,
        headers={
            "Authorisation": user_token,
            "Content-Type": "multipart/form-data",
        }
    )    
    assert res.status_code == 200
    assert res.json["data"] == [{"filename": "test.xml", "invoiceId": 1}]
    invoice_id = res.json["data"][0]["invoiceId"]

    res = client.post(
        f"{INVOICE_DOWNLOAD_PATH}/{invoice_id}",
        headers={
            "Authorisation": user_token,
            "Content-Type": "application/json",
        }
    )

    assert res.status_code == 200
    assert res.json["message"] == '<?xml version="1.0" encoding="UTF-8"?><Invoice xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"><cbc:CustomizationID>urn:cen.eu:en16931:2017#conformant#urn:fdc:peppol.eu:2017:poacc:billing:international:aunz:3.0</cbc:CustomizationID><cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID><cbc:ID>Invoice03</cbc:ID><cbc:IssueDate>2022-07-31</cbc:IssueDate><cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode><cbc:Note>Adjustment note to reverse prior bill Invoice01. Free text field can bring attention to reason for credit etc.</cbc:Note><cbc:DocumentCurrencyCode>AUD</cbc:DocumentCurrencyCode><cbc:BuyerReference>Simple solar plan</cbc:BuyerReference><cac:InvoicePeriod><cbc:StartDate>2022-06-15</cbc:StartDate><cbc:EndDate>2022-07-15</cbc:EndDate></cac:InvoicePeriod><cac:BillingReference><cac:InvoiceDocumentReference><cbc:ID>Invoice01</cbc:ID><cbc:IssueDate>2022-07-29</cbc:IssueDate></cac:InvoiceDocumentReference></cac:BillingReference><cac:AdditionalDocumentReference><cbc:ID>Invoice03.pdf</cbc:ID><cac:Attachment><cbc:EmbeddedDocumentBinaryObject mimeCode="application/pdf" filename="Invoice03.pdf">UGxhaW4gdGV4dCBpbiBwbGFjZSBvZiBwZGYgYXR0YWNobWVudCBmb3Igc2FtcGxlIGludm9pY2Vz</cbc:EmbeddedDocumentBinaryObject></cac:Attachment></cac:AdditionalDocumentReference><cac:AccountingSupplierParty><cac:Party><cbc:EndpointID schemeID="0151">47555222000</cbc:EndpointID><cac:PostalAddress><cbc:CityName>Harrison</cbc:CityName><cbc:PostalZone>2912</cbc:PostalZone><cbc:CountrySubentity>NSW</cbc:CountrySubentity><cac:Country><cbc:IdentificationCode>AU</cbc:IdentificationCode></cac:Country></cac:PostalAddress><cac:PartyLegalEntity><cbc:RegistrationName>Grey Roo Energy</cbc:RegistrationName><cbc:CompanyID schemeID="0151">47555222000</cbc:CompanyID></cac:PartyLegalEntity></cac:Party></cac:AccountingSupplierParty><cac:AccountingCustomerParty><cac:Party><cbc:EndpointID schemeID="0151">47555222000</cbc:EndpointID><cac:PartyIdentification><cbc:ID>AccountNumber123</cbc:ID></cac:PartyIdentification><cac:PostalAddress><cbc:StreetName>100 Queen Street</cbc:StreetName><cbc:CityName>Sydney</cbc:CityName><cbc:PostalZone>2000</cbc:PostalZone><cbc:CountrySubentity>NSW</cbc:CountrySubentity><cac:Country><cbc:IdentificationCode>AU</cbc:IdentificationCode></cac:Country></cac:PostalAddress><cac:PartyLegalEntity><cbc:RegistrationName>Trotters Incorporated</cbc:RegistrationName><cbc:CompanyID schemeID="0151">91888222000</cbc:CompanyID></cac:PartyLegalEntity><cac:Contact><cbc:Name>Lisa Johnson</cbc:Name></cac:Contact></cac:Party></cac:AccountingCustomerParty><cac:TaxTotal><cbc:TaxAmount currencyID="AUD">-15.94</cbc:TaxAmount><cac:TaxSubtotal><cbc:TaxableAmount currencyID="AUD">-159.43</cbc:TaxableAmount><cbc:TaxAmount currencyID="AUD">-15.94</cbc:TaxAmount><cac:TaxCategory><cbc:ID>S</cbc:ID><cbc:Percent>10</cbc:Percent><cac:TaxScheme><cbc:ID>GST</cbc:ID></cac:TaxScheme></cac:TaxCategory></cac:TaxSubtotal></cac:TaxTotal><cac:LegalMonetaryTotal><cbc:LineExtensionAmount currencyID="AUD">-159.43</cbc:LineExtensionAmount><cbc:TaxExclusiveAmount currencyID="AUD">-159.43</cbc:TaxExclusiveAmount><cbc:TaxInclusiveAmount currencyID="AUD">-175.37</cbc:TaxInclusiveAmount><cbc:PayableAmount currencyID="AUD">-175.37</cbc:PayableAmount></cac:LegalMonetaryTotal><cac:InvoiceLine><cbc:ID>1</cbc:ID><cbc:InvoicedQuantity unitCode="KWH">-325.2</cbc:InvoicedQuantity><cbc:LineExtensionAmount currencyID="AUD">-129.04</cbc:LineExtensionAmount><cac:Item><cbc:Name>Adjustment - reverse prior Electricity charges - all day rate NMI 9000074677</cbc:Name><cac:ClassifiedTaxCategory><cbc:ID>S</cbc:ID><cbc:Percent>10</cbc:Percent><cac:TaxScheme><cbc:ID>GST</cbc:ID></cac:TaxScheme></cac:ClassifiedTaxCategory></cac:Item><cac:Price><cbc:PriceAmount currencyID="AUD">0.3968</cbc:PriceAmount></cac:Price></cac:InvoiceLine><cac:InvoiceLine><cbc:ID>2</cbc:ID><cbc:InvoicedQuantity unitCode="DAY">-31</cbc:InvoicedQuantity><cbc:LineExtensionAmount currencyID="AUD">-30.39</cbc:LineExtensionAmount><cac:Item><cbc:Name>Adjustment - reverse prior Supply charge</cbc:Name><cac:ClassifiedTaxCategory><cbc:ID>S</cbc:ID><cbc:Percent>10</cbc:Percent><cac:TaxScheme><cbc:ID>GST</cbc:ID></cac:TaxScheme></cac:ClassifiedTaxCategory></cac:Item><cac:Price><cbc:PriceAmount currencyID="AUD">0.9803</cbc:PriceAmount></cac:Price></cac:InvoiceLine></Invoice>'

    res = client.get(
        INVOICE_HISTORY_PATH,
        headers={
            "Authorisation": user_token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200
    assert len(res.json) == 1

    res = client.get(
        f"{INVOICE_VALIDATE_PATH}?rules=AUNZ_PEPPOL_1_0_10&id={invoice_id}",
        headers={
            "Authorisation": user_token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200
    assert res.json["validationOutcome"][0]["validated"]

    res = client.post(
        f"{INVOICE_SEND_PATH}?xml_id={invoice_id}&target_email=TEST",
        headers={
            "Authorisation": user_token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200

    res = client.delete(
        f"{INVOICE_DELETE_PATH}/{invoice_id}",
        headers={
            "Authorisation": user_token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200

    res = client.get(
        INVOICE_HISTORY_PATH,
        headers={
            "Authorisation": user_token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200
    assert len(res.json) == 0

# Register -> Upload PDF Create -> Download -> History (Confirm 1 exist) -> Validate (Fail) -> Delete -> History (Confirm 0 exists)
def test_pdf_create_sequence(client):
    data = {
        "email": "abc@gmail.com",
        "password": "abc"
    }
    
    res = client.post(
        REGISTER_PATH, 
        data=json.dumps(data),
        content_type="application/json"
    )

    assert res.status_code == 201
    user_token = res.json["token"]

    data['files'] = [(io.BytesIO(base64.b64decode(TEST_DATA["PDF_1"])), 'test.pdf')]

    res = client.post(
        INVOICE_UPLOAD_CREATE_PATH,
        data=data,
        headers={
            "Authorisation": user_token,
            "Content-Type": "multipart/form-data",
        }
    )    
    assert res.status_code == 200
    assert res.json["data"] == [{"filename": "test.xml", "invoiceId": 1}]
    invoice_id = res.json["data"][0]["invoiceId"]

    res = client.post(
        f"{INVOICE_DOWNLOAD_PATH}/{invoice_id}",
        headers={
            "Authorisation": user_token,
            "Content-Type": "application/json",
        }
    )

    assert res.status_code == 200
    assert res.json["message"] == '<?xml version="1.0" encoding="UTF-8"?><Invoice xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"><cbc:CustomizationID>urn:cen.eu:en16931:2017#conformant#urn:fdc:peppol.eu:2017:poacc:billing:international:aunz:3.0</cbc:CustomizationID><cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID><cbc:ID>Invoice03</cbc:ID><cbc:IssueDate>2022-07-31</cbc:IssueDate><cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode><cbc:Note>Adjustment note to reverse prior bill Invoice01. Free text field can bring attention to reason for credit etc.</cbc:Note><cbc:DocumentCurrencyCode>AUD</cbc:DocumentCurrencyCode><cbc:BuyerReference>Simple solar plan</cbc:BuyerReference><cac:InvoicePeriod><cbc:StartDate>2022-06-15</cbc:StartDate><cbc:EndDate>2022-07-15</cbc:EndDate></cac:InvoicePeriod><cac:BillingReference><cac:InvoiceDocumentReference><cbc:ID>Invoice01</cbc:ID><cbc:IssueDate>2022-07-29</cbc:IssueDate></cac:InvoiceDocumentReference></cac:BillingReference><cac:AdditionalDocumentReference><cbc:ID>Invoice03.pdf</cbc:ID><cac:Attachment><cbc:EmbeddedDocumentBinaryObject mimeCode="application/pdf" filename="Invoice03.pdf">UGxhaW4gdGV4dCBpbiBwbGFjZSBvZiBwZGYgYXR0YWNobWVudCBmb3Igc2FtcGxlIGludm9pY2Vz</cbc:EmbeddedDocumentBinaryObject></cac:Attachment></cac:AdditionalDocumentReference><cac:AccountingSupplierParty><cac:Party><cbc:EndpointID schemeID="0151">47555222000</cbc:EndpointID><cac:PostalAddress><cbc:CityName>Harrison</cbc:CityName><cbc:PostalZone>2912</cbc:PostalZone><cbc:CountrySubentity>NSW</cbc:CountrySubentity><cac:Country><cbc:IdentificationCode>AU</cbc:IdentificationCode></cac:Country></cac:PostalAddress><cac:PartyLegalEntity><cbc:RegistrationName>Grey Roo Energy</cbc:RegistrationName><cbc:CompanyID schemeID="0151">47555222000</cbc:CompanyID></cac:PartyLegalEntity></cac:Party></cac:AccountingSupplierParty><cac:AccountingCustomerParty><cac:Party><cbc:EndpointID schemeID="0151">47555222000</cbc:EndpointID><cac:PartyIdentification><cbc:ID>AccountNumber123</cbc:ID></cac:PartyIdentification><cac:PostalAddress><cbc:StreetName>100 Queen Street</cbc:StreetName><cbc:CityName>Sydney</cbc:CityName><cbc:PostalZone>2000</cbc:PostalZone><cbc:CountrySubentity>NSW</cbc:CountrySubentity><cac:Country><cbc:IdentificationCode>AU</cbc:IdentificationCode></cac:Country></cac:PostalAddress><cac:PartyLegalEntity><cbc:RegistrationName>Trotters Incorporated</cbc:RegistrationName><cbc:CompanyID schemeID="0151">91888222000</cbc:CompanyID></cac:PartyLegalEntity><cac:Contact><cbc:Name>Lisa Johnson</cbc:Name></cac:Contact></cac:Party></cac:AccountingCustomerParty><cac:TaxTotal><cbc:TaxAmount currencyID="AUD">-15.94</cbc:TaxAmount><cac:TaxSubtotal><cbc:TaxableAmount currencyID="AUD">-159.43</cbc:TaxableAmount><cbc:TaxAmount currencyID="AUD">-15.94</cbc:TaxAmount><cac:TaxCategory><cbc:ID>S</cbc:ID><cbc:Percent>10</cbc:Percent><cac:TaxScheme><cbc:ID>GST</cbc:ID></cac:TaxScheme></cac:TaxCategory></cac:TaxSubtotal></cac:TaxTotal><cac:LegalMonetaryTotal><cbc:LineExtensionAmount currencyID="AUD">-159.43</cbc:LineExtensionAmount><cbc:TaxExclusiveAmount currencyID="AUD">-159.43</cbc:TaxExclusiveAmount><cbc:TaxInclusiveAmount currencyID="AUD">-175.37</cbc:TaxInclusiveAmount><cbc:PayableAmount currencyID="AUD">-175.37</cbc:PayableAmount></cac:LegalMonetaryTotal><cac:InvoiceLine><cbc:ID>1</cbc:ID><cbc:InvoicedQuantity unitCode="KWH">-325.2</cbc:InvoicedQuantity><cbc:LineExtensionAmount currencyID="AUD">-129.04</cbc:LineExtensionAmount><cac:Item><cbc:Name>Adjustment - reverse prior Electricity charges - all day rate NMI 9000074677</cbc:Name><cac:ClassifiedTaxCategory><cbc:ID>S</cbc:ID><cbc:Percent>10</cbc:Percent><cac:TaxScheme><cbc:ID>GST</cbc:ID></cac:TaxScheme></cac:ClassifiedTaxCategory></cac:Item><cac:Price><cbc:PriceAmount currencyID="AUD">0.3968</cbc:PriceAmount></cac:Price></cac:InvoiceLine><cac:InvoiceLine><cbc:ID>2</cbc:ID><cbc:InvoicedQuantity unitCode="DAY">-31</cbc:InvoicedQuantity><cbc:LineExtensionAmount currencyID="AUD">-30.39</cbc:LineExtensionAmount><cac:Item><cbc:Name>Adjustment - reverse prior Supply charge</cbc:Name><cac:ClassifiedTaxCategory><cbc:ID>S</cbc:ID><cbc:Percent>10</cbc:Percent><cac:TaxScheme><cbc:ID>GST</cbc:ID></cac:TaxScheme></cac:ClassifiedTaxCategory></cac:Item><cac:Price><cbc:PriceAmount currencyID="AUD">0.9803</cbc:PriceAmount></cac:Price></cac:InvoiceLine></Invoice>'

    res = client.get(
        INVOICE_HISTORY_PATH,
        headers={
            "Authorisation": user_token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200
    assert len(res.json) == 1

    res = client.get(
        f"{INVOICE_VALIDATE_PATH}?rules=AUNZ_PEPPOL_1_0_10&id={invoice_id}",
        headers={
            "Authorisation": user_token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200
    assert res.json["validationOutcome"][0]["validated"]

    res = client.post(
        f"{INVOICE_SEND_PATH}?xml_id={invoice_id}&target_email=TEST",
        headers={
            "Authorisation": user_token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200

    res = client.delete(
        f"{INVOICE_DELETE_PATH}/{invoice_id}",
        headers={
            "Authorisation": user_token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200

    res = client.get(
        INVOICE_HISTORY_PATH,
        headers={
            "Authorisation": user_token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200
    assert len(res.json) == 0

# Register -> Upload XML Validate (Success) -> History (Confirm 1 Exist) -> Send (Success) -> Delete -> History (Confirm 0 exists) 
def test_upload_xml_sequence(client):
    data = {
        "email": "abc@gmail.com",
        "password": "abc"
    }
    
    res = client.post(
        REGISTER_PATH, 
        data=json.dumps(data),
        content_type="application/json"
    )

    assert res.status_code == 201
    user_token = res.json["token"]

    data = {
        "rules": "AUNZ_PEPPOL_1_0_10",
        "files": [(io.BytesIO(TEST_DATA['GOOD_XML'].encode('UTF-8')), 'test.xml')]
    }

    res = client.post(
        INVOICE_UPLOAD_VALIDATE_PATH,
        headers={
            "Authorisation": user_token
        },
        data=data,  
        content_type='multipart/form-data',
    )
    
    assert res.status_code == 200
    assert res.json["validationOutcome"][0]["validated"]
    invoice_id = res.json['validationOutcome'][0]['invoiceId']

    res = client.get(
        INVOICE_HISTORY_PATH,
        headers={
            "Authorisation": user_token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200
    assert len(res.json) == 1

    res = client.post(
        f"{INVOICE_SEND_PATH}?xml_id={invoice_id}&target_email=TEST",
        headers={
            "Authorisation": user_token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200

    res = client.delete(
        f"{INVOICE_DELETE_PATH}/{invoice_id}",
        headers={
            "Authorisation": user_token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200

    res = client.get(
        INVOICE_HISTORY_PATH,
        headers={
            "Authorisation": user_token,
            "Content-Type": "application/json"
        }
    )

    assert res.status_code == 200
    assert len(res.json) == 0
