import pytest

from app import create_app
from models import Invoice, User
from src.services.utils import salt_and_hash, db_insert

@pytest.fixture
def client():
    app = create_app(":memory:")
    with app.app_context():
        yield app.test_client()

@pytest.fixture
def user(client):
    user = User(email="abc@gmail.com", password=salt_and_hash("abc"), token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFiY0BnbWFpbC5jb20ifQ.t5iNUNMkVVEVGNcPx8UdmwWgIMJ22j36xn4kXB-e-qM")
    
    db_insert(user)
    return user

@pytest.fixture
def user_2(client):
    user = User(email="abc2@gmail.com", password=salt_and_hash("abc2"), token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFiYzJAZ21haWwuY29tIn0.Sz2dvn-pLfOtbpDEoFO7Mooc9xLL4fTYhMCoyeHBnKY")
    
    db_insert(user)
    return user

@pytest.fixture
def invoice(user):
    invoice = Invoice(
        name="test-invoice.xml", 
        fields={"ID":"Invoice03","IssueDate":"2022-07-31","InvoiceTypeCode":"380","Note":"Adjustment note to reverse prior bill Invoice01. Free text field can bring attention to reason for credit etc.","DocumentCurrencyCode":"AUD","BuyerReference":"Simple solar plan","InvoicePeriod":{"StartDate":"2022-06-15","EndDate":"2022-07-15"},"BillingReference":{"InvoiceDocumentReference":{"ID":"Invoice01","IssueDate":"2022-07-29"}},"AdditionalDocumentReference":{"ID":"Invoice03.pdf","Attachment":{"EmbeddedDocumentBinaryObject":{"mimeCode":"application/pdf","filename":"Invoice03.pdf","@value":"UGxhaW4gdGV4dCBpbiBwbGFjZSBvZiBwZGYgYXR0YWNobWVudCBmb3Igc2FtcGxlIGludm9pY2Vz"}}},"AccountingSupplierParty":{"Party":{"EndpointID":{"schemeID":"0151","@value":"47555222000"},"PostalAddress":{"CityName":"Harrison","PostalZone":"2912","CountrySubentity":"NSW","Country":{"IdentificationCode":"AU"}},"PartyLegalEntity":{"RegistrationName":"Grey Roo Energy","CompanyID":{"schemeID":"0151","@value":"47555222000"}}}},"AccountingCustomerParty":{"Party":{"EndpointID":{"schemeID":"0151","@value":"47555222000"},"PartyIdentification":{"ID":"AccountNumber123"},"PostalAddress":{"StreetName":"100 Queen Street","CityName":"Sydney","PostalZone":"2000","CountrySubentity":"NSW","Country":{"IdentificationCode":"AU"}},"PartyLegalEntity":{"RegistrationName":"Trotters Incorporated","CompanyID":{"schemeID":"0151","@value":"91888222000"}},"Contact":{"Name":"Lisa Johnson"}}},"TaxTotal":{"TaxAmount":{"currencyID":"AUD","@value":"-15.94"},"TaxSubtotal":{"TaxableAmount":{"currencyID":"AUD","@value":"-159.43"},"TaxAmount":{"currencyID":"AUD","@value":"-15.94"},"TaxCategory":{"ID":"S","Percent":"10","TaxScheme":{"ID":"GST"}}}},"LegalMonetaryTotal":{"LineExtensionAmount":{"currencyID":"AUD","@value":"-159.43"},"TaxExclusiveAmount":{"currencyID":"AUD","@value":"-159.43"},"TaxInclusiveAmount":{"currencyID":"AUD","@value":"-175.37"},"PayableAmount":{"currencyID":"AUD","@value":"-175.37"}},"InvoiceLine":[{"ID":"1","InvoicedQuantity":{"unitCode":"KWH","@value":"-325.2"},"LineExtensionAmount":{"currencyID":"AUD","@value":"-129.04"},"Item":{"Name":"Adjustment - reverse prior Electricity charges - all day rate NMI 9000074677","ClassifiedTaxCategory":{"ID":"S","Percent":"10","TaxScheme":{"ID":"GST"}}},"Price":{"PriceAmount":{"currencyID":"AUD","@value":"0.3968"}}},{"ID":"2","InvoicedQuantity":{"unitCode":"DAY","@value":"-31"},"LineExtensionAmount":{"currencyID":"AUD","@value":"-30.39"},"Item":{"Name":"Adjustment - reverse prior Supply charge","ClassifiedTaxCategory":{"ID":"S","Percent":"10","TaxScheme":{"ID":"GST"}}},"Price":{"PriceAmount":{"currencyID":"AUD","@value":"0.9803"}}}]},
        rule="AUNZ_PEPPOL_1_0_10",
        user_id=user.id,
        is_ready=False
    )
    
    db_insert(invoice)
    return invoice

@pytest.fixture
def invoice_2(user):
    invoice = Invoice(
        name="test-invoice2.xml", 
        fields={
            "Name": "Invoice 2",
            "Fields": {
                "yo": "Yo"
            },
        },
        rule="AUNZ_PEPPOL_1_0_10",
        user_id=user.id,
        completed_ubl="blahblahlba",
        is_ready=True
    )
    
    db_insert(invoice)
    return invoice

@pytest.fixture
def gui_invoice(user):
    invoice = Invoice(
        name="test-gui-invoice.xml", 
        fields={
        "AccountingCustomerParty": {
        "Party": {
            "EndpointID": {
                "@value": "0",
                "schemeID": "0151"
            },
            "PartyLegalEntity": {
                "CompanyID": {
                "@value": "0",
                "schemeID": "0151"
                },
                "RegistrationName": "string"
            },
            "PartyName": {
                "Name": "string"
            },
            "PartyTaxScheme": {
                "TaxScheme": {
                "CompanyID": "0",
                "ID": "GST"
                }
            },
            "PostalAddress": {
                "AdditionalStreetName": "string",
                "CityName": "string",
                "Country": {
                "IdentificationCode": "AU"
                },
                "PostalZone": "string",
                "StreetName": "string"
            }
            }
        },
        "AccountingSupplierParty": {
            "Party": {
            "EndpointID": {
                "@value": "111111",
                "schemeID": "0151"
            },
            "PartyLegalEntity": {
                "CompanyID": {
                "@value": "111111",
                "schemeID": "0151"
                },
                "RegistrationName": "string"
            },
            "PartyName": {
                "Name": "string"
            },
            "PartyTaxScheme": {
                "CompanyID": "111111",
                "TaxScheme": {
                "ID": "GST"
                }
            },
            "PostalAddress": {
                "AdditionalStreetName": "string",
                "CityName": "string",
                "Country": {
                "IdentificationCode": "AU"
                },
                "PostalZone": "string",
                "StreetName": "string"
            }
            }
        },
        "BuyerReference": "string",
        "DocumentCurrencyCode": "AUD",
        "ID": "Invoice01",
        "InvoiceLine": {
            "ID": "0",
            "InvoicedQuantity": {
            "@value": "0",
            "unitCode": "string"
            },
            "Item": {
            "ClassifiedTaxCategory": {
                "ID": "GST",
                "Percent": "0",
                "TaxScheme": {
                "ID": "GST"
                }
            },
            "Description": "string",
            "Name": "string"
            },
            "LineExtensionAmount": {
            "@value": "0.1",
            "currencyID": "AUD"
            },
            "Price": {
            "PriceAmount": {
                "@value": "0.1",
                "currencyID": "AUD"
            }
            }
        },
        "InvoiceTypeCode": "380",
        "IssueDate": "string",
        "LegalMonetaryTotal": {
            "LineExtensionAmount": {
            "@value": "0.1",
            "currencyID": "AUD"
            },
            "PayableAmount": {
            "@value": "0.1",
            "currencyID": "AUD"
            },
            "TaxExclusiveAmount": {
            "@value": "0.1",
            "currencyID": "AUD"
            },
            "TaxInclusiveAmount": {
            "@value": "0.1",
            "currencyID": "AUD"
            }
        },
        "Note": "Taxinvoice",
        "TaxTotal": {
            "TaxAmount": {
            "@value": "10",
            "currencyID": "AUD"
            },
            "TaxSubtotal": {
            "TaxAmount": {
                "@value": "10",
                "currencyID": "AUD"
            },
            "TaxCategory": {
                "ID": "S",
                "Percent": "10",
                "TaxScheme": {
                "ID": "GST"
                }
            },
            "TaxableAmount": {
                "@value": "0.1",
                "currencyID": "AUD"
            }
        }}
        },
        rule="AUNZ_PEPPOL_1_0_10",
        user_id=user.id,
        is_ready=False,
        is_gui=True
    )
    
    db_insert(invoice)
    return invoice

@pytest.fixture
def gui_invoice_2(user):
    invoice = Invoice(
        name="test-gui-invoice2.xml", 
        fields={
        "AccountingCustomerParty": {
        "Party": {
          "EndpointID": {
            "@value": "47555222000",
            "schemeID": "0151"
          },
          "PartyLegalEntity": {
            "CompanyID": {
              "@value": "47555222000",
              "schemeID": "0151"
            },
            "RegistrationName": "Henry Averies"
          },
          "PartyName": {
            "Name": "Henry Averies"
          },
          "PartyTaxScheme": {
            "TaxScheme": {
              "CompanyID": "47555222000",
              "ID": "GST"
            }
          },
          "PostalAddress": {
            "AdditionalStreetName": "a man",
            "CityName": "of fortune",
            "Country": {
              "IdentificationCode": "AU"
            },
            "PostalZone": "1994",
            "StreetName": "Jam"
          }
        }
      },
      "AccountingSupplierParty": {
        "Party": {
          "EndpointID": {
            "@value": "47555222000",
            "schemeID": "0151"
          },
          "PartyLegalEntity": {
            "CompanyID": {
              "@value": "47555222000",
              "schemeID": "0151"
            },
            "RegistrationName": "Windows to Fit Pty Ltd"
          },
          "PartyName": {
            "Name": "Windows to Fit Pty Ltd"
          },
          "PartyTaxScheme": {
            "CompanyID": "47555222000",
            "TaxScheme": {
              "ID": "GST"
            }
          },
          "PostalAddress": {
            "AdditionalStreetName": "test",
            "CityName": "test",
            "Country": {
              "IdentificationCode": "AU"
            },
            "PostalZone": "2912",
            "StreetName": "Test"
          }
        }
      },
      "BuyerReference": "test",
      "DocumentCurrencyCode": "AUD",
      "ID": "Invoice01",
      "InvoiceLine": {
        "ID": "0",
        "InvoicedQuantity": {
          "@value": "10",
          "unitCode": "X01"
        },
        "Item": {
          "ClassifiedTaxCategory": {
            "ID": "GST",
            "Percent": "10",
            "TaxScheme": {
              "ID": "GST"
            }
          },
          "Description": "Pirate",
          "Name": "Booty"
        },
        "LineExtensionAmount": {
          "@value": "1000.0",
          "currencyID": "AUD"
        },
        "Price": {
          "PriceAmount": {
            "@value": "100.0",
            "currencyID": "AUD"
          }
        }
      },
      "InvoiceTypeCode": "380",
      "IssueDate": "2024-06-25",
      "LegalMonetaryTotal": {
        "LineExtensionAmount": {
          "@value": "900.0",
          "currencyID": "AUD"
        },
        "PayableAmount": {
          "@value": "1000.0",
          "currencyID": "AUD"
        },
        "TaxExclusiveAmount": {
          "@value": "900.0",
          "currencyID": "AUD"
        },
        "TaxInclusiveAmount": {
          "@value": "1000.0",
          "currencyID": "AUD"
        }
      },
      "Note": "Taxinvoice",
      "TaxTotal": {
        "TaxAmount": {
          "@value": "10",
          "currencyID": "AUD"
        },
        "TaxSubtotal": {
          "TaxAmount": {
            "@value": "10",
            "currencyID": "AUD"
          },
          "TaxCategory": {
            "ID": "S",
            "Percent": "10",
            "TaxScheme": {
              "ID": "GST"
            }
          },
          "TaxableAmount": {
            "@value": "100.0",
            "currencyID": "AUD"
          }
        }
      }
    },
        rule="AUNZ_PEPPOL_1_0_10",
        user_id=user.id,
        completed_ubl="blahblahlba",
        is_ready=True,
        is_gui=True
    )
    
    db_insert(invoice)
    return invoice