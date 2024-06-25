import pytest
import json
import base64

from tests.fixtures import client
from src.validation import validate_xml,generate_token

VALIDATION_PATH = "/validation/validation"



def test_xml_validate_function_success(client):
    data = '''<?xml version="1.0" encoding="UTF-8"?>
        <Invoice xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
            xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"
            xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2">
            <cbc:CustomizationID>urn:cen.eu:en16931:2017#conformant#urn:fdc:peppol.eu:2017:poacc:billing:international:aunz:3.0</cbc:CustomizationID>
            <cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID>
            <cbc:ID>Invoice01</cbc:ID>
            <cbc:IssueDate>2019-07-29</cbc:IssueDate>
            <cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
            <cbc:Note>Tax invoice</cbc:Note>
            <cbc:DocumentCurrencyCode>AUD</cbc:DocumentCurrencyCode>
            <cbc:BuyerReference>Simple solar plan</cbc:BuyerReference>
            <cac:AccountingSupplierParty>
                <cac:Party>
                    <cbc:EndpointID schemeID="0151">47555222000</cbc:EndpointID>
                    <cac:PartyName>
                        <cbc:Name>Windows to Fit Pty Ltd</cbc:Name>
                    </cac:PartyName>
                    <cac:PostalAddress>
                        <cbc:StreetName>Main street 1</cbc:StreetName>
                        <cbc:AdditionalStreetName>Postbox 123</cbc:AdditionalStreetName>
                        <cbc:CityName>Harrison</cbc:CityName>
                        <cbc:PostalZone>2912</cbc:PostalZone>
                        <cac:Country>
                            <cbc:IdentificationCode>AU</cbc:IdentificationCode>
                        </cac:Country>
                    </cac:PostalAddress>
                    <cac:PartyLegalEntity>
                        <cbc:RegistrationName>Windows to Fit Pty Ltd</cbc:RegistrationName>
                        <cbc:CompanyID schemeID="0151">47555222000</cbc:CompanyID>
                    </cac:PartyLegalEntity>
                    <cac:PartyTaxScheme>
                        <cbc:CompanyID>47555222000</cbc:CompanyID>
                        <cac:TaxScheme>
                            <cbc:ID>GST</cbc:ID>
                        </cac:TaxScheme>
                    </cac:PartyTaxScheme>
                </cac:Party>
            </cac:AccountingSupplierParty>
            <cac:AccountingCustomerParty>
                <cac:Party>
                    <cbc:EndpointID schemeID="0151">91888222000</cbc:EndpointID>
                    <cac:PartyName>
                        <cbc:Name>Trotters Trading Co Ltd</cbc:Name>
                    </cac:PartyName>
                    <cac:PostalAddress>
                        <cbc:StreetName>100 Queen Street</cbc:StreetName>
                        <cbc:AdditionalStreetName>Po box 878</cbc:AdditionalStreetName>
                        <cbc:CityName>Sydney</cbc:CityName>
                        <cbc:PostalZone>2000</cbc:PostalZone>
                        <cac:Country>
                            <cbc:IdentificationCode>AU</cbc:IdentificationCode>
                        </cac:Country>
                    </cac:PostalAddress>
                    <cac:PartyLegalEntity>
                        <cbc:RegistrationName>Trotters Incorporated</cbc:RegistrationName>
                        <cbc:CompanyID schemeID="0151">91888222000</cbc:CompanyID>
                    </cac:PartyLegalEntity>
                    <cac:PartyTaxScheme>
                        <cac:TaxScheme>
                            <cbc:CompanyID>91888222000</cbc:CompanyID>
                            <cbc:ID>GST</cbc:ID>
                        </cac:TaxScheme>
                    </cac:PartyTaxScheme>
                </cac:Party>
            </cac:AccountingCustomerParty>
            <cac:TaxTotal>
                <cbc:TaxAmount currencyID="AUD">148.74</cbc:TaxAmount>
                <cac:TaxSubtotal>
                    <cbc:TaxableAmount currencyID="AUD">1487.40</cbc:TaxableAmount>
                    <cbc:TaxAmount currencyID="AUD">148.74</cbc:TaxAmount>
                    <cac:TaxCategory>
                        <cbc:ID>S</cbc:ID>
                        <cbc:Percent>10</cbc:Percent>
                        <cac:TaxScheme>
                            <cbc:ID>GST</cbc:ID>
                        </cac:TaxScheme>
                    </cac:TaxCategory>
                </cac:TaxSubtotal>
            </cac:TaxTotal>
            <cac:LegalMonetaryTotal>
                <cbc:LineExtensionAmount currencyID="AUD">1487.40</cbc:LineExtensionAmount>
                <cbc:TaxExclusiveAmount currencyID="AUD">1487.40</cbc:TaxExclusiveAmount>
                <cbc:TaxInclusiveAmount currencyID="AUD">1636.14</cbc:TaxInclusiveAmount>
                <cbc:PayableAmount currencyID="AUD">1636.14</cbc:PayableAmount>
            </cac:LegalMonetaryTotal>
            <cac:InvoiceLine>
                <cbc:ID>1</cbc:ID>
                <cbc:Note>Texts Giving More Info about the Invoice Line</cbc:Note>
                <cbc:InvoicedQuantity unitCode="E99">10</cbc:InvoicedQuantity>
                <cbc:LineExtensionAmount currencyID="AUD">299.90</cbc:LineExtensionAmount>
                <cac:Item>
                    <cbc:Description>Widgets True and Fair</cbc:Description>
                    <cbc:Name>True-Widgets</cbc:Name>
                    <cac:ClassifiedTaxCategory>
                        <cbc:ID>S</cbc:ID>
                        <cbc:Percent>10</cbc:Percent>
                        <cac:TaxScheme>
                            <cbc:ID>GST</cbc:ID>
                        </cac:TaxScheme>
                    </cac:ClassifiedTaxCategory>
                </cac:Item>
                <cac:Price>
                    <cbc:PriceAmount currencyID="AUD">29.99</cbc:PriceAmount>
                </cac:Price>
            </cac:InvoiceLine>
            <!-- Additional InvoiceLines omitted for brevity -->
        </Invoice>
'''
    encoded_data = base64.b64encode(data.encode('utf-8')).decode('utf-8')

    result = validate_xml("test.xml", encoded_data, ["AUNZ_PEPPOL_1_0_10"])
    
    assert result["successful"] is True






