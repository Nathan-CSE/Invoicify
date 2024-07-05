from datetime import datetime, timedelta
from xml.etree.ElementTree import fromstring, ParseError
import requests
import hashlib
import os

from models import db, ValidationAccessToken
from src.services.utils import db_insert, base64_decode

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
            - ParseError: If the XML passed is formatted invalidly
            - UnicodeDecodeError: If the content passed in has not been base-64 encoded

        Return Value:
            Returns {}
        '''
        try:
            self._check_for_invalid_xml(base64_decode(content))

            # generate a new access token if missing or has expired
            # access_token = ValidationAccessToken.query.first()
            # if not access_token or datetime.now() - access_token.updated_at >= timedelta(hours=1):
            #     access_token = self._generate_token(access_token)
            access_token = "eyJraWQiOiJqUWhhc1B3MXlhODluWVV5VDFIWHNab2dJWEJmRXlZWEZPeCtxV01WZHVJPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI3ZDMwYmk4N2lwdGVnYnJmMmJwMzdwNDJnZyIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiZWF0XC9yZWFkIiwiYXV0aF90aW1lIjoxNzIwMTUyMTEzLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtY2VudHJhbC0xLmFtYXpvbmF3cy5jb21cL2V1LWNlbnRyYWwtMV9xdkNTNFdSdnoiLCJleHAiOjE3MjAxNTU3MTMsImlhdCI6MTcyMDE1MjExMywidmVyc2lvbiI6MiwianRpIjoiY2IyN2U0M2EtYmVhMi00NWYxLTk2NTAtN2ZmN2MzNjEzZjFiIiwiY2xpZW50X2lkIjoiN2QzMGJpODdpcHRlZ2JyZjJicDM3cDQyZ2cifQ.X0teemm40XWXSvcw6iijMTjzIctln1YKISG-Q_RBzKUZL7Qb6F1ifX3tEG9sqLRYiZaqbVzIKaeeObaDI_wEWmq2HycCTRfNGpleQ6K30sWdg4R_zPU1owpMd1ueIchljEPmJmWKPAI2v8GX4Fs0SSJrsqN44ZafjTt3-IDAj2c7MJuAIM9Z4tsLL661QEdNkY5x_sVjMVE1x4rKkDyoR4MgmBKmtnPxQvmyY4uQKSshDXlaM7GwDifG7HxiCl4geN_uZI_Vut-_hHoo_KrLBjx4KD4AuBtUZDvmFCKIPX4Go7yHT_1L3OACbQxxtZwEEF4yEOGsourV18s2U0MqkA"
            res = requests.post(
                url=self._VALIDATION_URL,
                headers={
                    "Accept-Language": "en",
                    "Authorization": f"Bearer {access_token}"
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
        except (requests.exceptions.HTTPError, ParseError, UnicodeDecodeError) as err:
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

    def _check_for_invalid_xml(self, content):
        '''
        Checks if the XML string passed in is formatted correctly by attempting to convert it into an XML object
        This function has no return value

        Arguments:
            content: String
                - contents of the XML as a string

        Raises:
            - ParseError: If the XML passed is formatted invalidly
        '''
        try:
            fromstring(content)
        except ParseError as err:
            raise err