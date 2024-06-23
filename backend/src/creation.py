from flask import Flask, request, jsonify, make_response
from flask_restx import Namespace, Resource
import os

from src.creationUtils import save_file

UPLOAD_FOLDER = '/uploadfolder'  
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

creation_ns = Namespace('creation', description='Operations related to creation')

@creation_ns.route("/creationUpload")
class CreationUploadAPI(Resource):
    def post(self):
        if 'file' not in request.files:
            return jsonify({'error': 'No file'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        file_path = save_file(file, UPLOAD_FOLDER)
        
        if file_path:
            return jsonify({"message": "File successfully uploaded.", "path": file_path}), 201
        else:
            return jsonify({"error": "File type not allowed"}), 400