from flask_restx import Namespace, Resource
from flask import Flask, request, jsonify, make_response

from src.services.create_xml import create_xml
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

