import base64
from src.services.conversion import ConversionService
import json
from models import Invoice
from src.services.utils import db_insert
from src.services.validation import ValidationService

template = """<?xml version="1.0" encoding="UTF-8"?><Invoice xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"><cbc:CustomizationID>urn:cen.eu:en16931:2017#conformant#urn:fdc:peppol.eu:2017:poacc:billing:international:aunz:3.0</cbc:CustomizationID><cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID><cbc:ID>{invoice_number}</cbc:ID><cbc:IssueDate>{issue_date}</cbc:IssueDate><cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode><cbc:Note>Taxinvoice</cbc:Note><cbc:DocumentCurrencyCode>AUD</cbc:DocumentCurrencyCode><cbc:BuyerReference>{note}</cbc:BuyerReference><cac:AccountingSupplierParty><cac:Party><cbc:EndpointID schemeID="0151">{seller_abn}</cbc:EndpointID><cac:PartyName><cbc:Name>{company_name}</cbc:Name></cac:PartyName><cac:PostalAddress><cbc:StreetName>{street_name}</cbc:StreetName>{additional_name}<cbc:CityName>{city_name}</cbc:CityName><cbc:PostalZone>{post_code}</cbc:PostalZone><cac:Country><cbc:IdentificationCode>{seller_country}</cbc:IdentificationCode></cac:Country></cac:PostalAddress><cac:PartyLegalEntity><cbc:RegistrationName>{company_name}</cbc:RegistrationName><cbc:CompanyID schemeID="0151">{seller_abn}</cbc:CompanyID></cac:PartyLegalEntity><cac:PartyTaxScheme><cbc:CompanyID>{seller_abn}</cbc:CompanyID><cac:TaxScheme><cbc:ID>GST</cbc:ID></cac:TaxScheme></cac:PartyTaxScheme></cac:Party></cac:AccountingSupplierParty><cac:AccountingCustomerParty><cac:Party><cbc:EndpointID schemeID="0151">{buyer_abn}</cbc:EndpointID><cac:PartyName><cbc:Name>{buyer_company_name}</cbc:Name></cac:PartyName><cac:PostalAddress><cbc:StreetName>{buyer_street_name}</cbc:StreetName>{buyer_additional_name}<cbc:CityName>{buyer_city_name}</cbc:CityName><cbc:PostalZone>{buyer_post_code}</cbc:PostalZone><cac:Country><cbc:IdentificationCode>{buyer_country}</cbc:IdentificationCode></cac:Country></cac:PostalAddress><cac:PartyLegalEntity><cbc:RegistrationName>{buyer_company_name}</cbc:RegistrationName><cbc:CompanyID schemeID="0151">{buyer_abn}</cbc:CompanyID></cac:PartyLegalEntity><cac:PartyTaxScheme><cac:TaxScheme><cbc:CompanyID>{buyer_abn}</cbc:CompanyID><cbc:ID>{tax_name}</cbc:ID></cac:TaxScheme></cac:PartyTaxScheme></cac:Party></cac:AccountingCustomerParty><cac:TaxTotal><cbc:TaxAmount currencyID="AUD">{tax_per}</cbc:TaxAmount><cac:TaxSubtotal><cbc:TaxableAmount currencyID="AUD">{total_tax}</cbc:TaxableAmount><cbc:TaxAmount currencyID="AUD">{tax_per}</cbc:TaxAmount><cac:TaxCategory><cbc:ID>S</cbc:ID><cbc:Percent>{tax_per}</cbc:Percent><cac:TaxScheme><cbc:ID>{tax_name}</cbc:ID></cac:TaxScheme></cac:TaxCategory></cac:TaxSubtotal></cac:TaxTotal><cac:LegalMonetaryTotal><cbc:LineExtensionAmount currencyID="AUD">{total_without_tax}</cbc:LineExtensionAmount><cbc:TaxExclusiveAmount currencyID="AUD">{total_without_tax}</cbc:TaxExclusiveAmount><cbc:TaxInclusiveAmount currencyID="AUD">{total_after_tax}</cbc:TaxInclusiveAmount><cbc:PayableAmount currencyID="AUD">{total_after_tax}</cbc:PayableAmount></cac:LegalMonetaryTotal>{products}</Invoice>
"""
item_format = '<cac:InvoiceLine><cbc:ID>{item_id}</cbc:ID><cbc:InvoicedQuantity unitCode="{unit_code}">{amount_product}</cbc:InvoicedQuantity><cbc:LineExtensionAmount currencyID="AUD">{cost_product}</cbc:LineExtensionAmount><cac:Item>{item_description}<cbc:Name>{item_name}</cbc:Name><cac:ClassifiedTaxCategory><cbc:ID>GST</cbc:ID><cbc:Percent>{tax_amount}</cbc:Percent><cac:TaxScheme><cbc:ID>{tax_name}</cbc:ID></cac:TaxScheme></cac:ClassifiedTaxCategory></cac:Item><cac:Price><cbc:PriceAmount currencyID="AUD">{cost_per_product}</cbc:PriceAmount></cac:Price></cac:InvoiceLine>'

