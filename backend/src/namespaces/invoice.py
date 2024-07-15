from flask_restx import Namespace, fields, reqparse
from werkzeug.datastructures import FileStorage

class InvoiceNamespace(Namespace):
    def get_create_ubl_fields(self):
        address_fields = self.model("Address", {
            "streetName": fields.String(),
            "additionalStreetName": fields.String(),
            "cityName": fields.String(),
            "postalCode": fields.String(),
            "country": fields.String()
        })
        seller_fields = self.model("Seller", {
            "ABN": fields.Integer(),
            "companyName": fields.String(),
            "address": fields.Nested(address_fields)
        })
        buyer_fields= self.clone("Buyer", seller_fields)
        invoice_item_fields = self.model("InvoiceItem", {
            "quantity": fields.Integer(),
            "unitCode": fields.String(),
            "item": fields.String(),
            "description": fields.String(),
            "unitPrice": fields.Float(default=0.1),
            "GST": fields.Integer(),
            "totalPrice": fields.Float(default=0.1)
        })
        
        return self.model('CreateUBLFields', {
            "invoiceName": fields.String(),
            "invoiceNumber": fields.Integer(),
            "invoiceIssueDate": fields.String(),
            "seller": fields.Nested(seller_fields),
            "buyer": fields.Nested(buyer_fields),
            "invoiceItems": fields.List(fields.Nested(invoice_item_fields)),
            "totalGST": fields.Float(default=0.1),
            "totalTaxable": fields.Float(default=0.1),
            "totalAmount": fields.Float(default=0.1)
        })
        
    def get_upload_validation_fields(self):
        upload_validate_parser = reqparse.RequestParser()
        upload_validate_parser.add_argument('files', location='files', type=FileStorage, required=True)
        upload_validate_parser.add_argument('rules', type=str, help='Rules for validation', required=True)

        return upload_validate_parser

    def get_upload_create_fields(self):
        upload_create_parser = reqparse.RequestParser()
        upload_create_parser.add_argument('files', location='files', type=FileStorage, required=True)

        return upload_create_parser

    def get_history_fields(self):
        history_fields = reqparse.RequestParser()
        history_fields.add_argument('is_ready', type=bool, choices=["true", "false"], required=False, help='Optional flag to filter by invoices.\n If no value is provided, all invoices will be returned')

        return history_fields
    
    def get_send_mail_fields(self):
        send_mail_fields = reqparse.RequestParser()
        send_mail_fields.add_argument('target_email', type=str, required=True)
        return send_mail_fields

    

    def get_id_validation_fields(self):
        validate_parser = invoice_ns.parser()
        validate_parser.add_argument('rules', type=str, help='Rules for validation', required=True)

        return validate_parser

    def get_save_ubl_fields(self):
        return self.model("SaveUBLFields", {
            "name": fields.String(default="Invoice 1", required=True),
            "fields": fields.Raw(default={
                "invoiceName": "test",
                "invoiceNumber": "1",
                "invoiceIssueDate": "2024-06-25",
                "seller": {
                    "ABN": 47555222000,
                    "companyName": "Windows to Fit Pty Ltd",
                    "address": {
                        "streetName": "Test",
                        "additionalStreetName": "test",
                        "cityName": "test",
                        "postalCode": 2912,
                        "country": "AU"
                    }
                }
            }, required=True)
        })

    def get_edit_fields(self):
        return self.model("EditUBLFields", {
            "name": fields.String(default="Invoice 1"),
            "fields": fields.Raw(default={
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
            }, required=True),
            "rule": fields.String(required=True, default="AUNZ_PEPPOL_1_0_10")
        })
