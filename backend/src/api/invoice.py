from flask import request, jsonify, make_response
from flask_restx import Namespace, Resource, fields, reqparse
from werkzeug.datastructures import FileStorage

from models import db, Invoice
from src.services.create_xml import create_xml
from src.services.utils import token_required, db_insert, base64_encode
from src.services.validation import ValidationService
from src.services.upload import handle_file_upload, handle_xml_upload
from src.services.conversion import ConversionService

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
    "unitCode": fields.Integer(),
    "item": fields.String(),
    "description": fields.String(),
    "unitPrice": fields.Float(default=0.1),
    "GST": fields.String(),
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
            201: 'Created successfully',
            400: 'Bad request',
        },
    )
    @token_required
    def post(self, user):
        data = request.json
        try:
            res = create_xml(data)
            return make_response(jsonify(res), 201)
        except Exception as e:
            print(e)
            return make_response(jsonify({"message": "UBL not created"}), 400)

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

        invoice.fields = data["fields"]
        db.session.commit()

        return make_response(jsonify(invoice.to_dict()), 204)

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
@invoice_ns.route("/validate")
class ValidationAPI(Resource):
    @invoice_ns.doc(
    description="Upload endpoint for validation of UBL2.1 XML",
    responses={
        200: 'Files received successfully',
        400: 'Bad request',
    })
    @invoice_ns.expect(upload_parser)
    @token_required
    def post(self, user):
        res = handle_xml_upload(request)
        if not res[1] == 200:
            return res
        
        # takes one file then encodes it to feed to validation service
        file = request.files['files']
        content = file.read()  
        encoded_content = base64_encode(content.decode())
         
        vs = ValidationService()

        retval = vs.validate_xml(
            filename=file.filename,
            content=encoded_content,
            rules=["AUNZ_PEPPOL_1_0_10"]
        )

        if retval["successful"] is True:
            return make_response(jsonify({"message": "Invoice validated sucessfully"}), 200)
        else:
            # retmessage = "Validation failed.\n"
            # retmessage += 'Failed assertion check:\n'
            # for err in retval["report"]["reports"]["AUNZ_PEPPOL_1_0_10"]["firedAssertionErrors"]:
            #     retmessage += f'''Failed the test {err["test"]} with error code {err["id"]}: {err["text"]} This error happened at {err["location"]}\n'''
            retmessage = retval["report"]
            return make_response(jsonify({"message": retmessage}), 400)
        
@invoice_ns.route("/uploadCreate")
class CreateAPI(Resource):
    @invoice_ns.doc(
    description="Upload endpoint for PDFs and Jsons to create UBLs",
    responses={
        200: 'UBL2.1 created successfully',
        400: 'Bad request',
    })
    @invoice_ns.expect(upload_parser)
    @token_required
    def post(self, user):
        res = handle_file_upload(request)
        if not res[1] == 200:
            return res
        
        vs = ValidationService()
        cs = ConversionService()
        
        ublretval = []
        for f in request.files.getlist('files'):
            if f.filename.rsplit('.', 1)[1].lower() == 'pdf':
                pass
            json_str = f.read()
            # encoded_content = base64.b64encode(json_str).decode('utf-8') 
            encoded_content = base64_encode(json_str.decode('utf-8'))
            ubl = cs.json_to_xml(encoded_content)

            retval = vs.validate_xml(
                filename=f.filename,
                content=ubl,
                rules=["AUNZ_PEPPOL_1_0_10"]
            )
            temp_xml_filename = f.filename.replace('.pdf', '.xml')
            with open(temp_xml_filename, 'wb') as xml_file:
                xml_file.write(ubl.encode('utf-8'))

            if retval["successful"] is not True:
                # retmessage = "Validation failed.\n"
                # retmessage += 'Failed assertion check:\n'
                # for err in retval["report"]["reports"]["AUNZ_PEPPOL_1_0_10"]["firedAssertionErrors"]:
                #     retmessage += f'''Failed the test {err["test"]} with error code {err["id"]}: {err["text"]} This error happened at {err["location"]}\n'''
                retmessage = retval["report"]
                return make_response(jsonify({"message": retmessage}), 400)

            ublretval.append((temp_xml_filename, ubl)) 
        
        return make_response(jsonify({"message": "Invoice(s) created successfully", "data": ublretval}), 200)
        