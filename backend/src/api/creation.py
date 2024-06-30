from flask import Flask, request, jsonify, make_response
from flask_restx import Namespace, Resource, fields
from werkzeug.datastructures import FileStorage

from src.services.upload import handle_file_upload, save_file
from src.services.utils import token_required

creation_ns = Namespace('creation', description='Operations related to uploading files for creaiton')

upload_parser = creation_ns.parser()
upload_parser.add_argument('files', location='files',
                           type=FileStorage, required=True)

@creation_ns.route("/creationupload")
class CreationUploadAPI(Resource):
    @creation_ns.doc(
    description="Creation endpoint for PDFs and JSONs",
    responses={
        200: 'Files received successfully',
        400: 'Bad request',
    })
    @creation_ns.expect(upload_parser)
    @token_required
    def post(self, user):
        res = handle_file_upload(request)
        if not res[1] == 200:
            return res
        
        # sort files by pdf and json
        # validate pdf extracted fields and json fields
        # call the creation service 
        # collect all XMLs 
        # return
        # tempt response, full function will return XML 
        return make_response(jsonify({"message": f"XMLs created"}), 200)


