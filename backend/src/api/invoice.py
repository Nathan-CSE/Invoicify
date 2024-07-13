from flask import request, jsonify, make_response, send_file
from flask_restx import Namespace, Resource, fields, reqparse
from werkzeug.datastructures import FileStorage
import io
import json

from models import db, Invoice
from src.services.create_xml import create_xml, save_xml
from src.services.utils import base64_encode, token_required, db_insert
from src.services.validation import ValidationService
from src.services.conversion import ConversionService
from src.services.upload import UploadService

invoice_ns = Namespace('invoice', description='Operations related to creating invoices')

address_fields = invoice_ns.model("Address", {
    "streetName": fields.String(),
    "additionalStreetName": fields.String(),
    "cityName": fields.String(),
    "postalCode": fields.Integer(),
    "country": fields.String()
})
seller_fields = invoice_ns.model("Seller", {
    "ABN": fields.Integer(),
    "companyName": fields.String(),
    "address": fields.Nested(address_fields)
})
buyer_fields= invoice_ns.clone("Buyer", seller_fields)
invoice_item_fields = invoice_ns.model("InvoiceItem", {
    "quantity": fields.Integer(),
    "unitCode": fields.String(),
    "item": fields.String(),
    "description": fields.String(),
    "unitPrice": fields.Float(default=0.1),
    "GST": fields.Integer(),
    "totalPrice": fields.Float(default=0.1)
})
create_ubl_fields = invoice_ns.model('CreateUBLFields', {
    "invoiceName": fields.String(),
    "invoiceNumber": fields.String(),
    "invoiceIssueDate": fields.String(),
    "seller": fields.Nested(seller_fields),
    "buyer": fields.Nested(buyer_fields),
    "invoiceItems": fields.List(fields.Nested(invoice_item_fields)),
    "totalGST": fields.Float(default=0.1),
    "totalTaxable": fields.Float(default=0.1),
    "totalAmount": fields.Float(default=0.1)
})
@invoice_ns.route("/create")
class Create(Resource):
    @invoice_ns.doc(
        description="Creates a UBL",
        body=create_ubl_fields,
        responses={
            201: 'Invoice in XML',
            400: 'Bad request',
            422: 'Failed validation'
        },
    )
    @token_required
    def post(self, user):
        data = request.json
        try:
            res = create_xml(data, user)
            return make_response(jsonify(res), 201)
        except ValueError as e:
            return make_response(str(e), 422)
        except Exception as e:
            return make_response(jsonify({"message": str(e)}), 400)
        
@invoice_ns.route("/download")
class SendUBL(Resource):
    @invoice_ns.doc(
    description="""Use this api to download xml
        input:
        article_id: int
        output:
            nothing (file should start downloading in browser)c
        """,
    responses={
        201: 'Created successfully',
        400: 'Bad request',
    })
    @token_required
    def post(self, user, article_id):
        invoice = Invoice.query.where(Invoice.id==article_id).where(Invoice.user_id==user.id).where(Invoice.is_ready==True).first()
        if invoice:
            file = io.BytesIO()
            file.write(invoice.fields.encode('utf-8'))
            file.seek(0)
            return send_file(file, mimetype='application/xml', as_attachment=True, download_name=invoice.name)
        else:
            return make_response(jsonify({"message": "Article not found"}), 400)
        
        # Create a BytesIO object

