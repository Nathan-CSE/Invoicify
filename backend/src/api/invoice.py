import io
import json

from flask import request, jsonify, make_response, send_file
from flask_restx import Resource

from models import db, Invoice
from src.namespaces.invoice import InvoiceNamespace
from src.services.conversion import ConversionService
from src.services.create_xml import create_xml
from src.services.utils import base64_encode, token_required, db_insert
from src.services.validation import ValidationService
from src.services.upload import UploadService

invoice_ns = InvoiceNamespace(name='invoice', description='Operations related to creating invoices')

@invoice_ns.route("/create")
class Create(Resource):
    @invoice_ns.doc(
        description="Creates a UBL",
        body=invoice_ns.get_create_ubl_fields(),
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
        
@invoice_ns.route("/save")
class Save(Resource):
    @invoice_ns.doc(
        description="Ability to save UBLs",
        body=invoice_ns.get_save_ubl_fields(),
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


@invoice_ns.route("/edit/<int:id>")
class Edit(Resource):
    @invoice_ns.doc(
        description="Ability to edit UBLs",
        body=invoice_ns.get_edit_fields(),
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
        body=invoice_ns.get_history_fields(),
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
    
@invoice_ns.route("/validate")
class ValidationAPI(Resource):
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
        # takes one file then encodes it to feed to validation service
        file = request.files['files']
        content = file.read()  
        rules = request.args['rules']
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
        