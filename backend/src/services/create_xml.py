from flask import Flask, request, jsonify, make_response
from flask_restx import Namespace, Resource, fields

from models import db, Invoice
from src.services.utils import db_insert
from src.services.validation import ValidationService
import base64


template = """<Invoice xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2">
    <cbc:CustomizationID>urn:cen.eu:en16931:2017#conformant#urn:fdc:peppol.eu:2017:poacc:billing:international:aunz:3.0</cbc:CustomizationID>
    <cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID>
    <cbc:ID>Invoice01</cbc:ID>
    <cbc:IssueDate>{issue_date}</cbc:IssueDate>
    <cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
    <cbc:Note>Tax invoice</cbc:Note>
    <cbc:DocumentCurrencyCode>AUD</cbc:DocumentCurrencyCode>
    <cbc:BuyerReference>{note}</cbc:BuyerReference>
    <cac:AccountingSupplierParty>
        <cac:Party>
            <cbc:EndpointID schemeID="0151">{seller_abn}</cbc:EndpointID>
            <cac:PartyName>
                <cbc:Name>{company_name}</cbc:Name>
            </cac:PartyName>
            <cac:PostalAddress>
                <cbc:StreetName>{street_name}</cbc:StreetName>
                <cbc:AdditionalStreetName>{additional_name}</cbc:AdditionalStreetName>
                <cbc:CityName>{city_name}</cbc:CityName>
                <cbc:PostalZone>{post_code}</cbc:PostalZone>
                <cac:Country>
                    <cbc:IdentificationCode>AU</cbc:IdentificationCode>
                </cac:Country>
            </cac:PostalAddress>
            <cac:PartyLegalEntity>
                <cbc:RegistrationName>{company_name}</cbc:RegistrationName>
                <cbc:CompanyID schemeID="0151">{seller_abn}</cbc:CompanyID>
            </cac:PartyLegalEntity>
            <cac:PartyTaxScheme>
                <cbc:CompanyID>{seller_abn}</cbc:CompanyID>
                <cac:TaxScheme>
                    <cbc:ID>GST</cbc:ID>
                </cac:TaxScheme>
            </cac:PartyTaxScheme>
        </cac:Party>
    </cac:AccountingSupplierParty>
    <cac:AccountingCustomerParty>
        <cac:Party>
            <cbc:EndpointID schemeID="0151">{buyer_abn}</cbc:EndpointID>
            <cac:PartyName>
                <cbc:Name>{buyer_company_name}</cbc:Name>
            </cac:PartyName>
            <cac:PostalAddress>
                <cbc:StreetName>{buyer_street_name}</cbc:StreetName>
                <cbc:AdditionalStreetName>{buyer_additional_name}</cbc:AdditionalStreetName>
                <cbc:CityName>{buyer_city_name}</cbc:CityName>
                <cbc:PostalZone>{buyer_post_code}</cbc:PostalZone>
                <cac:Country>
                    <cbc:IdentificationCode>AU</cbc:IdentificationCode>
                </cac:Country>
            </cac:PostalAddress>
            <cac:PartyLegalEntity>
                <cbc:RegistrationName>{buyer_company_name}</cbc:RegistrationName>
                <cbc:CompanyID schemeID="0151">{buyer_abn}</cbc:CompanyID>
            </cac:PartyLegalEntity>
            <cac:PartyTaxScheme>
                <cac:TaxScheme>
                    <cbc:CompanyID>{buyer_abn}</cbc:CompanyID>
                    <cbc:ID>{tax_name}</cbc:ID>
                </cac:TaxScheme>
            </cac:PartyTaxScheme>
        </cac:Party>
    </cac:AccountingCustomerParty>
    <cac:TaxTotal>
        <cbc:TaxAmount currencyID="AUD">{tax_per}</cbc:TaxAmount>
        <cac:TaxSubtotal>
            <cbc:TaxableAmount currencyID="AUD">{total_tax}</cbc:TaxableAmount>
            <cbc:TaxAmount currencyID="AUD">{tax_per}</cbc:TaxAmount>
            <cac:TaxCategory>
                <cbc:ID>S</cbc:ID>
                <cbc:Percent>{tax_per}</cbc:Percent>
                <cac:TaxScheme>
                    <cbc:ID>{tax_name}</cbc:ID>
                </cac:TaxScheme>
            </cac:TaxCategory>
        </cac:TaxSubtotal>
    </cac:TaxTotal>
    <cac:LegalMonetaryTotal>
        <cbc:LineExtensionAmount currencyID="AUD">{total_without_tax}</cbc:LineExtensionAmount>
        <cbc:TaxExclusiveAmount currencyID="AUD">{total_without_tax}</cbc:TaxExclusiveAmount>
        <cbc:TaxInclusiveAmount currencyID="AUD">{total_after_tax}</cbc:TaxInclusiveAmount>
        <cbc:PayableAmount currencyID="AUD">{total_after_tax}</cbc:PayableAmount>
    </cac:LegalMonetaryTotal>
    {products}
    </Invoice>
"""
item_format = """<cac:InvoiceLine>
    <cbc:ID>{item_id}</cbc:ID>
    <cbc:Note>Texts Giving More Info about the Invoice Line</cbc:Note>
    <cbc:InvoicedQuantity unitCode={unit_code}>{amount_product}</cbc:InvoicedQuantity>
    <cbc:LineExtensionAmount currencyID="AUD">{cost_product}</cbc:LineExtensionAmount>
    <cac:Item>
        <cbc:Description>{item_description}</cbc:Description>
        <cbc:Name>{item_name}</cbc:Name>
        <cac:ClassifiedTaxCategory>
            <cbc:ID>S</cbc:ID>
            <cbc:Percent>{tax_amount}</cbc:Percent>
            <cac:TaxScheme>
                <cbc:ID>{tax_name}</cbc:ID>
            </cac:TaxScheme>
        </cac:ClassifiedTaxCategory>
    </cac:Item>
    <cac:Price>
        <cbc:PriceAmount currencyID="AUD">{cost_per_product}</cbc:PriceAmount>
    </cac:Price>
</cac:InvoiceLine>
"""


