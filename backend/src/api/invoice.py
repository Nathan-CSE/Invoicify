from flask import Flask, request, jsonify, make_response
from flask_restx import Namespace, Resource, fields

import json

from src.services.create_xml import create_xml
from src.services.utils import token_required, db_insert
from models import Invoice

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

xml_fields = invoice_ns.model('XMLFields', {
    "invoiceName": fields.String(),
    "invoiceNumber": fields.String(),
    "invoiceIssueDate": fields.String(),
    "seller": fields.Nested(seller_fields)
})

save_ubl_fields = invoice_ns.model("SaveUBLFields", {
    "name": fields.String(default="Invoice 1", required=True),
    # "fields": fields.Nested(xml_fields, default={
    #     "invoiceName": "test",
    #     "invoiceNumber": "1",
    #     "invoiceIssueDate": "2024-06-25",
    #     "seller": {
    #         "ABN": 47555222000,
    #         "companyName": "Windows to Fit Pty Ltd",
    #         "address": {
    #             "streetName": "Test",
    #             "additionalStreetName": "test",
    #             "cityName": "test",
    #             "postalCode": 2912,
    #             "country": "AU"
    #         }
    #     }
    # }, required=True)
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
    def put(self, user):
        data = request.json

        db_insert(Invoice(name=data["name"], fields=json.dumps(data["fields"]), user_id=user.id, is_ready=False))

@invoice_ns.route("/save/<int:id>")
class UpdateSaved(Resource):
    @invoice_ns.doc(
        description="Ability to update saved UBLs that are incomplete",
        body=save_ubl_fields,
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

        return make_response(jsonify(invoice.to_dict()), 204)
        db_insert(Invoice(name=data["name"], fields=json.dumps(data["fields"]), user_id=user.id, is_ready=False))

@invoice_ns.route("/history")
class History(Resource):
    @invoice_ns.doc(
        description="UBL history of user",
        responses={
            200: 'Successful Request',
            400: 'Bad request',
        },
    )
    @token_required
    def get(self, user):
        return make_response(jsonify([invoice.to_dict() for invoice in Invoice.query.filter(Invoice.user_id==user.id).all()]), 200)