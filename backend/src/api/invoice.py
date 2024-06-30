from flask import Flask, request, jsonify, make_response
from flask_restx import Namespace, Resource, fields, reqparse

import json

from src.services.create_xml import create_xml
from src.services.utils import token_required, db_insert
from models import db, Invoice

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

history_fields = reqparse.RequestParser()
history_fields.add_argument('is_ready', type=bool, choices=['true', 'false'], help='Optional flag to filter by invoices.\n If no value is provided, all invoices will be returned')

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
    def post(self, user):
        data = request.json
        db_insert(Invoice(name=data["name"], fields=data["fields"], user_id=user.id, is_ready=False))
        
        return make_response(jsonify({"message": "UBL saved successfully"}), 201)

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