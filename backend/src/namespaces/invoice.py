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
            "GST": fields.Float(default=0.1),
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
            "totalAmount": fields.Float(default=0.1),
            "buyerVatRate": fields.Integer(),
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
        history_fields.add_argument('is_gui', type=bool, choices=["true", "false"], required=False, help='Optional flag to filter by type of invoice.\n If no value is provided, all invoices will be returned')

        return history_fields
    
    def get_send_mail_fields(self):
        send_mail_fields = reqparse.RequestParser()
        send_mail_fields.add_argument('xml_id', type=int, required=False, action='split')
        send_mail_fields.add_argument('files', location='files', type=FileStorage, required=False)
        send_mail_fields.add_argument('target_email', type=str, required=True)
        return send_mail_fields

    

    def get_id_validation_fields(self):
        validate_parser = reqparse.RequestParser()
        validate_parser.add_argument('rules', type=str, help='Rules for validation', required=True)
        validate_parser.add_argument('id', type=str, help='Id for validation', action='split')
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
            "fields": fields.Nested(self.get_create_ubl_fields()),
            "rule": fields.String(required=True, default="AUNZ_PEPPOL_1_0_10")
        })
