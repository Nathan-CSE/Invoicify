import json
import re

from flask import Response, request, jsonify, make_response
from flask_restx import Resource

from models import User, db, Invoice
from src.namespaces.invoice import InvoiceNamespace
from src.services.create_xml import create_xml, format_xml
from src.services.utils import base64_encode, token_required, db_insert
from src.services.validation import ValidationService
from src.services.conversion import ConversionService
from src.services.upload import UploadService
from src.services.ocr import OCRService
from src.services.send_mail import send_attachment

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
    def post(self, user: User) -> Response:
        data = request.json
        try:
            res = create_xml(data, user)
            return make_response(jsonify({"data": [res]}), 201)
        except ValueError as e:
            return make_response(e, 422)
        except Exception as e:
            return make_response(jsonify({"message": "UBL not created"}), 400)
        
@invoice_ns.route("/download/<int:id>")
class SendUBLAPI(Resource):
    @invoice_ns.doc(
        description="""Use this api to download xml
            input:
            article_id: int
            output:
                xml string 
            """,
        responses={
            200: 'Created successfully',
            400: 'Bad request',
        }
    )
    def post(self, id: int) -> Response:
        invoice = Invoice.query.where(Invoice.id==id).first()
        if invoice:
            cs = ConversionService()
            xml = cs.json_to_xml(json.dumps(invoice.fields), "AUNZ_PEPPOL_1_0_10")
            return make_response(jsonify({"message": xml}), 200)
        else:
            return make_response(jsonify({"message": "Article not found"}), 400)

@invoice_ns.route("/send_ubl")
class SendEmailAPI(Resource):
    @invoice_ns.doc(
    description="""Use this api to send ubl""",
    body=invoice_ns.get_send_mail_fields(),

    responses={
        200: 'Sent successfully',
        400: 'Bad request',
    })
    @token_required
    def post(self, user: User) -> Response:
        ups = UploadService()
        if 'files' in request.files:
            res = ups.handle_file_upload(request)
            if not res:
                return make_response(jsonify({"message": f"the file uploaded is not a pdf/json, please upload a valid file"}), 400)
        args = invoice_ns.get_send_mail_fields().parse_args()
        target_email = args["target_email"]
        xml_data = []
        cs = ConversionService()

        for id in args.xml_id or []:
            invoice = Invoice.query.where(Invoice.id==id).where(Invoice.user_id==user.id).first()
            if invoice:
                if not invoice.is_ready:
                    return make_response(jsonify({"message": "Article is not ready to be sent"}), 400)
                xml = cs.json_to_xml(json.dumps(invoice.fields), "AUNZ_PEPPOL_1_0_10")
                xml_name = invoice.name
                if ".xml" not in xml_name:
                    xml_name += ".xml"
                xml_data.append((xml_name, xml))
            else:
                return make_response(jsonify({"message": "Article not found"}), 400)
        if send_attachment([target_email], "These documents were requested to be sent to you", xml_data, request.files.getlist('files')):
            return make_response(jsonify({"message": "Successfully sent"}), 200)
        else:
            return make_response(jsonify({"message": "Was unable to be sent"}), 400)

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
    def put(self, id: int, user: User) -> Response:
        data = request.json

        if not (invoice := Invoice.query.filter(Invoice.id == id).filter(Invoice.is_gui == True).first()) or invoice.user_id != user.id:
            return make_response(jsonify({"message": "Invoice does not exist"}), 404)

        json_str = format_xml(data["fields"])

        # Fields or rule has been changed
        if invoice.fields != json_str or invoice.rule != data["rule"]:
            invoice.completed_ubl = None
            invoice.is_ready = False

        invoice.name = data["name"]
        invoice.rule = data["rule"]
        invoice.fields = json.loads(json_str)

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
    def delete(self, id: int, user: User) -> Response:
        if not (invoice := Invoice.query.filter(Invoice.id == id).first()) or invoice.user_id != user.id:
            return make_response(jsonify({"message": "Invoice does not exist"}), 404)

        db.session.delete(invoice)
        db.session.commit()
        return make_response(jsonify({"message": "Invoice was deleted successfully"}), 200)