json_format = {
    "json": '{"ID":"Invoice03","IssueDate":"{issue_date}","InvoiceTypeCode":"380","Note":"Adjustment note to reverse prior bill Invoice01. Free text field can bring attention to reason for credit etc.","DocumentCurrencyCode":"AUD","BuyerReference":"{}","InvoicePeriod":{"StartDate":"2022-06-15","EndDate":"2022-07-15"},"BillingReference":{"InvoiceDocumentReference":{"ID":"Invoice01","IssueDate":"2022-07-29"}},"AdditionalDocumentReference":{"ID":"Invoice03.pdf","Attachment":{"EmbeddedDocumentBinaryObject":{"mimeCode":"application/pdf","filename":"Invoice03.pdf","value":"UGxhaW4gdGV4dCBpbiBwbGFjZSBvZiBwZGYgYXR0YWNobWVudCBmb3Igc2FtcGxlIGludm9pY2Vz"}}},"AccountingSupplierParty":{"Party":{"EndpointID":{"schemeID":"0151","value":"47555222000"},"PostalAddress":{"CityName":"Harrison","PostalZone":"2912","CountrySubentity":"NSW","Country":{"IdentificationCode":"AU"}},"PartyLegalEntity":{"RegistrationName":"Grey Roo Energy","CompanyID":{"schemeID":"0151","value":"47555222000"}}}},"AccountingCustomerParty":{"Party":{"EndpointID":{"schemeID":"0151","value":"47555222000"},"PartyIdentification":{"ID":"AccountNumber123"},"PostalAddress":{"StreetName":"100 Queen Street","CityName":"Sydney","PostalZone":"2000","CountrySubentity":"NSW","Country":{"IdentificationCode":"AU"}},"PartyLegalEntity":{"RegistrationName":"Trotters Incorporated","CompanyID":{"schemeID":"0151","value":"91888222000"}},"Contact":{"Name":"Lisa Johnson"}}},"TaxTotal":{"TaxAmount":{"currencyID":"AUD","value":"-15.94"},"TaxSubtotal":{"TaxableAmount":{"currencyID":"AUD","value":"-159.43"},"TaxAmount":{"currencyID":"AUD","value":"-15.94"},"TaxCategory":{"ID":"S","Percent":"10","TaxScheme":{"ID":"GST"}}}},"LegalMonetaryTotal":{"LineExtensionAmount":{"currencyID":"AUD","value":"-159.43"},"TaxExclusiveAmount":{"currencyID":"AUD","value":"-159.43"},"TaxInclusiveAmount":{"currencyID":"AUD","value":"-175.37"},"PayableAmount":{"currencyID":"AUD","value":"-175.37"}},"InvoiceLine":[{"ID":"1","InvoicedQuantity":{"unitCode":"KWH","value":"-325.2"},"LineExtensionAmount":{"currencyID":"AUD","value":"-129.04"},"Item":{"Name":"Adjustment - reverse prior Electricity charges - all day rate NMI 9000074677","ClassifiedTaxCategory":{"ID":"S","Percent":"10","TaxScheme":{"ID":"GST"}}},"Price":{"PriceAmount":{"currencyID":"AUD","value":"0.3968"}}},{"ID":"2","InvoicedQuantity":{"unitCode":"DAY","value":"-31"},"LineExtensionAmount":{"currencyID":"AUD","value":"-30.39"},"Item":{"Name":"Adjustment - reverse prior Supply charge","ClassifiedTaxCategory":{"ID":"S","Percent":"10","TaxScheme":{"ID":"GST"}}},"Price":{"PriceAmount":{"currencyID":"AUD","value":"0.9803"}}}]}'
}


