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
                <cbc:Percent>{tax_amount}</cbc:Percent>
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
item = """<cac:InvoiceLine>
    <cbc:ID>{item_id}</cbc:ID>
    <cbc:Note>Texts Giving More Info about the Invoice Line</cbc:Note>
    <cbc:InvoicedQuantity unitCode="E99">{amount_product}</cbc:InvoicedQuantity>
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


def create_xml(file):
    products = ""
    for item, no in enumerate(file["invoiceItems"]):
        products += items.format(
            item_id = no
            item_name = item["item"]
            item_description = item["description"]
            amount_product = item["quantity"] 
            cost_per_product = item["unitPrice"]
            cost_product = item["totalPrice"]
            tax_amount = 10
            tax_name = item["GST"]
        )

    content = template.format(
        issue_date=file["invoiceIssueDate"], 
        note=variable2, 
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
        buyer_post_code=["buyer"]["address"]["postalCode"],
        products=products
    )

    with open('output.xml', 'w') as file:
        file.write(content)

if __name__ == "__main__":
    create_xml("test")