from flask_restx import Namespace, Resource
from flask import Flask, request, jsonify, make_response, send_file
import io
from models import Invoice

from src.services.create_xml import create_xml, save_xml
from src.services.utils import token_required

invoice_ns = Namespace('invoice', description='Operations related to creating invoices')

xml_fields = invoice_ns.model('XMLFields', {
})
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
            201: '{{user_id: no, article_id: int}}',
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
            return make_response(jsonify({e}, 422))
        except Exception as e:
            return make_response(jsonify({"message": "UBL not created"}), 400)
        
@invoice_ns.route("/download")
class SendUBL(Resource):
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
        
        # Create a BytesIO object