def create_xml(file, user):
    products = ""
    for no, item in enumerate(file["invoiceItems"]):
        print(item)
        products += item_format.format(
            item_id = no,
            item_name = item["item"],
            unit_code = item["unitCode"],
            item_description = item["description"],
            amount_product = item["quantity"] ,
            cost_per_product = item["unitPrice"],
            cost_product = item["totalPrice"],
            tax_amount = item["GST"],
            tax_name = "GST",
        )
    try:
        content = template.format(
            issue_date=file["invoiceIssueDate"], 
            note=file["invoiceName"],
            seller_abn=file["seller"]["ABN"], 
            company_name=file["seller"]["companyName"],
            street_name=file["seller"]["address"]["streetName"], 
            additional_name=file["seller"]["address"]["additionalStreetName"],
            city_name=file["seller"]["address"]["cityName"], 
            post_code=file["seller"]["address"]["postalCode"],
            buyer_abn=file["buyer"]["ABN"], 
            buyer_company_name=file["buyer"]["companyName"],
            buyer_street_name=file["buyer"]["address"]["streetName"], 
            buyer_additional_name=file["buyer"]["address"]["additionalStreetName"],
            buyer_city_name=file["buyer"]["address"]["cityName"],
            buyer_post_code=file["buyer"]["address"]["postalCode"],
            products=products,
            tax_name="GST",
            tax_per=10,
            total_tax=file["totalGST"],
            total_without_tax=file["totalTaxable"],
            total_after_tax=file["totalAmount"]
        )
    except Exception as e:
        raise Exception(f"Couldn't make UBL: {str(e)}")
    

    content_encode = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    va = ValidationService()
    result = va.validate_xml("test.xml", content_encode, ["AUNZ_PEPPOL_1_0_10"])
    if result["successful"] == True:
        db_insert(Invoice(name=file["invoiceName"], fields=content,  rule="AUNZ_PEPPOL_1_0_10", user_id=user.id, is_ready=True))
        return content
    else:
        raise ValueError(result)
    
def save_xml(file, user):
    db_insert(Invoice(name="test", fields=file, user_id=user.id, is_ready=False))
    invoice = Invoice.query.where(Invoice.fields==file).first()
    return invoice.id

    # with open("output.xml", 'w') as file:
    #     file.write(content)
    # with open("output.xml", 'rb') as file:
    #     
if __name__ == "__main__":
    create_xml("test")