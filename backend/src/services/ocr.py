import json
import requests
import os

class OCRService():

    _URL = "https://xtract.upbrains.ai/integration-apis/extract-file"

    def run(self, base64_content):
        try:
            res = requests.post(
                self._URL, 
                data={
                    "service_name": "Xtract-Prebuilt",
                    "model_name": "Invoice - Procurement",
                    "base64_content": base64_content
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
            data = data["extractor_result"]["documents"][0]["fields"]
        except (KeyError, IndexError) as err:
            raise err

        fields = {}

        for field in data:
            if not data[field]["content"]:
                continue

            fields[field.replace(" ", "")] = data[field]["content"]
    
        return json.dumps(fields)
