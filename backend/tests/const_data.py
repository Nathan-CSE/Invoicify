json_str_1 = '''
{
    "ID": "Invoice03",
    "IssueDate": "2022-07-31",
    "InvoiceTypeCode": "380",
    "Note": "Adjustment note to reverse prior bill Invoice01. Free text field can bring attention to reason for credit etc.",
    "DocumentCurrencyCode": "AUD",
    "BuyerReference": "Simple solar plan",
    "InvoicePeriod": {
        "StartDate": "2022-06-15",
        "EndDate":"2022-07-15"
    },
    "BillingReference": {
        "InvoiceDocumentReference": {
        "ID": "Invoice01",
        "IssueDate": "2022-07-29"
        }
    },
    "AdditionalDocumentReference": {
        "ID": "Invoice03.pdf",
        "Attachment": {
            "EmbeddedDocumentBinaryObject": {
                "mimeCode": "application/pdf",
                "filename": "Invoice03.pdf",
                "value": "UGxhaW4gdGV4dCBpbiBwbGFjZSBvZiBwZGYgYXR0YWNobWVudCBmb3Igc2FtcGxlIGludm9pY2Vz"
            }
        }
    },
    "AccountingSupplierParty": {
        "Party": {
            "EndpointID": {
                    "schemeID": "0151",
                    "value": "47555222000"
                },
            "PostalAddress": {
                "CityName": "Harrison",
                "PostalZone": "2912",
                "CountrySubentity": "NSW",
                "Country": {
                "IdentificationCode": "AU"
                }
            },
            "PartyLegalEntity": {
                "RegistrationName": "Grey Roo Energy",
                "CompanyID": {
                "schemeID": "0151",
                "value": "47555222000"
                }
            }
        }
    },
    "AccountingCustomerParty": {
        "Party": {
            "EndpointID": {
                "schemeID": "0151",
                "value": "47555222000"
            },
            "PartyIdentification": {
                "ID": "AccountNumber123"
            },
            "PostalAddress": {
                "StreetName": "100 Queen Street",
                "CityName": "Sydney",
                "PostalZone": "2000",
                "CountrySubentity": "NSW",
                "Country": {
                "IdentificationCode": "AU"
                }
            },
            "PartyLegalEntity": {
                "RegistrationName": "Trotters Incorporated",
                "CompanyID": {
                "schemeID": "0151",
                "value": "91888222000"
                }
            },
            "Contact": {
                "Name": "Lisa Johnson"
            }
        }
    },
    "TaxTotal": {
        "TaxAmount": {
            "currencyID": "AUD",
            "value": "-15.94"
        },
        "TaxSubtotal": {
            "TaxableAmount": {
                "currencyID": "AUD",
                "value": "-159.43"
            },
            "TaxAmount": {
                "currencyID": "AUD",
                "value": "-15.94"
            },
            "TaxCategory": {
                "ID": "S",
                "Percent": "10",
                "TaxScheme": {
                    "ID": "GST"
                }
            }
        }
    },
    "LegalMonetaryTotal": {
        "LineExtensionAmount": {
            "currencyID": "AUD",
            "value": "-159.43"
        },
        "TaxExclusiveAmount": {
            "currencyID": "AUD",
            "value": "-159.43"
        },
        "TaxInclusiveAmount": {
            "currencyID": "AUD",
            "value": "-175.37"
        },
        "PayableAmount": {
            "currencyID": "AUD",
            "value": "-175.37"
        }
    },
    "InvoiceLine": [
        {
            "ID": "1",
            "InvoicedQuantity": {
                "unitCode": "KWH",
                "value": "-325.2"
            },
            "LineExtensionAmount": {
                "currencyID": "AUD",
                "value": "-129.04"
            },
            "Item": {
                "Name": "Adjustment - reverse prior Electricity charges - all day rate NMI 9000074677",
                "ClassifiedTaxCategory": {
                    "ID": "S",
                    "Percent": "10",
                    "TaxScheme": {
                        "ID": "GST"
                    }
                }
            },
            "Price": {
                "PriceAmount": {
                "currencyID": "AUD",
                "value": "0.3968"
                }
            }
        },
        {
            "ID": "2",
            "InvoicedQuantity": {
                "unitCode": "DAY",
                "value": "-31"
            },
            "LineExtensionAmount": {
                "currencyID": "AUD",
                "value": "-30.39"
            },
            "Item": {
                "Name": "Adjustment - reverse prior Supply charge",
                    "ClassifiedTaxCategory": {
                    "ID": "S",
                    "Percent": "10",
                    "TaxScheme": {
                        "ID": "GST"
                    }
                }
            },
            "Price": {
                "PriceAmount": {
                "currencyID": "AUD",
                "value": "0.9803"
                }
            }
        }
    ]
}
'''

