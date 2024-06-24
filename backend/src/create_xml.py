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
            <!-- seller ABN -->
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
                <!-- seller ABN -->
            </cac:PartyLegalEntity>
            <cac:PartyTaxScheme>
                <cbc:CompanyID>{seller_abn}</cbc:CompanyID>
                <!-- seller ABN -->
                <cac:TaxScheme>
                    <cbc:ID>GST</cbc:ID>
                </cac:TaxScheme>
            </cac:PartyTaxScheme>
        </cac:Party>
    </cac:AccountingSupplierParty>
    <cac:AccountingCustomerParty>
        <cac:Party>
            <cbc:EndpointID schemeID="0151">{buyer_abn}</cbc:EndpointID>
            <!-- Buyer/customer ABN -->
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
                <!-- Buyer/customer ABN -->
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
        <cbc:LineExtensionAmount currencyID="AUD">{total_tax}</cbc:LineExtensionAmount>
        <cbc:TaxExclusiveAmount currencyID="AUD">{total_tax}</cbc:TaxExclusiveAmount>
        <cbc:TaxInclusiveAmount currencyID="AUD">{total_after_tax}</cbc:TaxInclusiveAmount>
        <cbc:PayableAmount currencyID="AUD">{total_after_tax}</cbc:PayableAmount>
    </cac:LegalMonetaryTotal>
    <cac:InvoiceLine>
        <cbc:ID>1</cbc:ID>
        <cbc:Note>Texts Giving More Info about the Invoice Line</cbc:Note>
        <cbc:InvoicedQuantity unitCode="E99">{amount_product}</cbc:InvoicedQuantity>
        <cbc:LineExtensionAmount currencyID="AUD">{cost_product}</cbc:LineExtensionAmount>
        <cac:Item>
            <cbc:Description>{name_product}</cbc:Description>
            <!-- optional -->
            <cbc:Name>True-Widgets</cbc:Name>
            <cac:ClassifiedTaxCategory>
                <cbc:ID>S</cbc:ID>
                <cbc:Percent>{tax_amount}</cbc:Percent>
                <cac:TaxScheme>
                    <cbc:ID>{tax_name}</cbc:ID>
                </cac:TaxScheme>
            </cac:ClassifiedTaxCategory>
        </cac:Item>
        <cac:Price>
            <cbc:PriceAmount currencyID="AUD">{cost_product}</cbc:PriceAmount>
        </cac:Price>
    </cac:InvoiceLine>
    <cac:InvoiceLine>
        <cbc:ID>1</cbc:ID>
        <cbc:Note>Texts Giving More Info about the Invoice Line</cbc:Note>
        <cbc:InvoicedQuantity unitCode="E99">{amount_product}</cbc:InvoicedQuantity>
        <cbc:LineExtensionAmount currencyID="AUD">{cost_product}</cbc:LineExtensionAmount>
        <cac:Item>
            <cbc:Description>Widgets True and Fair</cbc:Description>
            <cbc:Name>True-Widgets</cbc:Name>
            <cac:ClassifiedTaxCategory>
                <cbc:ID>S</cbc:ID>
                <cbc:Percent>{tax_amount}</cbc:Percent>
                <cac:TaxScheme>
                    <cbc:ID>{tax_name}</cbc:ID>
                </cac:TaxScheme>
            </cac:ClassifiedTaxCategory>
        </cac:Item>
        <cac:Price>
            <cbc:PriceAmount currencyID="AUD">{cost_product}</cbc:PriceAmount>
        </cac:Price>
    </cac:InvoiceLine>
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
    </Invoice>
"""



def create_xml(file):
    variable1 = "test"
    variable2 = "test" 
    variable3 = "test" 
    variable4 = "test" 

    variable5 = 8008 

    content = template.format(
        issue_date=variable5, 
        note=variable2, 
        seller_abn=variable5, 
        company_name=variable4,
        street_name=variable3, 
        additional_name=variable4,
        city_name=variable3, 
        post_code=variable5,
        buyer_abn=variable5, 
        buyer_company_name=variable4,
        buyer_city_name=variable4,
        buyer_post_code=variable5,
        buyer_street_name=variable3, 
        buyer_additional_name=variable4,
        tax_name=variable3, 
        tax_per=variable4,
        total_tax=variable5, 
        total_after_tax=variable5,
        amount_product=variable5, 
        cost_product=variable5,
        name_product=variable5,
        tax_amount=variable5
    )

    with open('output.xml', 'w') as file:
        file.write(content)

if __name__ == "__main__":
    create_xml("test")