@invoice_ns.route("/history")
class HistoryAPI(Resource):
    def check_bool(self, bool: bool) -> bool:
        bool = bool.lower().capitalize()
        if bool == "True":
            return True
        elif bool == "False":
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
    def get(self, user: User) -> Response:
        sql = Invoice.query.filter(Invoice.user_id==user.id)
        args = request.args
        if args.get("is_ready"):
            try:
                sql = sql.filter(Invoice.is_ready==self.check_bool(args.get("is_ready")))
            except Exception as err:
                return (make_response(jsonify({"message": str(err)}), 400))

        if args.get("is_gui"):
            try:
                sql = sql.filter(Invoice.is_gui==self.check_bool(args.get("is_gui")))
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
    def post(self, user: User) -> Response:
        ups = UploadService()
        
        res = ups.handle_xml_upload(request)
        args = invoice_ns.get_upload_validation_fields().parse_args()
        rules = args["rules"]
        if not res:
            return make_response(jsonify({"message": f"One or more of the files uploaded is not a XML, please upload XMLs only"}), 400)
        
        vs = ValidationService()
        cs = ConversionService()
        validationRetval = []
        
        for file in request.files.getlist('files'):
            content = file.read()
            try:
                retval = vs.validate_xml(
                    filename=file.filename,
                    content=base64_encode(content),
                    rules=[rules]
                )
            except Exception as err:
                print(str(err))
                return make_response(jsonify({"message": str(err)}), 400)

            if retval["successful"] is True:
                json_str = cs.xml_to_json(content)
                invoice = Invoice(name=file.filename, fields=json.loads(json_str), user_id=user.id, is_ready=True, completed_ubl=base64_encode(content), rule=rules)
                db_insert(invoice)
                validationRetval.append({"validated": True, "data": "Invoice validated successfully", "invoiceId": invoice.id, "invoiceName": invoice.name, "rule": rules})
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
                validationRetval.append({
                    "validated": False, 
                    "data": {
                        "firedAssertionErrors": errors,
                        "firedAssertionErrorsCount": retval["report"].get("firedAssertionErrorsCount", 0),
                        "firedSuccessfulReportsCount": retval["report"].get("firedSuccessfulReportsCount", 0),
                        "successful": retval["report"].get("successful", False),
                        "summary": retval["report"].get("summary", "No summary available")
                    }, 
                    "invoiceId": -1, 
                    "invoiceName": file.filename,
                    "rule": rules
                })
        return make_response(jsonify({"validationOutcome": validationRetval}), 200)

@invoice_ns.route("/validate")
class ValidationAPI(Resource):
    @invoice_ns.doc(
        description="Ability to validate created invoices",
        body=invoice_ns.get_id_validation_fields(),
        responses={
            200: "Validation Complete",
            203: 'Files received but failed to validate',
            400: "Bad Request"
        }
    )
    @token_required
    def get(self, user: User) -> Response:
        args = invoice_ns.get_id_validation_fields().parse_args()
        invoice_ids = args['id']
        rules = args['rules']
        converter = ConversionService()
        vs = ValidationService()
        
        validationRetval = []
        for id in invoice_ids:
            if not (invoice := Invoice.query.filter(Invoice.id == id).first()) or invoice.user_id != user.id:
                return make_response(jsonify({"message": "Invoice does not exist"}), 400)
            try:
                xml_content = converter.json_to_xml(json.dumps(invoice.fields), rules)
            except Exception as err:
                return make_response(jsonify({"message": f"Error converting JSON to XML, {str(err)}"}), 400)
            
            encoded_xml_content = base64_encode(xml_content.encode())

            try:
                retval = vs.validate_xml(
                    filename=invoice.name,
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
                validationRetval.append({"validated": True, "data": "Invoice validated successfully", "invoiceId": invoice.id, "invoiceName": invoice.name, "rule": rules})
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
                validationRetval.append({
                    "validated": False, 
                    "data": {
                        "firedAssertionErrors": errors,
                        "firedAssertionErrorsCount": retval["report"].get("firedAssertionErrorsCount", 0),
                        "firedSuccessfulReportsCount": retval["report"].get("firedSuccessfulReportsCount", 0),
                        "successful": retval["report"].get("successful", False),
                        "summary": retval["report"].get("summary", "No summary available")
                    }, 
                    "invoiceId": invoice.id, 
                    "invoiceName": invoice.name,
                    "rule": rules
                })
        return make_response(jsonify({"validationOutcome": validationRetval}), 200)
        

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
    def post(self, user: User) -> Response:
        ups = UploadService()
        res = ups.handle_file_upload(request)
        if not res:
            return make_response(jsonify({"message": f"the file uploaded is not a pdf/json, please upload a valid file"}), 400)
        
        ublretval = []
        ocr = OCRService()
        for f in request.files.getlist('files'):
            if f.filename.rsplit('.', 1)[1].lower() == 'pdf':
                pdf_str = f.read()
                try:
                    json_str = ocr.run(base64_encode(pdf_str))
                except Exception as err:
                    return make_response(jsonify({"message": f"the file uploaded could not be processed by OCR: {str(err)}"}), 400)

                temp_xml_filename = f.filename.replace('.pdf', '.xml')
            else:
                json_str = f.read().decode('utf-8')
                temp_xml_filename = f.filename.replace('.json', '.xml')

            try:
                invoice = Invoice(name=temp_xml_filename, fields=json.loads(json_str), user_id=user.id, is_ready=False)
            except json.JSONDecodeError:
                return make_response(jsonify({"message": f"the file uploaded is not a valid json, please upload a valid file"}), 400)

            db_insert(invoice)
            
            ublretval.append({
                "filename": temp_xml_filename, "invoiceId": invoice.id}) 
        
        return make_response(jsonify({"message": "Invoice(s) created successfully", "data": ublretval}), 200)
        