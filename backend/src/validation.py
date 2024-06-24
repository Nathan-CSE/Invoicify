from datetime import datetime, timedelta
import requests
import json
import hashlib
import os

from flask_restx import Namespace, Resource

from models import db, ValidationAccessToken
from src.utils import db_insert

AUTH_URL = "https://dev-eat.auth.eu-central-1.amazoncognito.com/oauth2/token"
VALIDATION_URL = "https://services.ebusiness-cloud.com/ess-schematron/v1/api/validate"

validation_ns = Namespace('validation', description='Operations related to validation')

@validation_ns.route("/validation")
class ValidationAPI(Resource):
    # Temporary API endpoint to allow validate function to be tested
    def get(self):
        validate_xml(
            filename="",
            content="PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPEludm9pY2UgeG1sbnM6Y2FjPSJ1cm46b2FzaXM6bmFtZXM6c3BlY2lmaWNhdGlvbjp1Ymw6c2NoZW1hOnhzZDpDb21tb25BZ2dyZWdhdGVDb21wb25lbnRzLTIiCiAgICB4bWxuczpjYmM9InVybjpvYXNpczpuYW1lczpzcGVjaWZpY2F0aW9uOnVibDpzY2hlbWE6eHNkOkNvbW1vbkJhc2ljQ29tcG9uZW50cy0yIgogICAgeG1sbnM9InVybjpvYXNpczpuYW1lczpzcGVjaWZpY2F0aW9uOnVibDpzY2hlbWE6eHNkOkludm9pY2UtMiI+CiAgICA8Y2JjOkN1c3RvbWl6YXRpb25JRD51cm46Y2VuLmV1OmVuMTY5MzE6MjAxNyNjb25mb3JtYW50I3VybjpmZGM6cGVwcG9sLmV1OjIwMTc6cG9hY2M6YmlsbGluZzppbnRlcm5hdGlvbmFsOmF1bno6My4wPC9jYmM6Q3VzdG9taXphdGlvbklEPgogICAgPGNiYzpQcm9maWxlSUQ+dXJuOmZkYzpwZXBwb2wuZXU6MjAxNzpwb2FjYzpiaWxsaW5nOjAxOjEuMDwvY2JjOlByb2ZpbGVJRD4KICAgIDxjYmM6SUQ+SW52b2ljZTAxPC9jYmM6SUQ+CiAgICA8Y2JjOklzc3VlRGF0ZT4yMDE5LTA3LTI5PC9jYmM6SXNzdWVEYXRlPgogICAgPGNiYzpJbnZvaWNlVHlwZUNvZGU+MzgwPC9jYmM6SW52b2ljZVR5cGVDb2RlPgogICAgPGNiYzpOb3RlPlRheCBpbnZvaWNlPC9jYmM6Tm90ZT4KICAgIDxjYmM6RG9jdW1lbnRDdXJyZW5jeUNvZGU+QVVEPC9jYmM6RG9jdW1lbnRDdXJyZW5jeUNvZGU+CiAgICA8Y2JjOkJ1eWVyUmVmZXJlbmNlPlNpbXBsZSBzb2xhciBwbGFuPC9jYmM6QnV5ZXJSZWZlcmVuY2U+CiAgICA8Y2FjOkFjY291bnRpbmdTdXBwbGllclBhcnR5PgogICAgICAgIDxjYWM6UGFydHk+CiAgICAgICAgICAgIDxjYmM6RW5kcG9pbnRJRCBzY2hlbWVJRD0iMDE1MSI+NDc1NTUyMjIwMDA8L2NiYzpFbmRwb2ludElEPiA8IS0tIHNlbGxlciBBQk4gLS0+CiAgICAgICAgICAgIDxjYWM6UGFydHlOYW1lPgogICAgICAgICAgICAgICAgPGNiYzpOYW1lPldpbmRvd3MgdG8gRml0IFB0eSBMdGQ8L2NiYzpOYW1lPgogICAgICAgICAgICA8L2NhYzpQYXJ0eU5hbWU+CiAgICAgICAgICAgIDxjYWM6UG9zdGFsQWRkcmVzcz4KICAgICAgICAgICAgICAgIDxjYmM6U3RyZWV0TmFtZT5NYWluIHN0cmVldCAxPC9jYmM6U3RyZWV0TmFtZT4KICAgICAgICAgICAgICAgIDxjYmM6QWRkaXRpb25hbFN0cmVldE5hbWU+UG9zdGJveCAxMjM8L2NiYzpBZGRpdGlvbmFsU3RyZWV0TmFtZT4KICAgICAgICAgICAgICAgIDxjYmM6Q2l0eU5hbWU+SGFycmlzb248L2NiYzpDaXR5TmFtZT4KICAgICAgICAgICAgICAgIDxjYmM6UG9zdGFsWm9uZT4yOTEyPC9jYmM6UG9zdGFsWm9uZT4KICAgICAgICAgICAgICAgIDxjYWM6Q291bnRyeT4KICAgICAgICAgICAgICAgICAgICA8Y2JjOklkZW50aWZpY2F0aW9uQ29kZT5BVTwvY2JjOklkZW50aWZpY2F0aW9uQ29kZT4KICAgICAgICAgICAgICAgIDwvY2FjOkNvdW50cnk+CiAgICAgICAgICAgIDwvY2FjOlBvc3RhbEFkZHJlc3M+CiAgICAgICAgICAgIDxjYWM6UGFydHlMZWdhbEVudGl0eT4KCQkJCTxjYmM6UmVnaXN0cmF0aW9uTmFtZT5XaW5kb3dzIHRvIEZpdCBQdHkgTHRkPC9jYmM6UmVnaXN0cmF0aW9uTmFtZT4KCQkJCTxjYmM6Q29tcGFueUlEIHNjaGVtZUlEPSIwMTUxIj40NzU1NTIyMjAwMDwvY2JjOkNvbXBhbnlJRD4gPCEtLSBzZWxsZXIgQUJOIC0tPgoJCQk8L2NhYzpQYXJ0eUxlZ2FsRW50aXR5PgogICAgICAgICAgICA8Y2FjOlBhcnR5VGF4U2NoZW1lPgogICAgICAgICAgICAgICAgPGNiYzpDb21wYW55SUQ+NDc1NTUyMjIwMDA8L2NiYzpDb21wYW55SUQ+IDwhLS0gc2VsbGVyIEFCTiAtLT4KICAgICAgICAgICAgICAgIDxjYWM6VGF4U2NoZW1lPgogICAgICAgICAgICAgICAgICAgIDxjYmM6SUQ+R1NUPC9jYmM6SUQ+CiAgICAgICAgICAgICAgICA8L2NhYzpUYXhTY2hlbWU+CiAgICAgICAgICAgIDwvY2FjOlBhcnR5VGF4U2NoZW1lPgogICAgICAgIDwvY2FjOlBhcnR5PgogICAgPC9jYWM6QWNjb3VudGluZ1N1cHBsaWVyUGFydHk+CgogICAgPGNhYzpBY2NvdW50aW5nQ3VzdG9tZXJQYXJ0eT4KICAgICAgICA8Y2FjOlBhcnR5PgogICAgICAgICAgICA8Y2JjOkVuZHBvaW50SUQgc2NoZW1lSUQ9IjAxNTEiPjkxODg4MjIyMDAwPC9jYmM6RW5kcG9pbnRJRD4gPCEtLSBCdXllci9jdXN0b21lciBBQk4gLS0+CiAgICAgICAgICAgIDxjYWM6UGFydHlOYW1lPgogICAgICAgICAgICAgICAgPGNiYzpOYW1lPlRyb3R0ZXJzIFRyYWRpbmcgQ28gTHRkPC9jYmM6TmFtZT4KICAgICAgICAgICAgPC9jYWM6UGFydHlOYW1lPgogICAgICAgICAgICA8Y2FjOlBvc3RhbEFkZHJlc3M+CiAgICAgICAgICAgICAgICA8Y2JjOlN0cmVldE5hbWU+MTAwIFF1ZWVuIFN0cmVldDwvY2JjOlN0cmVldE5hbWU+CiAgICAgICAgICAgICAgICA8Y2JjOkFkZGl0aW9uYWxTdHJlZXROYW1lPlBvIGJveCA4Nzg8L2NiYzpBZGRpdGlvbmFsU3RyZWV0TmFtZT4KICAgICAgICAgICAgICAgIDxjYmM6Q2l0eU5hbWU+U3lkbmV5PC9jYmM6Q2l0eU5hbWU+CiAgICAgICAgICAgICAgICA8Y2JjOlBvc3RhbFpvbmU+MjAwMDwvY2JjOlBvc3RhbFpvbmU+CiAgICAgICAgICAgICAgICA8Y2FjOkNvdW50cnk+CiAgICAgICAgICAgICAgICAgICAgPGNiYzpJZGVudGlmaWNhdGlvbkNvZGU+QVU8L2NiYzpJZGVudGlmaWNhdGlvbkNvZGU+CiAgICAgICAgICAgICAgICA8L2NhYzpDb3VudHJ5PgogICAgICAgICAgICA8L2NhYzpQb3N0YWxBZGRyZXNzPgogICAgICAgICAgICA8Y2FjOlBhcnR5TGVnYWxFbnRpdHk+CgkJCQk8Y2JjOlJlZ2lzdHJhdGlvbk5hbWU+VHJvdHRlcnMgSW5jb3Jwb3JhdGVkPC9jYmM6UmVnaXN0cmF0aW9uTmFtZT4KCQkJCTxjYmM6Q29tcGFueUlEIHNjaGVtZUlEPSIwMTUxIj45MTg4ODIyMjAwMDwvY2JjOkNvbXBhbnlJRD4gPCEtLSBCdXllci9jdXN0b21lciBBQk4gLS0+CgkJCTwvY2FjOlBhcnR5TGVnYWxFbnRpdHk+CiAgICAgICAgICAgIDxjYWM6UGFydHlUYXhTY2hlbWU+CiAgICAgICAgICAgICAgICA8Y2FjOlRheFNjaGVtZT4KICAgICAgICAgICAgICAgICAgICA8Y2JjOkNvbXBhbnlJRD45MTg4ODIyMjAwMDwvY2JjOkNvbXBhbnlJRD4gPCEtLSBzZWxsZXIgQUJOIC0tPgogICAgICAgICAgICAgICAgICAgIDxjYmM6SUQ+R1NUPC9jYmM6SUQ+CiAgICAgICAgICAgICAgICA8L2NhYzpUYXhTY2hlbWU+CiAgICAgICAgICAgIDwvY2FjOlBhcnR5VGF4U2NoZW1lPgogICAgICAgIDwvY2FjOlBhcnR5PgogICAgPC9jYWM6QWNjb3VudGluZ0N1c3RvbWVyUGFydHk+CgogICAgPGNhYzpUYXhUb3RhbD4KICAgICAgICA8Y2JjOlRheEFtb3VudCBjdXJyZW5jeUlEPSJBVUQiPjE0OC43NDwvY2JjOlRheEFtb3VudD4KICAgICAgICA8Y2FjOlRheFN1YnRvdGFsPgogICAgICAgICAgICA8Y2JjOlRheGFibGVBbW91bnQgY3VycmVuY3lJRD0iQVVEIj4xNDg3LjQwPC9jYmM6VGF4YWJsZUFtb3VudD4KICAgICAgICAgICAgPGNiYzpUYXhBbW91bnQgY3VycmVuY3lJRD0iQVVEIj4xNDguNzQ8L2NiYzpUYXhBbW91bnQ+CiAgICAgICAgICAgIDxjYWM6VGF4Q2F0ZWdvcnk+CiAgICAgICAgICAgICAgICA8Y2JjOklEPlM8L2NiYzpJRD4KICAgICAgICAgICAgICAgIDxjYmM6UGVyY2VudD4xMDwvY2JjOlBlcmNlbnQ+CiAgICAgICAgICAgICAgICA8Y2FjOlRheFNjaGVtZT4KICAgICAgICAgICAgICAgICAgICA8Y2JjOklEPkdTVDwvY2JjOklEPgogICAgICAgICAgICAgICAgPC9jYWM6VGF4U2NoZW1lPgogICAgICAgICAgICA8L2NhYzpUYXhDYXRlZ29yeT4KICAgICAgICA8L2NhYzpUYXhTdWJ0b3RhbD4KICAgIDwvY2FjOlRheFRvdGFsPgoKCgogICAgPGNhYzpMZWdhbE1vbmV0YXJ5VG90YWw+CiAgICAgICAgPGNiYzpMaW5lRXh0ZW5zaW9uQW1vdW50IGN1cnJlbmN5SUQ9IkFVRCI+MTQ4Ny40MDwvY2JjOkxpbmVFeHRlbnNpb25BbW91bnQ+CiAgICAgICAgPGNiYzpUYXhFeGNsdXNpdmVBbW91bnQgY3VycmVuY3lJRD0iQVVEIj4xNDg3LjQwPC9jYmM6VGF4RXhjbHVzaXZlQW1vdW50PgogICAgICAgIDxjYmM6VGF4SW5jbHVzaXZlQW1vdW50IGN1cnJlbmN5SUQ9IkFVRCI+MTYzNi4xNDwvY2JjOlRheEluY2x1c2l2ZUFtb3VudD4KICAgICAgICA8Y2JjOlBheWFibGVBbW91bnQgY3VycmVuY3lJRD0iQVVEIj4xNjM2LjE0PC9jYmM6UGF5YWJsZUFtb3VudD4KICAgIDwvY2FjOkxlZ2FsTW9uZXRhcnlUb3RhbD4KIAoKICAgIDxjYWM6SW52b2ljZUxpbmU+CiAgICAgICA8Y2JjOklEPjE8L2NiYzpJRD4KICAgICAgIDxjYmM6Tm90ZT5UZXh0cyBHaXZpbmcgTW9yZSBJbmZvIGFib3V0IHRoZSBJbnZvaWNlIExpbmU8L2NiYzpOb3RlPgogICAgICAgPGNiYzpJbnZvaWNlZFF1YW50aXR5IHVuaXRDb2RlPSJFOTkiPjEwPC9jYmM6SW52b2ljZWRRdWFudGl0eT4KICAgICAgIDxjYmM6TGluZUV4dGVuc2lvbkFtb3VudCBjdXJyZW5jeUlEPSAiQVVEIj4yOTkuOTA8L2NiYzpMaW5lRXh0ZW5zaW9uQW1vdW50PgoKICAgIDxjYWM6SXRlbT4KICAgICAgICA8Y2JjOkRlc2NyaXB0aW9uPldpZGdldHMgVHJ1ZSBhbmQgRmFpcjwvY2JjOkRlc2NyaXB0aW9uPiA8IS0tIG9wdGlvbmFsIC0tPgogICAgICAgICAgIDxjYmM6TmFtZT5UcnVlLVdpZGdldHM8L2NiYzpOYW1lPgogICAgICAgICAgICA8Y2FjOkNsYXNzaWZpZWRUYXhDYXRlZ29yeT4KICAgICAgICAgICAgICAgIDxjYmM6SUQ+UzwvY2JjOklEPgogICAgICAgICAgICAgICAgPGNiYzpQZXJjZW50PjEwPC9jYmM6UGVyY2VudD4KICAgICAgICAgICAgICAgIDxjYWM6VGF4U2NoZW1lPgogICAgICAgICAgICAgICAgICAgIDxjYmM6SUQ+R1NUPC9jYmM6SUQ+CiAgICAgICAgICAgICAgICA8L2NhYzpUYXhTY2hlbWU+CiAgICAgICAgICAgIDwvY2FjOkNsYXNzaWZpZWRUYXhDYXRlZ29yeT4KICAgICAgICA8L2NhYzpJdGVtPgoKICAgICAgIDxjYWM6UHJpY2U+CiAgICAgICAgICAgPGNiYzpQcmljZUFtb3VudCBjdXJyZW5jeUlEPSJBVUQiPjI5Ljk5PC9jYmM6UHJpY2VBbW91bnQ+CiAgICAgICA8L2NhYzpQcmljZT4KCiAgICA8L2NhYzpJbnZvaWNlTGluZT4KCgogICA8Y2FjOkludm9pY2VMaW5lPgogICAgICAgPGNiYzpJRD4xPC9jYmM6SUQ+CiAgICAgICA8Y2JjOk5vdGU+VGV4dHMgR2l2aW5nIE1vcmUgSW5mbyBhYm91dCB0aGUgSW52b2ljZSBMaW5lPC9jYmM6Tm90ZT4KICAgICAgIDxjYmM6SW52b2ljZWRRdWFudGl0eSB1bml0Q29kZT0iRTk5Ij4xMDwvY2JjOkludm9pY2VkUXVhbnRpdHk+CiAgICAgICA8Y2JjOkxpbmVFeHRlbnNpb25BbW91bnQgY3VycmVuY3lJRD0gIkFVRCI+Mjk5LjkwPC9jYmM6TGluZUV4dGVuc2lvbkFtb3VudD4KCiAgICA8Y2FjOkl0ZW0+CiAgICAgICAgPGNiYzpEZXNjcmlwdGlvbj5XaWRnZXRzIFRydWUgYW5kIEZhaXI8L2NiYzpEZXNjcmlwdGlvbj4KICAgICAgICAgICA8Y2JjOk5hbWU+VHJ1ZS1XaWRnZXRzPC9jYmM6TmFtZT4KICAgICAgICAgICAgPGNhYzpDbGFzc2lmaWVkVGF4Q2F0ZWdvcnk+CiAgICAgICAgICAgICAgICA8Y2JjOklEPlM8L2NiYzpJRD4KICAgICAgICAgICAgICAgIDxjYmM6UGVyY2VudD4xMDwvY2JjOlBlcmNlbnQ+CiAgICAgICAgICAgICAgICA8Y2FjOlRheFNjaGVtZT4KICAgICAgICAgICAgICAgICAgICA8Y2JjOklEPkdTVDwvY2JjOklEPgogICAgICAgICAgICAgICAgPC9jYWM6VGF4U2NoZW1lPgogICAgICAgICAgICA8L2NhYzpDbGFzc2lmaWVkVGF4Q2F0ZWdvcnk+CiAgICAgICAgPC9jYWM6SXRlbT4KCiAgICAgICA8Y2FjOlByaWNlPgogICAgICAgICAgIDxjYmM6UHJpY2VBbW91bnQgY3VycmVuY3lJRD0iQVVEIj4yOS45OTwvY2JjOlByaWNlQW1vdW50PgogICAgICAgPC9jYWM6UHJpY2U+CgogICAgPC9jYWM6SW52b2ljZUxpbmU+CgoKPGNhYzpJbnZvaWNlTGluZT4KICAgICAgIDxjYmM6SUQ+MTwvY2JjOklEPgogICAgICAgPGNiYzpOb3RlPlRleHRzIEdpdmluZyBNb3JlIEluZm8gYWJvdXQgdGhlIEludm9pY2UgTGluZTwvY2JjOk5vdGU+CiAgICAgICA8Y2JjOkludm9pY2VkUXVhbnRpdHkgdW5pdENvZGU9IkU5OSI+MTA8L2NiYzpJbnZvaWNlZFF1YW50aXR5PgogICAgICAgPGNiYzpMaW5lRXh0ZW5zaW9uQW1vdW50IGN1cnJlbmN5SUQ9ICJBVUQiPjI5OS45MDwvY2JjOkxpbmVFeHRlbnNpb25BbW91bnQ+CgogICAgPGNhYzpJdGVtPgogICAgICAgIDxjYmM6RGVzY3JpcHRpb24+V2lkZ2V0cyBUcnVlIGFuZCBGYWlyPC9jYmM6RGVzY3JpcHRpb24+CiAgICAgICAgICAgPGNiYzpOYW1lPlRydWUtV2lkZ2V0czwvY2JjOk5hbWU+CiAgICAgICAgICAgIDxjYWM6Q2xhc3NpZmllZFRheENhdGVnb3J5PgogICAgICAgICAgICAgICAgPGNiYzpJRD5TPC9jYmM6SUQ+CiAgICAgICAgICAgICAgICA8Y2JjOlBlcmNlbnQ+MTA8L2NiYzpQZXJjZW50PgogICAgICAgICAgICAgICAgPGNhYzpUYXhTY2hlbWU+CiAgICAgICAgICAgICAgICAgICAgPGNiYzpJRD5HU1Q8L2NiYzpJRD4KICAgICAgICAgICAgICAgIDwvY2FjOlRheFNjaGVtZT4KICAgICAgICAgICAgPC9jYWM6Q2xhc3NpZmllZFRheENhdGVnb3J5PgogICAgICAgIDwvY2FjOkl0ZW0+CgogICAgICAgPGNhYzpQcmljZT4KICAgICAgICAgICA8Y2JjOlByaWNlQW1vdW50IGN1cnJlbmN5SUQ9IkFVRCI+MjkuOTk8L2NiYzpQcmljZUFtb3VudD4KICAgICAgIDwvY2FjOlByaWNlPgoKICAgIDwvY2FjOkludm9pY2VMaW5lPgoKCjwvSW52b2ljZT4K",
            rules=["AUNZ_PEPPOL_1_0_10"]
        )

def generate_token(access_token):
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
            url=AUTH_URL,
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

def validate_xml(filename, content, rules):
    '''
    Validates that an XML is compliant with the specified UBL rules

    Arguments:
        filename: Optional[string]   
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
            access_token = generate_token(access_token)

        res = requests.post(
            url=VALIDATION_URL,
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