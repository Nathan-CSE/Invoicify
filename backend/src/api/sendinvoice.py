from flask import Flask, request, jsonify, make_response
from flask_restx import Namespace, Resource
from werkzeug.datastructures import FileStorage
from src.services.upload import handle_file_upload
from src.services.utils import token_required

sendInvoice_ns = Namespace('sendInvoice', description='Operations related to uploading files for creaiton')

upload_parser = sendInvoice_ns.parser()
upload_parser.add_argument('files', location='files',
                           type=FileStorage, required=True)

@sendInvoice_ns.route("/sendInvoiceUpload")
class SendInvoiceUploadAPI(Resource):
    @sendInvoice_ns.doc(
    description="Endpoint for uploading and sending PDFs/ Json",
    responses={
        200: 'Files received and sent successfully',
        400: 'Bad request',
    })
    @sendInvoice_ns.expect(upload_parser)
    @token_required
    def post(self):
        res = handle_file_upload(request)
        if not res[1] == 200:
            return res
        
        # callsend 
        # collect all XMLs 
        # return
        return make_response(jsonify({"message": f"files received and sent"}), 200)
    
# TODO: 
# @sendInvoice_ns.route("/sendInvoiceFromHistory")
# class SendInvoiceUploadAPI(Resource):
#     @sendInvoice_ns.doc(
#     description="Invoice for sending endpoint for PDFs and JSONs",
#     responses={
#         200: 'Files received successfully',
#         400: 'Bad request',
#     })
#     @sendInvoice_ns.expect(upload_parser)
#     def post(self):
#         res = handle_file_upload(request)
#         if not res[1] == 200:
#             return res
        
#         # callsend 
#         # collect all XMLs 
#         # return
#         return make_response(jsonify({"message": f"XMLs created"}), 200) 

   
