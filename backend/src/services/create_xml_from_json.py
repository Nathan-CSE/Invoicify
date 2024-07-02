import json
from xml.etree.ElementTree import Element, SubElement, tostring

def build_xml(element, key, value):
    is_field = key[0].isupper()
    namespace = "cbc"

    if is_field and isinstance(value, dict):
        if not value.get("value"):
            namespace = "cac"
        subelement = SubElement(element, f"{namespace}:{key}")
        build_xml_tree(subelement, value)
    elif is_field and isinstance(value, str):
        subelement = SubElement(element, f"{namespace}:{key}")
        subelement.text = value
    elif key == "value":
        element.text = value
    else:
        element.set(key, value)

def build_xml_tree(element, data):
    for key, value in data.items():
        if isinstance(value, list):
            for item in value:
                build_xml(element, key, item)
        else:
            build_xml(element, key, value)

def json_to_xml(json_str):
    data = json.loads(json_str)
    root = Element('Invoice', {
        "xmlns:cac": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        "xmlns:cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        "xmlns":"urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"
    })
    customisationIdElement = SubElement(root, "cbc:CustomizationID")
    customisationIdElement.text = "urn:cen.eu:en16931:2017#conformant#urn:fdc:peppol.eu:2017:poacc:billing:international:aunz:3.0"

    profileIdElement = SubElement(root, "cbc:ProfileID")
    profileIdElement.text = "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0"

    build_xml_tree(root, data)

    xml_str = tostring(root, encoding='unicode')
    xml_str = f'<?xml version="1.0" encoding="UTF-8"?>\n{xml_str}'
    
    return xml_str

json_str3 = '''
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

print(json_to_xml(json_str3))