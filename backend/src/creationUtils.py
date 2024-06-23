from werkzeug.utils import secure_filename
import os

def save_file(file, upload_folder):
    """
    Saves the uploaded file to the specified upload folder.
    
    :param file: Uploaded file instance from Flask request.files
    :param upload_folder: Path to the folder where the file should be saved
    :return: Full path to the saved file
    """
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return file_path
    return None

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'csv'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
