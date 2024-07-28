import json
import requests
import os

class OCRService():
    """
    OCR service for converting PDF into a JSON format

    Attributes:
        _URL: String
            - String of the OCR API

    Methods:
        run(self, content)
            - Converts a base64 encoded PDF into a JSON string
    """
    _URL = "https://xtract.upbrains.ai/integration-apis/extract-file"

    def run(self, content):
        '''
        Runs the OCR for a base64 encoded PDF file and converts it into a JSON string

        Arguments:
            content: string              
                - A string containing the base-64 encoded contents of the PDF file
            
        Raises:
            - HTTPError: If any HTTP requests fail to execute successfully
            - KeyError, IndexError: If the PDF passed in doesn't return correct fields

        Return Value:
            Returns {}
        '''
        try:
            res = requests.post(
                self._URL, 
                data={
                    "service_name": "Xtract-Prebuilt",
                    "model_name": "Invoice - Procurement",
                    "base64_content": content
                },
                headers={
                    "Authorization": os.getenv("OCR_AUTH_TOKEN")
                }
            )
            res.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise err
        
        data = res.json()
        try:
            data_fields = data["extractor_result"]["documents"][0]["fields"]
            data_items = data["extractor_result"]["documents"][0]["items"]
        except (KeyError, IndexError) as err:
            raise err

        fields = {}
        for field in data_fields:
            if not data_fields[field]["content"]:
                continue

            fields[field.replace(" ", "")] = data_fields[field]["content"]
        
        for item in data_items:
            if "InvoiceLine" not in fields:
                fields["InvoiceLine"] = []

            item_fields = {}
            for field in item:
                if "content" not in item[field] or not item[field]["content"]:
                    continue
                
                item_fields[field.replace(" ", "")] = item[field]["content"]
        
            fields["InvoiceLine"].append(item_fields)

        return json.dumps(fields)
