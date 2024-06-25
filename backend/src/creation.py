from flask import Flask, request, jsonify, make_response
from flask_restx import Namespace, Resource, fields

creation_ns = Namespace('creation', description='Operations related to uploading files for creaiton')


@creation_ns.route("/creationupload")
class CreationUploadAPI(Resource):

    def post(self):
        if 'files' not in request.files:
            return make_response(jsonify({"message": "No files found in the request"}), 400)

        files = request.files.getlist('files')
        allowed_extensions = {'pdf', 'json'}

        for file in files:
            if file.filename == '':
                continue 

            if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                print(file.filename)
            else:
                return make_response(jsonify({"message": f"File {file.filename} is not a PDF or JSON"}), 400)

        return make_response(jsonify({"message": "Files received"}), 200)



# creation_upload_fields = creation_ns.model('CreationUpload', {
#     'files': fields.List(fields.Raw, required=True, description='List of files')
# })

    # @creation_ns.doc(
    #     description="Creation endpoint for PDFs and JSONs",
    #     body=creation_upload_fields,
    #     responses={
    #         200: 'Files received successfully',
    #         400: 'Bad request',
    #     })
