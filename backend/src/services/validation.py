from datetime import datetime, timedelta
import requests
import hashlib
import os

from models import db, ValidationAccessToken
from src.services.utils import db_insert

class ValidationService():
    """
    Validation service for validating data

    Attributes:
        _AUTH_URL: string
            - OAuth URL to retrieve a token for the validation API
        _VALIDATION_URL: string
            - Validation API url to validate XMLs

    Methods:
        validate_xml(filename, content, rules)
            - Validates that an XML is compliant with the specified UBL rules
        _generate_token(access_token)
            - Generates an OAuth Token to allow access to the Validation API
    """

    _AUTH_URL = "https://dev-eat.auth.eu-central-1.amazoncognito.com/oauth2/token"
    _VALIDATION_URL = "https://services.ebusiness-cloud.com/ess-schematron/v1/api/validate"

    def validate_xml(self, filename, content, rules):
        '''
        Validates that an XML is compliant with the specified UBL rules

        Arguments:
            filename: string
                - A string to uniquely identify the XML file
            content: string              
                - A string containing the base-64 encoded contents of the XML
            rules: List[string]      
                - List of rules to validate the XML against
                - Available values: 
                    - AUNZ_PEPPOL_1_0_10, 
                    - AUNZ_PEPPOL_SB_1_0_10, 
                    - AUNZ_UBL_1_0_10, 
                    - FR_EN16931_CII_1_3_11, 
                    - FR_EN16931_UBL_1_3_11, 
                    - RO_RO16931_UBL_1_0_8_EN16931, R
                    - O_RO16931_UBL_1_0_8_CIUS_RO

        Raises:
            - HTTPError: If any HTTP requests fail to execute successfully

        Return Value:
            Returns {}
        '''
        # generate a new access token if missing or has expired
        access_token = ValidationAccessToken.query.first()
        try:
            if not access_token or datetime.now() - access_token.updated_at >= timedelta(hours=1):
                access_token = self._generate_token(access_token)

            res = requests.post(
                url=self._VALIDATION_URL,
                headers={
                    "Accept-Language": "en",
                    "Authorization": f"Bearer {access_token.token}"
                },
                params={
                    "rules": ",".join(rules)
                },
                json={
                    "filename": filename,
                    "content": content,
                    "checksum": hashlib.md5(content.encode()).hexdigest()
                }
            )
            res.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise err
        
        response_body = res.json()

        return response_body

    def _generate_token(self, access_token):
        '''
        Generates an OAuth Token to allow access to the Validation API
        Stores a new token in the database if it does not exist, otherwise updates the previous access_token with the new token

        Arguments:
            access_token: Union[ValidationAccessToken, None]

        Raises:
            - HTTPError: If the HTTP requests to the OAuth API fails to execute successfully

        Return Value:
            Returns {}
        '''
        try:
            res = requests.post(
                url=self._AUTH_URL,
                headers={
                    "content-type": "application/x-www-form-urlencoded"
                },
                data={
                    "grant_type": "client_credentials",
                    "client_id": os.getenv("VALIDATION_OAUTH_CLIENT_ID"),
                    "client_secret": os.getenv("VALIDATION_OAUTH_CLIENT_SECRET"),
                    "scope": "eat/read"
                }
            )
            res.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise err

        response_body = res.json()

        if not access_token:
            db_insert(
                ValidationAccessToken(
                    token=response_body["access_token"],
                    updated_at=datetime.now()
                )
            )
            access_token = ValidationAccessToken.query.first()
        else:
            access_token.token = response_body["access_token"]
            access_token.updated_at = datetime.now()

            db.session.commit()

        return access_token