def test_xml_validate_success(client):
    data = {
        """<?xml version="1.0" encoding="UTF-8"?>
        <Invoice xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
            xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"
            xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2">
            <cbc:CustomizationID>urn:cen.eu:en16931:2017#conformant#urn:fdc:peppol.eu:2017:poacc:billing:international:aunz:3.0</cbc:CustomizationID>
            <cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID>
            <cbc:ID>Invoice01</cbc:ID>
            <cbc:IssueDate>2019-07-29</cbc:IssueDate>
            <cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
            <cbc:Note>Tax invoice</cbc:Note>
            <cbc:DocumentCurrencyCode>AUD</cbc:DocumentCurrencyCode>
            <cbc:BuyerReference>Simple solar plan</cbc:BuyerReference>
            <cac:AccountingSupplierParty>
                <cac:Party>
                    <cbc:EndpointID schemeID="0151">47555222000</cbc:EndpointID>
                    <cac:PartyName>
                        <cbc:Name>Windows to Fit Pty Ltd</cbc:Name>
                    </cac:PartyName>
                    <cac:PostalAddress>
                        <cbc:StreetName>Main street 1</cbc:StreetName>
                        <cbc:AdditionalStreetName>Postbox 123</cbc:AdditionalStreetName>
                        <cbc:CityName>Harrison</cbc:CityName>
                        <cbc:PostalZone>2912</cbc:PostalZone>
                        <cac:Country>
                            <cbc:IdentificationCode>AU</cbc:IdentificationCode>
                        </cac:Country>
                    </cac:PostalAddress>
                    <cac:PartyLegalEntity>
                        <cbc:RegistrationName>Windows to Fit Pty Ltd</cbc:RegistrationName>
                        <cbc:CompanyID schemeID="0151">47555222000</cbc:CompanyID>
                    </cac:PartyLegalEntity>
                    <cac:PartyTaxScheme>
                        <cbc:CompanyID>47555222000</cbc:CompanyID>
                        <cac:TaxScheme>
                            <cbc:ID>GST</cbc:ID>
                        </cac:TaxScheme>
                    </cac:PartyTaxScheme>
                </cac:Party>
            </cac:AccountingSupplierParty>
            <cac:AccountingCustomerParty>
                <cac:Party>
                    <cbc:EndpointID schemeID="0151">91888222000</cbc:EndpointID>
                    <cac:PartyName>
                        <cbc:Name>Trotters Trading Co Ltd</cbc:Name>
                    </cac:PartyName>
                    <cac:PostalAddress>
                        <cbc:StreetName>100 Queen Street</cbc:StreetName>
                        <cbc:AdditionalStreetName>Po box 878</cbc:AdditionalStreetName>
                        <cbc:CityName>Sydney</cbc:CityName>
                        <cbc:PostalZone>2000</cbc:PostalZone>
                        <cac:Country>
                            <cbc:IdentificationCode>AU</cbc:IdentificationCode>
                        </cac:Country>
                    </cac:PostalAddress>
                    <cac:PartyLegalEntity>
                        <cbc:RegistrationName>Trotters Incorporated</cbc:RegistrationName>
                        <cbc:CompanyID schemeID="0151">91888222000</cbc:CompanyID>
                    </cac:PartyLegalEntity>
                    <cac:PartyTaxScheme>
                        <cac:TaxScheme>
                            <cbc:CompanyID>91888222000</cbc:CompanyID>
                            <cbc:ID>GST</cbc:ID>
                        </cac:TaxScheme>
                    </cac:PartyTaxScheme>
                </cac:Party>
            </cac:AccountingCustomerParty>
            <cac:TaxTotal>
                <cbc:TaxAmount currencyID="AUD">148.74</cbc:TaxAmount>
                <cac:TaxSubtotal>
                    <cbc:TaxableAmount currencyID="AUD">1487.40</cbc:TaxableAmount>
                    <cbc:TaxAmount currencyID="AUD">148.74</cbc:TaxAmount>
                    <cac:TaxCategory>
                        <cbc:ID>S</cbc:ID>
                        <cbc:Percent>10</cbc:Percent>
                        <cac:TaxScheme>
                            <cbc:ID>GST</cbc:ID>
                        </cac:TaxScheme>
                    </cac:TaxCategory>
                </cac:TaxSubtotal>
            </cac:TaxTotal>
            <cac:LegalMonetaryTotal>
                <cbc:LineExtensionAmount currencyID="AUD">1487.40</cbc:LineExtensionAmount>
                <cbc:TaxExclusiveAmount currencyID="AUD">1487.40</cbc:TaxExclusiveAmount>
                <cbc:TaxInclusiveAmount currencyID="AUD">1636.14</cbc:TaxInclusiveAmount>
                <cbc:PayableAmount currencyID="AUD">1636.14</cbc:PayableAmount>
            </cac:LegalMonetaryTotal>
            <cac:InvoiceLine>
                <cbc:ID>1</cbc:ID>
                <cbc:Note>Texts Giving More Info about the Invoice Line</cbc:Note>
                <cbc:InvoicedQuantity unitCode="E99">10</cbc:InvoicedQuantity>
                <cbc:LineExtensionAmount currencyID="AUD">299.90</cbc:LineExtensionAmount>
                <cac:Item>
                    <cbc:Description>Widgets True and Fair</cbc:Description>
                    <cbc:Name>True-Widgets</cbc:Name>
                    <cac:ClassifiedTaxCategory>
                        <cbc:ID>S</cbc:ID>
                        <cbc:Percent>10</cbc:Percent>
                        <cac:TaxScheme>
                            <cbc:ID>GST</cbc:ID>
                        </cac:TaxScheme>
                    </cac:ClassifiedTaxCategory>
                </cac:Item>
                <cac:Price>
                    <cbc:PriceAmount currencyID="AUD">29.99</cbc:PriceAmount>
                </cac:Price>
            </cac:InvoiceLine>
            <!-- Additional InvoiceLines omitted for brevity -->
        </Invoice>"""
    }
    data_list = list(data)
    res = client.post(
        VALIDATION_PATH,
        data=json.dumps(data_list),
        content_type="application/json"
    )
  
    assert res.status_code == 201


