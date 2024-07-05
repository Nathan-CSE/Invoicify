import os

def handle_file_upload(request):
    if 'files' not in request.files:
        return {"message": f"No files were uploaded"}, 400

    files = request.files.getlist('files')
    allowed_extensions = {'pdf', 'json'}

    for file in files:
        if file.filename == '':
            continue 

        if not('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
            return {"message": f"{file.filename} is not a PDF or JSON, please remove that file and try again"}, 400

    return {"message": f"Files uploaded"}, 200



def handle_xml_upload(request):
    if 'files' not in request.files:
        return {"message": "No file was uploaded"}, 400

    file = request.files['files']
    allowed_extensions = {'xml'}

    # Check if the file is XML
    if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
        return True
    else:
        return False


def save_file(file, email):
    base_path = "instance/documents"
    user_folder = os.path.join(base_path, email)
    file_destination = os.path.join(user_folder, "files", file.filename)
    
    # Create the directory structure if it doesn't exist
    os.makedirs(os.path.dirname(file_destination), exist_ok=True)
    
    file.save(file_destination)