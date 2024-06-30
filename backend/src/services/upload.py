

def handle_file_upload(request):
    if 'files' not in request.files:
        return {"message": f"No files were uploaded"}, 400

    files = request.files.getlist('files')
    allowed_extensions = {'pdf', 'json'}

    for file in files:
        if file.filename == '':
            continue 

        if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
            print(file.filename)
        else:
            return {"message": f"{file.filename} is not a PDF or JSON, please remove that file and try again"}, 400

    return {"message": f"Files uploaded"}, 200






   