def fix_optional(name, value):
    if value == "" or value == None:
        return ""
    else:
        return f"<cbc:{name}>{value}</cbc:{name}>"
    
def create_xml(file, user):
    json_val = format_xml(file)

    invoice_name = file["invoiceName"] + ".xml"
    invoice = Invoice(name=invoice_name, fields=json.loads(json_val),  rule="AUNZ_PEPPOL_1_0_10", user_id=user.id, is_ready=False, is_gui=True)

    db_insert(invoice)
    
    return {"filename": invoice.name, "invoiceId": invoice.id} 
 
def format_xml(file):
    products = ""
    for no, item in enumerate(file["invoiceItems"]):
        description = fix_optional("Description", item["description"])
        products += item_format.format(
            item_id = no,
            item_name = item["item"],
            unit_code = item["unitCode"],
            item_description = description,
            amount_product = item["quantity"] ,
            cost_per_product = item["totalPrice"],
            cost_product = item["totalPrice"],
            tax_amount = item["GST"],
            tax_name = "GST",
        )
    try:
        seller_ad_name = fix_optional("AdditionalStreetName", file["seller"]["address"]["additionalStreetName"])
        buyer_ad_name = fix_optional("AdditionalStreetName", file["buyer"]["address"]["additionalStreetName"])
        content = template.format(
            invoice_number=file["invoiceNumber"],
            issue_date=file["invoiceIssueDate"], 
            note=file["invoiceName"],
            seller_abn=file["seller"]["ABN"], 
            company_name=file["seller"]["companyName"],
            street_name=file["seller"]["address"]["streetName"], 
            seller_country=file["seller"]["address"]["country"],
            additional_name=seller_ad_name,
            city_name=file["seller"]["address"]["cityName"], 
            post_code=file["seller"]["address"]["postalCode"],
            buyer_abn=file["buyer"]["ABN"], 
            buyer_company_name=file["buyer"]["companyName"],
            buyer_street_name=file["buyer"]["address"]["streetName"], 
            buyer_additional_name=buyer_ad_name,
            buyer_city_name=file["buyer"]["address"]["cityName"],
            buyer_post_code=file["buyer"]["address"]["postalCode"],
            buyer_country=file["buyer"]["address"]["country"],
            products=products,
            tax_name="GST",
            tax_per=file["buyerVatRate"],
            total_tax=file["totalGST"],
            total_without_tax=file["totalTaxable"],
            total_after_tax=file["totalAmount"]
        )
    except Exception as e:
        raise Exception(f"Couldn't make UBL: {str(e)}")
    cs = ConversionService()
    json_val = {}
    try:
        json_val = cs.xml_to_json(content)
    except Exception as e:
        print(f"ERROR: {e}")
    
    return json_val

if __name__ == "__main__":
    create_xml("test")