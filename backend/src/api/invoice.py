import base64
from flask_restx import Namespace, Resource
from flask import Flask, request, jsonify, make_response
from werkzeug.datastructures import FileStorage

from src.services.validation import ValidationService
from src.services.upload import handle_xml_uplaod, save_file
from src.services.create_xml import create_xml
from src.services.utils import token_required

invoice_ns = Namespace('invoice', description='Operations related to creating invoices')

xml_fields = invoice_ns.model('XMLFields', {
})

upload_parser = invoice_ns.parser()
upload_parser.add_argument('files', location='files',
                           type=FileStorage, required=True)

@invoice_ns.route("/create")
class CreateUBL(Resource):
    @invoice_ns.doc(
        description="""Takes a json file in the format
        invoiceName: str,
        invoiceNumber: int,
        invoiceIssueDate: str,
        seller: {
            ABN: int,
            companyName: str,
            address: {
                streetName: str,
                additionalStreetName: str,
                cityName: str,
                postalCode: str,
                country: str
            }
        }
        buyer: {
            ABN: int,
            companyName: str,
            address: {
                streetName: str,
                additionalStreetName: str,
                cityName: str,
                postalCode: str,
                country: str
            }
        }
        invoiceItems: [{
            quantity: int,
            unitCode: int,
            item: str,
            description: str,
            unitPrice: float,
            GST: str,
            totalPrice: float
        }],
        totalGST: float,
        totalTaxable: float,
        totalAmount: float        
        """,
        body = xml_fields,
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



@invoice_ns.route("/validatenewupload")
class ValidationAPI(Resource):
    @invoice_ns.doc(
    description="Upload endpoint for validation of UBL2.1 XMLs",
    responses={
        200: 'Files received successfully',
        400: 'Bad request',
    })
    @invoice_ns.expect(upload_parser)
    @token_required
    def post(self, user):
        res = handle_xml_uplaod(request)
        if not res[1] == 200:
            return res
        file = request.files['files']
        content = file.read()  # Read the file content
        encoded_content = base64.b64encode(content).decode('utf-8') 
        vs = ValidationService()

        return vs.validate_xml(
            filename=file.filename,
            content=encoded_content,
            rules=["AUNZ_PEPPOL_1_0_10"]
        )