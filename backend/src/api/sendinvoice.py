from flask import Flask, request, jsonify, make_response
from flask_restx import Namespace, Resource, fields
from werkzeug.datastructures import FileStorage

sendInvoice_ns = Namespace('sendInvoice', description='Operations related to uploading files for creaiton')

upload_parser = sendInvoice_ns.parser()
upload_parser.add_argument('files', location='files',
                           type=FileStorage, required=True)
@sendInvoice_ns.route("/sendInvoiceUpload")
class SendInvoiceUploadAPI(Resource):
    @sendInvoice_ns.doc(
    description="Invoice for sending endpoint for PDFs and JSONs",
    responses={
        200: 'Files received successfully',
        400: 'Bad request',
    })
    @sendInvoice_ns.expect(upload_parser)
    def post(self):
        if 'files' not in request.files:
            return make_response(jsonify({"message": "No files found in the request"}), 400)

        files = request.files.getlist('files')
        allowed_extensions = {'pdf', 'json'}

        for file in files:
            print(file)
            if file.filename == '':
                continue 

            if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                print(file.filename)
            else:
                return make_response(jsonify({"message": f"File {file.filename} is not a PDF or JSON"}), 400)

        return make_response(jsonify({"message": "Files received"}), 200)





   
