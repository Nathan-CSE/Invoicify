from flask import Request

class UploadService():
    """
    Upload service for uploading files

    Attributes:
        None

    Methods:
        handle_file_upload(request)
            - Handles file uploading for creation endpoints
        _generate_token(access_token)
            - Generates an OAuth Token to allow access to the Validation API
    """
    
    def handle_file_upload(self, request: Request) -> bool:
        '''
        Takes in files and ensure that they are pdf/ json

        Arguments:
            request: Request
                - the whole request including all the files

        Return Value:
            Returns True on success
            Returns False if its not a pdf/ json or file array is empty 
        '''
        if 'files' not in request.files:
            return False

        files = request.files.getlist('files')
        allowed_extensions = {'pdf', 'json'}

        for file in files:
            if file.filename == '':
                continue 

            if not('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
                return False

        return True

    def handle_xml_upload(self, request: Request) -> bool:
        '''
        Takes in files and ensure that they are xml

        Arguments:
            request: Request
                - the whole request including all the files

        Return Value:
            Returns True on success
            Returns False if its not a xml or file array is empty 
        '''
        if 'files' not in request.files:
            return False

        file = request.files['files']
        allowed_extensions = {'xml'}

        # Check if the file is XML
        if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
            return True
        else:
            return False
        