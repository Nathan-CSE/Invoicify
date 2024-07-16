import io
import json
import re

from flask import request, jsonify, make_response, send_file
from flask_restx import Resource

from models import db, Invoice
from src.namespaces.invoice import InvoiceNamespace
from src.services.create_xml import create_xml
from src.services.utils import base64_encode, token_required, db_insert
from src.services.validation import ValidationService
from src.services.conversion import ConversionService
from src.services.upload import UploadService
from src.services.send_mail import send_xml

invoice_ns = InvoiceNamespace(name='invoice', description='Operations related to creating invoices')

@invoice_ns.route("/create")
class CreateUBLAPI(Resource):
    @invoice_ns.doc(
        description="Creates a UBL",
        body=invoice_ns.get_create_ubl_fields(),
        responses={
            201: 'Invoice ID',
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
            return make_response(e, 422)
        except Exception as e:
            return make_response(jsonify({"message": "UBL not created"}), 400)
        
@invoice_ns.route("/download")
class SendUBLAPI(Resource):
    @invoice_ns.doc(
    description="""Use this api to download xml
        input:
        article_id: int
        output:
            nothing (file should start downloading in browser)
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

@invoice_ns.route("/send_ubl/<int:id>")
class SendEmailAPI(Resource):
    @invoice_ns.doc(
    description="""Use this api to send xml""",
    body=invoice_ns.get_send_mail_fields(),

    responses={
        200: 'Sent successfully',
        400: 'Bad request',
    })
    @token_required
    def post(self, user, id):
        args = invoice_ns.get_send_mail_fields().parse_args()
        target_email = args["target_email"]
        invoice = Invoice.query.where(Invoice.id==id).where(Invoice.user_id==user.id).first()
        if invoice:
            cs = ConversionService()
            print("#################")
            print(invoice.fields)
            print("#################")

            print(json.dumps(invoice.fields))
            print("#################")
            xml = cs.json_to_xml(json.dumps(invoice.fields), "AUNZ_PEPPOL_1_0_10")
            send_xml([target_email], xml, invoice.name + ".xml")
            return make_response(jsonify({"message": "Successfully sent"}), 200)

        else:
            return make_response(jsonify({"message": "Article not found"}), 400)
        
@invoice_ns.route("/save")
class SaveAPI(Resource):
    @invoice_ns.doc(
        description="Ability to save UBLs from GUI",
        body=invoice_ns.get_save_ubl_fields(),
        responses={
            201: 'Saved Successfully',
            400: 'Bad request',
        },
    )
    @token_required
    def post(self, user):
        data = request.json
        db_insert(Invoice(name=data["name"], fields=data["fields"], rule="AUNZ_PEPPOL_1_0_10", user_id=user.id, is_ready=False))
        
        return make_response(jsonify({"message": "UBL saved successfully"}), 201)

@invoice_ns.route("/edit/<int:id>")
class EditAPI(Resource):
    @invoice_ns.doc(
        description="Ability to edit UBLs",
        body=invoice_ns.get_edit_fields(),
        responses={
            204: 'Updated successfully',
            400: 'Bad request',
            404: "Not Found"
        },
    )
    @token_required
    def put(self, id, user):
        data = request.json

        if not (invoice := Invoice.query.filter(Invoice.id == id).first()) or invoice.user_id != user.id:
            return make_response(jsonify({"message": "Invoice does not exist"}), 404)

        # Fields or rule has been changed
        if invoice.fields != data["fields"] or invoice.rule != data["rule"]:
            invoice.completed_ubl = None
            invoice.is_ready = False

        invoice.name = data["name"]
        invoice.rule = data["rule"]
        invoice.fields = data["fields"] 

        db.session.commit()

        return make_response(jsonify(invoice.to_dict()), 204)

@invoice_ns.route("/delete/<int:id>")
class DeleteAPI(Resource):
    @invoice_ns.doc(
        description="Ability to delete UBLs",
        responses={
            200: 'Deleted successfully',
            400: 'Bad request',
            404: "Not Found"
        },
    )
    @token_required
    def delete(self, id, user):
        if not (invoice := Invoice.query.filter(Invoice.id == id).first()) or invoice.user_id != user.id:
            return make_response(jsonify({"message": "Invoice does not exist"}), 404)

        db.session.delete(invoice)
        db.session.commit()
        return make_response(jsonify({"message": "Invoice was deleted successfully"}), 200)

@invoice_ns.route("/history")
class HistoryAPI(Resource):
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
        body=invoice_ns.get_history_fields(),
        responses={
            200: 'Successful Request',
            400: 'Bad request',
        },
    )
    @token_required
    def get(self, user):
        sql = Invoice.query.filter(Invoice.user_id==user.id)
        args = request.args
        if args.get("is_ready"):
            try:
                sql = sql.filter(Invoice.is_ready==self.check_is_ready_param(args.get("is_ready")))
            except Exception as err:
                return (make_response(jsonify({"message": str(err)}), 400))

        return make_response(jsonify([invoice.to_dict() for invoice in sql.all()]), 200)
    
@invoice_ns.route("/uploadValidate")
class UploadValidationAPI(Resource):
    @invoice_ns.doc(
    description="Upload endpoint for validation of UBL2.1 XML",
    body=invoice_ns.get_upload_validation_fields(),
    responses={
        200: 'Files received successfully',
        203: 'Files received but failed to validate',
        400: 'Bad request',
    })
    @token_required
    def post(self, user):
        ups = UploadService()
        
        res = ups.handle_xml_upload(request)
        args = invoice_ns.get_upload_validation_fields().parse_args()
        # takes one file then encodes it to feed to validation service
        file = args['files']
        content = file.read()  
        rules = args["rules"]
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
            cs = ConversionService()
            json_str = cs.xml_to_json(content)
            invoice = Invoice(name=file.filename, fields=json.dumps(json_str), user_id=user.id, is_ready=True, completed_ubl=base64_encode(content), rule=rules)
            db_insert(invoice)
            return make_response(jsonify({"message": "Invoice validated sucessfully", "data": invoice.id}), 200)
        else:
            errors = [
                {
                    "id": error["id"],
                    "location": ', '.join(re.findall(r'\*\:(\w+)', error["location"])),
                    "text": error["text"]
                }
                for report in retval["report"].get("reports", {}).values()
                for error in report.get("firedAssertionErrors", [])
            ]
            
            response = {
                "filename": file.filename,
                "reports": {
                    "firedAssertionErrors": errors,
                    "firedAssertionErrorsCount": retval["report"].get("firedAssertionErrorsCount", 0),
                    "firedSuccessfulReportsCount": retval["report"].get("firedSuccessfulReportsCount", 0),
                    "successful": retval["report"].get("successful", False),
                    "summary": retval["report"].get("summary", "No summary available")
                }
            }
            return make_response(jsonify(response), 203)

@invoice_ns.route("/validate/<int:id>")
class ValidationAPI(Resource):
    @invoice_ns.doc(
        description="Ability to validate created invoices",
        responses={
            200: "Validation Complete",
            203: 'Files received but failed to validate',
            400: "Bad Request"
        }
    )
    @token_required
    def get(self, id, user):

        args = invoice_ns.get_id_validation_fields().parse_args()
        rules = args['rules']

        if not (invoice := Invoice.query.filter(Invoice.id == id).first()) or invoice.user_id != user.id:
            return make_response(jsonify({"message": "Invoice does not exist"}), 400)

        converter = ConversionService()

        try:
            xml_content = converter.json_to_xml(invoice.fields)
        except Exception as err:
            return make_response(jsonify({"message": "Error converting JSON to XML"}), 400)
        
        encoded_xml_content = base64_encode(xml_content.encode()).decode()

        vs = ValidationService()
        
        try:
            retval = vs.validate_xml(
                filename=f"invoice_{id}.xml",
                content=encoded_xml_content,
                rules=[rules]  
            )
        except Exception as err:
            return make_response(jsonify({"message": str(err)}), 400)

        if retval["successful"] is True:
            invoice.is_ready = True
            invoice.completed_ubl = encoded_xml_content
            invoice.rule = rules
            db.session.commit()
            return make_response(jsonify({"message": "Invoice validated successfully"}), 200)
        else:
            invoice.is_ready = False
            invoice.completed_ubl = None
            db.session.commit()
            errors = [
                {
                    "id": error["id"],
                    "location": ', '.join(re.findall(r'\*\:(\w+)', error["location"])),
                    "text": error["text"]
                }
                for report in retval["report"].get("reports", {}).values()
                for error in report.get("firedAssertionErrors", [])
            ]
            
            response = {
                "invoice_id": id,
                "reports": {
                    "firedAssertionErrors": errors,
                    "firedAssertionErrorsCount": retval["report"].get("firedAssertionErrorsCount", 0),
                    "firedSuccessfulReportsCount": retval["report"].get("firedSuccessfulReportsCount", 0),
                    "successful": retval["report"].get("successful", False),
                    "summary": retval["report"].get("summary", "No summary available")
                }
            }
            return make_response(jsonify(response), 203)

@invoice_ns.route("/uploadCreate")
class UploadCreateAPI(Resource):
    @invoice_ns.doc(
    description="Upload endpoint for PDFs and Jsons to create UBLs, returns a list with each item containing the xml name, id of the xml, and json contents",
    body=invoice_ns.get_upload_create_fields(),
    responses={
        200: 'Invoice(s) created successfully',
        400: 'Bad request',
    })
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
            invoice = Invoice(name=temp_xml_filename, fields=json.loads(json_str), user_id=user.id, is_ready=False)
            db_insert(invoice)
            
            ublretval.append({
                "filename": temp_xml_filename, "invoiceId": invoice.id, "retJson": json.loads(json_str)}) 
        
        return make_response(jsonify({"message": "Invoice(s) created successfully", "data": ublretval}), 200)
        
