from flask import Flask, request, jsonify, make_response
from flask_restx import Namespace, Resource
from werkzeug.datastructures import FileStorage
from src.services.upload import handle_file_upload, save_file
from src.services.utils import token_required

saveInvoice = Namespace('saveInvoice', description='Operations related to uploading files without conversion')

upload_parser = saveInvoice.parser()
upload_parser.add_argument('files', location='files',
                           type=FileStorage, required=True)

@saveInvoice.route("/sendInvoiceUpload")
class saveInvoiceUploadAPI(Resource):
    @saveInvoice.doc(
    description="Endpoint for uploading PDFs/ Json without saving them",
    responses={
        200: 'Files received and saved successfully',
        400: 'Bad request',
    })
    @saveInvoice.expect(upload_parser)
    @token_required
    def post(self, user):
        res = handle_file_upload(request)
        if not res[1] == 200:
            return res
        
        email = user.email
        for f in request.files.getlist('files'):
            save_file(f, email)

        return make_response(jsonify({"message": f"Files saved successfully"}), 200)