save_ubl_fields = invoice_ns.model("SaveUBLFields", {
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
@invoice_ns.route("/save")
class Save(Resource):
    @invoice_ns.doc(
        description="Ability to save UBLs",
        body=save_ubl_fields,
        responses={
            201: 'Saved Successfully',
            400: 'Bad request',
        },
    )
    @token_required
    def post(self, user):
        data = request.json
        db_insert(Invoice(name=data["name"], fields=data["fields"], user_id=user.id, is_ready=False))
        
        return make_response(jsonify({"message": "UBL saved successfully"}), 201)

edit_fields = invoice_ns.model("EditUBLFields", {
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
    "rule": fields.String(default="AUNZ_PEPPOL_1_0_10")
})
@invoice_ns.route("/edit/<int:id>")
class Edit(Resource):
    @invoice_ns.doc(
        description="Ability to edit UBLs",
        body=edit_fields,
        responses={
            204: 'Updated successfully',
            400: 'Bad request',
        },
    )
    @token_required
    def put(self, id, user):
        data = request.json

        if not (invoice := Invoice.query.filter(Invoice.id == id).first()) or invoice.user_id != user.id:
            return make_response(jsonify({"message": "Invoice does not exist"}), 400)

        try:
            cs = ConversionService()
            xml_str = base64_encode(cs.json_to_xml(json.dumps(data["fields"]), data["rule"]).encode())

            vs = ValidationService()
            res = vs.validate_xml(
                filename=data["name"],
                content=xml_str,
                rules=[data["rule"]]
            )
        except Exception as err:
            return make_response(jsonify({"message": str(err)}), 400)

        invoice.name = data["name"]
        invoice.fields = data["fields"] 
        invoice.rule = data["rule"]
        if res["successful"]:
            invoice.completed_ubl = xml_str
            invoice.is_ready = True
        else:
            invoice.completed_ubl = None
            invoice.is_ready = False

        db.session.commit()
        return make_response(jsonify(invoice.to_dict()), 204)

@invoice_ns.route("/delete/<int:id>")
class Delete(Resource):
    @invoice_ns.doc(
        description="Ability to delete UBLs",
        responses={
            200: 'Deleted successfully',
            400: 'Bad request',
        },
    )
    @token_required
    def delete(self, id, user):
        if not (invoice := Invoice.query.filter(Invoice.id == id).first()) or invoice.user_id != user.id:
            return make_response(jsonify({"message": "Invoice does not exist"}), 400)

        db.session.delete(invoice)
        db.session.commit()
        return make_response(jsonify({"message": "Invoice was deleted successfully"}), 200)


history_fields = reqparse.RequestParser()
history_fields.add_argument('is_ready', type=bool, choices=['true', 'false'], help='Optional flag to filter by invoices.\n If no value is provided, all invoices will be returned')
@invoice_ns.route("/history")
class History(Resource):
    def check_is_ready_param(self, is_ready):
        is_ready = is_ready.lower().capitalize()
        if is_ready == "True":
            return True
        elif is_ready == "False":
            return False
        else:
            raise Exception("Invalid parameter value passed for is_ready")

    @invoice_ns.doc(
        description="UBL history of user",
        body=history_fields,
        responses={
            200: 'Successful Request',
            400: 'Bad request',
        },
    )
    @token_required
    def get(self, user):
        sql = Invoice.query.filter(Invoice.user_id==user.id)

        if request.args.get("is_ready") != None:
            try:
                sql = sql.filter(Invoice.is_ready==self.check_is_ready_param(request.args.get("is_ready")))
            except Exception as err:
                return (make_response(jsonify({"message": str(err)}), 400))

        return make_response(jsonify([invoice.to_dict() for invoice in sql.all()]), 200)
    
    
upload_parser = invoice_ns.parser()
upload_parser.add_argument('files', location='files',
                           type=FileStorage, required=True)
upload_parser.add_argument('rules', type=str, help='Rules for validation', required=True)
@invoice_ns.route("/uploadValidate")
class ValidationAPI(Resource):
    @invoice_ns.doc(
    description="Upload endpoint for validation of UBL2.1 XML",
    responses={
        200: 'Files received successfully',
        203: 'Files received but failed to validate',
        400: 'Bad request',
    })
    @invoice_ns.expect(upload_parser)
    @token_required
    def post(self, user):
        ups = UploadService()
        
        res = ups.handle_xml_upload(request)
        args = upload_parser.parse_args()
        # takes one file then encodes it to feed to validation service
        file = args['files']
        content = file.read()  
        rules = args['rules']
        if not res:
            return make_response(jsonify({"message": f"{file.filename} is not a XML, please upload a valid file"}), 400)
        

        vs = ValidationService()

        try:
            retval = vs.validate_xml(
                filename=file.filename,
                content=base64_encode(content),
                rules=[rules]
            )
        except Exception as err:
            return make_response(jsonify({"message": str(err)}), 400)

        if retval["successful"] is True:
            return make_response(jsonify({"message": "Invoice validated sucessfully"}), 200)
        else:
            retmessage = retval["report"]
            return make_response(jsonify({"message": retmessage}), 203)

upload_create_parser = invoice_ns.parser()
upload_create_parser.add_argument('files', location='files',
                           type=FileStorage, required=True)
@invoice_ns.route("/uploadCreate")
class CreateAPI(Resource):
    @invoice_ns.doc(
    description="Upload endpoint for PDFs and Jsons to create UBLs, returns a list with each item containing the xml name, id of the xml, and json contents",
    responses={
        200: 'Invoice(s) created successfully',
        400: 'Bad request',
    })
    @invoice_ns.expect(upload_create_parser)
    @token_required
    def post(self, user):
        ups = UploadService()
        res = ups.handle_file_upload(request)
        if not res:
            return make_response(jsonify({"message": f"the file uploaded is not a pdf/json, please upload a valid file"}), 400)
        
        ublretval = []
        for f in request.files.getlist('files'):
            if f.filename.rsplit('.', 1)[1].lower() == 'pdf':
                pass
            json_str = f.read().decode('utf-8')
            
            temp_xml_filename = f.filename.replace('.json', '.xml')
            invoice = Invoice(name=temp_xml_filename, fields=json.dumps(json_str), user_id=user.id, is_ready=False)
            db_insert(invoice)
            
            ublretval.append({
                "filename": temp_xml_filename, "invoiceId": invoice.id, "retJson": json.loads(json_str)}) 
        
        return make_response(jsonify({"message": "Invoice(s) created successfully", "data": ublretval}), 200)
        