xml_from_json_str_1 = '<?xml version="1.0" encoding="UTF-8"?><Invoice xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"><cbc:CustomizationID>urn:cen.eu:en16931:2017#conformant#urn:fdc:peppol.eu:2017:poacc:billing:international:aunz:3.0</cbc:CustomizationID><cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID><cbc:ID>Invoice03</cbc:ID><cbc:IssueDate>2022-07-31</cbc:IssueDate><cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode><cbc:Note>Adjustment note to reverse prior bill Invoice01. Free text field can bring attention to reason for credit etc.</cbc:Note><cbc:DocumentCurrencyCode>AUD</cbc:DocumentCurrencyCode><cbc:BuyerReference>Simple solar plan</cbc:BuyerReference><cac:InvoicePeriod><cbc:StartDate>2022-06-15</cbc:StartDate><cbc:EndDate>2022-07-15</cbc:EndDate></cac:InvoicePeriod><cac:BillingReference><cac:InvoiceDocumentReference><cbc:ID>Invoice01</cbc:ID><cbc:IssueDate>2022-07-29</cbc:IssueDate></cac:InvoiceDocumentReference></cac:BillingReference><cac:AdditionalDocumentReference><cbc:ID>Invoice03.pdf</cbc:ID><cac:Attachment><cbc:EmbeddedDocumentBinaryObject mimeCode="application/pdf" filename="Invoice03.pdf">UGxhaW4gdGV4dCBpbiBwbGFjZSBvZiBwZGYgYXR0YWNobWVudCBmb3Igc2FtcGxlIGludm9pY2Vz</cbc:EmbeddedDocumentBinaryObject></cac:Attachment></cac:AdditionalDocumentReference><cac:AccountingSupplierParty><cac:Party><cbc:EndpointID schemeID="0151">47555222000</cbc:EndpointID><cac:PostalAddress><cbc:CityName>Harrison</cbc:CityName><cbc:PostalZone>2912</cbc:PostalZone><cbc:CountrySubentity>NSW</cbc:CountrySubentity><cac:Country><cbc:IdentificationCode>AU</cbc:IdentificationCode></cac:Country></cac:PostalAddress><cac:PartyLegalEntity><cbc:RegistrationName>Grey Roo Energy</cbc:RegistrationName><cbc:CompanyID schemeID="0151">47555222000</cbc:CompanyID></cac:PartyLegalEntity></cac:Party></cac:AccountingSupplierParty><cac:AccountingCustomerParty><cac:Party><cbc:EndpointID schemeID="0151">47555222000</cbc:EndpointID><cac:PartyIdentification><cbc:ID>AccountNumber123</cbc:ID></cac:PartyIdentification><cac:PostalAddress><cbc:StreetName>100 Queen Street</cbc:StreetName><cbc:CityName>Sydney</cbc:CityName><cbc:PostalZone>2000</cbc:PostalZone><cbc:CountrySubentity>NSW</cbc:CountrySubentity><cac:Country><cbc:IdentificationCode>AU</cbc:IdentificationCode></cac:Country></cac:PostalAddress><cac:PartyLegalEntity><cbc:RegistrationName>Trotters Incorporated</cbc:RegistrationName><cbc:CompanyID schemeID="0151">91888222000</cbc:CompanyID></cac:PartyLegalEntity><cac:Contact><cbc:Name>Lisa Johnson</cbc:Name></cac:Contact></cac:Party></cac:AccountingCustomerParty><cac:TaxTotal><cbc:TaxAmount currencyID="AUD">-15.94</cbc:TaxAmount><cac:TaxSubtotal><cbc:TaxableAmount currencyID="AUD">-159.43</cbc:TaxableAmount><cbc:TaxAmount currencyID="AUD">-15.94</cbc:TaxAmount><cac:TaxCategory><cbc:ID>S</cbc:ID><cbc:Percent>10</cbc:Percent><cac:TaxScheme><cbc:ID>GST</cbc:ID></cac:TaxScheme></cac:TaxCategory></cac:TaxSubtotal></cac:TaxTotal><cac:LegalMonetaryTotal><cbc:LineExtensionAmount currencyID="AUD">-159.43</cbc:LineExtensionAmount><cbc:TaxExclusiveAmount currencyID="AUD">-159.43</cbc:TaxExclusiveAmount><cbc:TaxInclusiveAmount currencyID="AUD">-175.37</cbc:TaxInclusiveAmount><cbc:PayableAmount currencyID="AUD">-175.37</cbc:PayableAmount></cac:LegalMonetaryTotal><cac:InvoiceLine><cbc:ID>1</cbc:ID><cbc:InvoicedQuantity unitCode="KWH">-325.2</cbc:InvoicedQuantity><cbc:LineExtensionAmount currencyID="AUD">-129.04</cbc:LineExtensionAmount><cac:Item><cbc:Name>Adjustment - reverse prior Electricity charges - all day rate NMI 9000074677</cbc:Name><cac:ClassifiedTaxCategory><cbc:ID>S</cbc:ID><cbc:Percent>10</cbc:Percent><cac:TaxScheme><cbc:ID>GST</cbc:ID></cac:TaxScheme></cac:ClassifiedTaxCategory></cac:Item><cac:Price><cbc:PriceAmount currencyID="AUD">0.3968</cbc:PriceAmount></cac:Price></cac:InvoiceLine><cac:InvoiceLine><cbc:ID>2</cbc:ID><cbc:InvoicedQuantity unitCode="DAY">-31</cbc:InvoicedQuantity><cbc:LineExtensionAmount currencyID="AUD">-30.39</cbc:LineExtensionAmount><cac:Item><cbc:Name>Adjustment - reverse prior Supply charge</cbc:Name><cac:ClassifiedTaxCategory><cbc:ID>S</cbc:ID><cbc:Percent>10</cbc:Percent><cac:TaxScheme><cbc:ID>GST</cbc:ID></cac:TaxScheme></cac:ClassifiedTaxCategory></cac:Item><cac:Price><cbc:PriceAmount currencyID="AUD">0.9803</cbc:PriceAmount></cac:Price></cac:InvoiceLine></Invoice>'