def test_empty_xml_fail(client):
    data = {}
    res = client.post(
        VALIDATION_PATH,
        data=json.dumps(data),
        content_type="application/json"
    )
  
    assert res.status_code == 400

def test_xml_missing_data_fail(client):
    data = {
        """<?xml version="1.0" encoding="UTF-8"?>
        <Invoice xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
            xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"
            xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2">
            <cbc:CustomizationID>urn:cen.eu:en16931:2017#conformant#urn:fdc:peppol.eu:2017:poacc:billing:international:aunz:3.0</cbc:CustomizationID>
            <cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID>
            <cbc:ID>Invoice01</cbc:ID>
            <cbc:IssueDate>2019-07-29</cbc:IssueDate>
            <cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
            <cbc:Note>Tax invoice</cbc:Note>
            <cbc:DocumentCurrencyCode>AUD</cbc:DocumentCurrencyCode>
            <cbc:BuyerReference>Simple solar plan</cbc:BuyerReference>
            <cac:AccountingSupplierParty>
                <cac:Party>
                    <cbc:EndpointID schemeID="0151">47555222000</cbc:EndpointID>
                    <cac:PostalAddress>
                        <cbc:StreetName>Main street 1</cbc:StreetName>
                        <cbc:AdditionalStreetName>Postbox 123</cbc:AdditionalStreetName>
                        <cbc:CityName>Harrison</cbc:CityName>
                        <cbc:PostalZone>2912</cbc:PostalZone>
                        <cac:Country>
                            <cbc:IdentificationCode>AU</cbc:IdentificationCode>
                        </cac:Country>
                    </cac:PostalAddress>
                    <cac:PartyLegalEntity>
                        <cbc:RegistrationName>Windows to Fit Pty Ltd</cbc:RegistrationName>
                        <cbc:CompanyID schemeID="0151">47555222000</cbc:CompanyID>
                    </cac:PartyLegalEntity>
                    <cac:PartyTaxScheme>
                        <cbc:CompanyID>47555222000</cbc:CompanyID>
                        <cac:TaxScheme>
                            <cbc:ID>GST</cbc:ID>
                        </cac:TaxScheme>
                    </cac:PartyTaxScheme>
                </cac:Party>
            </cac:AccountingSupplierParty>
            <cac:AccountingCustomerParty>
                <cac:Party>
                    <cbc:EndpointID schemeID="0151">91888222000</cbc:EndpointID>
                    <cac:PartyLegalEntity>
                        <cbc:RegistrationName>Trotters Incorporated</cbc:RegistrationName>
                        <cbc:CompanyID schemeID="0151">91888222000</cbc:CompanyID>
                    </cac:PartyLegalEntity>
                    <cac:PartyTaxScheme>
                        <cac:TaxScheme>
                            <cbc:CompanyID>91888222000</cbc:CompanyID>
                            <cbc:ID>GST</cbc:ID>
                        </cac:TaxScheme>
                    </cac:PartyTaxScheme>
                </cac:Party>
            </cac:AccountingCustomerParty>
            <cac:TaxTotal>
                <cbc:TaxAmount currencyID="AUD">148.74</cbc:TaxAmount>
                <cac:TaxSubtotal>
                    <cbc:TaxableAmount currencyID="AUD">1487.40</cbc:TaxableAmount>
                    <cbc:TaxAmount currencyID="AUD">148.74</cbc:TaxAmount>
                    <cac:TaxCategory>
                        <cbc:ID>S</cbc:ID>
                        <cbc:Percent>10</cbc:Percent>
                        <cac:TaxScheme>
                            <cbc:ID>GST</cbc:ID>
                        </cac:TaxScheme>
                    </cac:TaxCategory>
                </cac:TaxSubtotal>
            </cac:TaxTotal>
            <cac:InvoiceLine>
                <cbc:ID>1</cbc:ID>
                <cbc:Note>Texts Giving More Info about the Invoice Line</cbc:Note>
                <cbc:InvoicedQuantity unitCode="E99">10</cbc:InvoicedQuantity>
                <cbc:LineExtensionAmount currencyID="AUD">299.90</cbc:LineExtensionAmount>
                <cac:Price>
                    <cbc:PriceAmount currencyID="AUD">29.99</cbc:PriceAmount>
                </cac:Price>
            </cac:InvoiceLine>
            <!-- Additional InvoiceLines omitted for brevity -->
        </Invoice>"""
    }
    my_list = list(data)
    res = client.post(
        VALIDATION_PATH,
        data=json.dumps(my_list),
        content_type="application/json"
    )
  
  
    assert res.status_code == 400