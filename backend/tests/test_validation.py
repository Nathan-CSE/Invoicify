import pytest
import json

from tests.fixtures import client
from src.services.validation import ValidationService

VALIDATION_PATH = "/validation/validation"
vs = ValidationService()

def test_xml_validate_function_success(client):
    encoded_data = "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KICAgICAgICA8SW52b2ljZSB4bWxuczpjYWM9InVybjpvYXNpczpuYW1lczpzcGVjaWZpY2F0aW9uOnVibDpzY2hlbWE6eHNkOkNvbW1vbkFnZ3JlZ2F0ZUNvbXBvbmVudHMtMiIKICAgICAgICAgICAgeG1sbnM6Y2JjPSJ1cm46b2FzaXM6bmFtZXM6c3BlY2lmaWNhdGlvbjp1Ymw6c2NoZW1hOnhzZDpDb21tb25CYXNpY0NvbXBvbmVudHMtMiIKICAgICAgICAgICAgeG1sbnM9InVybjpvYXNpczpuYW1lczpzcGVjaWZpY2F0aW9uOnVibDpzY2hlbWE6eHNkOkludm9pY2UtMiI+CiAgICAgICAgICAgIDxjYmM6Q3VzdG9taXphdGlvbklEPnVybjpjZW4uZXU6ZW4xNjkzMToyMDE3I2NvbmZvcm1hbnQjdXJuOmZkYzpwZXBwb2wuZXU6MjAxNzpwb2FjYzpiaWxsaW5nOmludGVybmF0aW9uYWw6YXVuejozLjA8L2NiYzpDdXN0b21pemF0aW9uSUQ+CiAgICAgICAgICAgIDxjYmM6UHJvZmlsZUlEPnVybjpmZGM6cGVwcG9sLmV1OjIwMTc6cG9hY2M6YmlsbGluZzowMToxLjA8L2NiYzpQcm9maWxlSUQ+CiAgICAgICAgICAgIDxjYmM6SUQ+SW52b2ljZTAxPC9jYmM6SUQ+CiAgICAgICAgICAgIDxjYmM6SXNzdWVEYXRlPjIwMTktMDctMjk8L2NiYzpJc3N1ZURhdGU+CiAgICAgICAgICAgIDxjYmM6SW52b2ljZVR5cGVDb2RlPjM4MDwvY2JjOkludm9pY2VUeXBlQ29kZT4KICAgICAgICAgICAgPGNiYzpOb3RlPlRheCBpbnZvaWNlPC9jYmM6Tm90ZT4KICAgICAgICAgICAgPGNiYzpEb2N1bWVudEN1cnJlbmN5Q29kZT5BVUQ8L2NiYzpEb2N1bWVudEN1cnJlbmN5Q29kZT4KICAgICAgICAgICAgPGNiYzpCdXllclJlZmVyZW5jZT5TaW1wbGUgc29sYXIgcGxhbjwvY2JjOkJ1eWVyUmVmZXJlbmNlPgogICAgICAgICAgICA8Y2FjOkFjY291bnRpbmdTdXBwbGllclBhcnR5PgogICAgICAgICAgICAgICAgPGNhYzpQYXJ0eT4KICAgICAgICAgICAgICAgICAgICA8Y2JjOkVuZHBvaW50SUQgc2NoZW1lSUQ9IjAxNTEiPjQ3NTU1MjIyMDAwPC9jYmM6RW5kcG9pbnRJRD4KICAgICAgICAgICAgICAgICAgICA8Y2FjOlBhcnR5TmFtZT4KICAgICAgICAgICAgICAgICAgICAgICAgPGNiYzpOYW1lPldpbmRvd3MgdG8gRml0IFB0eSBMdGQ8L2NiYzpOYW1lPgogICAgICAgICAgICAgICAgICAgIDwvY2FjOlBhcnR5TmFtZT4KICAgICAgICAgICAgICAgICAgICA8Y2FjOlBvc3RhbEFkZHJlc3M+CiAgICAgICAgICAgICAgICAgICAgICAgIDxjYmM6U3RyZWV0TmFtZT5NYWluIHN0cmVldCAxPC9jYmM6U3RyZWV0TmFtZT4KICAgICAgICAgICAgICAgICAgICAgICAgPGNiYzpBZGRpdGlvbmFsU3RyZWV0TmFtZT5Qb3N0Ym94IDEyMzwvY2JjOkFkZGl0aW9uYWxTdHJlZXROYW1lPgogICAgICAgICAgICAgICAgICAgICAgICA8Y2JjOkNpdHlOYW1lPkhhcnJpc29uPC9jYmM6Q2l0eU5hbWU+CiAgICAgICAgICAgICAgICAgICAgICAgIDxjYmM6UG9zdGFsWm9uZT4yOTEyPC9jYmM6UG9zdGFsWm9uZT4KICAgICAgICAgICAgICAgICAgICAgICAgPGNhYzpDb3VudHJ5PgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPGNiYzpJZGVudGlmaWNhdGlvbkNvZGU+QVU8L2NiYzpJZGVudGlmaWNhdGlvbkNvZGU+CiAgICAgICAgICAgICAgICAgICAgICAgIDwvY2FjOkNvdW50cnk+CiAgICAgICAgICAgICAgICAgICAgPC9jYWM6UG9zdGFsQWRkcmVzcz4KICAgICAgICAgICAgICAgICAgICA8Y2FjOlBhcnR5TGVnYWxFbnRpdHk+CiAgICAgICAgICAgICAgICAgICAgICAgIDxjYmM6UmVnaXN0cmF0aW9uTmFtZT5XaW5kb3dzIHRvIEZpdCBQdHkgTHRkPC9jYmM6UmVnaXN0cmF0aW9uTmFtZT4KICAgICAgICAgICAgICAgICAgICAgICAgPGNiYzpDb21wYW55SUQgc2NoZW1lSUQ9IjAxNTEiPjQ3NTU1MjIyMDAwPC9jYmM6Q29tcGFueUlEPgogICAgICAgICAgICAgICAgICAgIDwvY2FjOlBhcnR5TGVnYWxFbnRpdHk+CiAgICAgICAgICAgICAgICAgICAgPGNhYzpQYXJ0eVRheFNjaGVtZT4KICAgICAgICAgICAgICAgICAgICAgICAgPGNiYzpDb21wYW55SUQ+NDc1NTUyMjIwMDA8L2NiYzpDb21wYW55SUQ+CiAgICAgICAgICAgICAgICAgICAgICAgIDxjYWM6VGF4U2NoZW1lPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPGNiYzpJRD5HU1Q8L2NiYzpJRD4KICAgICAgICAgICAgICAgICAgICAgICAgPC9jYWM6VGF4U2NoZW1lPgogICAgICAgICAgICAgICAgICAgIDwvY2FjOlBhcnR5VGF4U2NoZW1lPgogICAgICAgICAgICAgICAgPC9jYWM6UGFydHk+CiAgICAgICAgICAgIDwvY2FjOkFjY291bnRpbmdTdXBwbGllclBhcnR5PgogICAgICAgICAgICA8Y2FjOkFjY291bnRpbmdDdXN0b21lclBhcnR5PgogICAgICAgICAgICAgICAgPGNhYzpQYXJ0eT4KICAgICAgICAgICAgICAgICAgICA8Y2JjOkVuZHBvaW50SUQgc2NoZW1lSUQ9IjAxNTEiPjkxODg4MjIyMDAwPC9jYmM6RW5kcG9pbnRJRD4KICAgICAgICAgICAgICAgICAgICA8Y2FjOlBhcnR5TmFtZT4KICAgICAgICAgICAgICAgICAgICAgICAgPGNiYzpOYW1lPlRyb3R0ZXJzIFRyYWRpbmcgQ28gTHRkPC9jYmM6TmFtZT4KICAgICAgICAgICAgICAgICAgICA8L2NhYzpQYXJ0eU5hbWU+CiAgICAgICAgICAgICAgICAgICAgPGNhYzpQb3N0YWxBZGRyZXNzPgogICAgICAgICAgICAgICAgICAgICAgICA8Y2JjOlN0cmVldE5hbWU+MTAwIFF1ZWVuIFN0cmVldDwvY2JjOlN0cmVldE5hbWU+CiAgICAgICAgICAgICAgICAgICAgICAgIDxjYmM6QWRkaXRpb25hbFN0cmVldE5hbWU+UG8gYm94IDg3ODwvY2JjOkFkZGl0aW9uYWxTdHJlZXROYW1lPgogICAgICAgICAgICAgICAgICAgICAgICA8Y2JjOkNpdHlOYW1lPlN5ZG5leTwvY2JjOkNpdHlOYW1lPgogICAgICAgICAgICAgICAgICAgICAgICA8Y2JjOlBvc3RhbFpvbmU+MjAwMDwvY2JjOlBvc3RhbFpvbmU+CiAgICAgICAgICAgICAgICAgICAgICAgIDxjYWM6Q291bnRyeT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxjYmM6SWRlbnRpZmljYXRpb25Db2RlPkFVPC9jYmM6SWRlbnRpZmljYXRpb25Db2RlPgogICAgICAgICAgICAgICAgICAgICAgICA8L2NhYzpDb3VudHJ5PgogICAgICAgICAgICAgICAgICAgIDwvY2FjOlBvc3RhbEFkZHJlc3M+CiAgICAgICAgICAgICAgICAgICAgPGNhYzpQYXJ0eUxlZ2FsRW50aXR5PgogICAgICAgICAgICAgICAgICAgICAgICA8Y2JjOlJlZ2lzdHJhdGlvbk5hbWU+VHJvdHRlcnMgSW5jb3Jwb3JhdGVkPC9jYmM6UmVnaXN0cmF0aW9uTmFtZT4KICAgICAgICAgICAgICAgICAgICAgICAgPGNiYzpDb21wYW55SUQgc2NoZW1lSUQ9IjAxNTEiPjkxODg4MjIyMDAwPC9jYmM6Q29tcGFueUlEPgogICAgICAgICAgICAgICAgICAgIDwvY2FjOlBhcnR5TGVnYWxFbnRpdHk+CiAgICAgICAgICAgICAgICAgICAgPGNhYzpQYXJ0eVRheFNjaGVtZT4KICAgICAgICAgICAgICAgICAgICAgICAgPGNhYzpUYXhTY2hlbWU+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8Y2JjOkNvbXBhbnlJRD45MTg4ODIyMjAwMDwvY2JjOkNvbXBhbnlJRD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxjYmM6SUQ+R1NUPC9jYmM6SUQ+CiAgICAgICAgICAgICAgICAgICAgICAgIDwvY2FjOlRheFNjaGVtZT4KICAgICAgICAgICAgICAgICAgICA8L2NhYzpQYXJ0eVRheFNjaGVtZT4KICAgICAgICAgICAgICAgIDwvY2FjOlBhcnR5PgogICAgICAgICAgICA8L2NhYzpBY2NvdW50aW5nQ3VzdG9tZXJQYXJ0eT4KICAgICAgICAgICAgPGNhYzpUYXhUb3RhbD4KICAgICAgICAgICAgICAgIDxjYmM6VGF4QW1vdW50IGN1cnJlbmN5SUQ9IkFVRCI+MTQ4Ljc0PC9jYmM6VGF4QW1vdW50PgogICAgICAgICAgICAgICAgPGNhYzpUYXhTdWJ0b3RhbD4KICAgICAgICAgICAgICAgICAgICA8Y2JjOlRheGFibGVBbW91bnQgY3VycmVuY3lJRD0iQVVEIj4xNDg3LjQwPC9jYmM6VGF4YWJsZUFtb3VudD4KICAgICAgICAgICAgICAgICAgICA8Y2JjOlRheEFtb3VudCBjdXJyZW5jeUlEPSJBVUQiPjE0OC43NDwvY2JjOlRheEFtb3VudD4KICAgICAgICAgICAgICAgICAgICA8Y2FjOlRheENhdGVnb3J5PgogICAgICAgICAgICAgICAgICAgICAgICA8Y2JjOklEPlM8L2NiYzpJRD4KICAgICAgICAgICAgICAgICAgICAgICAgPGNiYzpQZXJjZW50PjEwPC9jYmM6UGVyY2VudD4KICAgICAgICAgICAgICAgICAgICAgICAgPGNhYzpUYXhTY2hlbWU+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8Y2JjOklEPkdTVDwvY2JjOklEPgogICAgICAgICAgICAgICAgICAgICAgICA8L2NhYzpUYXhTY2hlbWU+CiAgICAgICAgICAgICAgICAgICAgPC9jYWM6VGF4Q2F0ZWdvcnk+CiAgICAgICAgICAgICAgICA8L2NhYzpUYXhTdWJ0b3RhbD4KICAgICAgICAgICAgPC9jYWM6VGF4VG90YWw+CiAgICAgICAgICAgIDxjYWM6TGVnYWxNb25ldGFyeVRvdGFsPgogICAgICAgICAgICAgICAgPGNiYzpMaW5lRXh0ZW5zaW9uQW1vdW50IGN1cnJlbmN5SUQ9IkFVRCI+MTQ4Ny40MDwvY2JjOkxpbmVFeHRlbnNpb25BbW91bnQ+CiAgICAgICAgICAgICAgICA8Y2JjOlRheEV4Y2x1c2l2ZUFtb3VudCBjdXJyZW5jeUlEPSJBVUQiPjE0ODcuNDA8L2NiYzpUYXhFeGNsdXNpdmVBbW91bnQ+CiAgICAgICAgICAgICAgICA8Y2JjOlRheEluY2x1c2l2ZUFtb3VudCBjdXJyZW5jeUlEPSJBVUQiPjE2MzYuMTQ8L2NiYzpUYXhJbmNsdXNpdmVBbW91bnQ+CiAgICAgICAgICAgICAgICA8Y2JjOlBheWFibGVBbW91bnQgY3VycmVuY3lJRD0iQVVEIj4xNjM2LjE0PC9jYmM6UGF5YWJsZUFtb3VudD4KICAgICAgICAgICAgPC9jYWM6TGVnYWxNb25ldGFyeVRvdGFsPgogICAgICAgICAgICA8Y2FjOkludm9pY2VMaW5lPgogICAgICAgICAgICAgICAgPGNiYzpJRD4xPC9jYmM6SUQ+CiAgICAgICAgICAgICAgICA8Y2JjOk5vdGU+VGV4dHMgR2l2aW5nIE1vcmUgSW5mbyBhYm91dCB0aGUgSW52b2ljZSBMaW5lPC9jYmM6Tm90ZT4KICAgICAgICAgICAgICAgIDxjYmM6SW52b2ljZWRRdWFudGl0eSB1bml0Q29kZT0iRTk5Ij4xMDwvY2JjOkludm9pY2VkUXVhbnRpdHk+CiAgICAgICAgICAgICAgICA8Y2JjOkxpbmVFeHRlbnNpb25BbW91bnQgY3VycmVuY3lJRD0iQVVEIj4yOTkuOTA8L2NiYzpMaW5lRXh0ZW5zaW9uQW1vdW50PgogICAgICAgICAgICAgICAgPGNhYzpJdGVtPgogICAgICAgICAgICAgICAgICAgIDxjYmM6RGVzY3JpcHRpb24+V2lkZ2V0cyBUcnVlIGFuZCBGYWlyPC9jYmM6RGVzY3JpcHRpb24+CiAgICAgICAgICAgICAgICAgICAgPGNiYzpOYW1lPlRydWUtV2lkZ2V0czwvY2JjOk5hbWU+CiAgICAgICAgICAgICAgICAgICAgPGNhYzpDbGFzc2lmaWVkVGF4Q2F0ZWdvcnk+CiAgICAgICAgICAgICAgICAgICAgICAgIDxjYmM6SUQ+UzwvY2JjOklEPgogICAgICAgICAgICAgICAgICAgICAgICA8Y2JjOlBlcmNlbnQ+MTA8L2NiYzpQZXJjZW50PgogICAgICAgICAgICAgICAgICAgICAgICA8Y2FjOlRheFNjaGVtZT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxjYmM6SUQ+R1NUPC9jYmM6SUQ+CiAgICAgICAgICAgICAgICAgICAgICAgIDwvY2FjOlRheFNjaGVtZT4KICAgICAgICAgICAgICAgICAgICA8L2NhYzpDbGFzc2lmaWVkVGF4Q2F0ZWdvcnk+CiAgICAgICAgICAgICAgICA8L2NhYzpJdGVtPgogICAgICAgICAgICAgICAgPGNhYzpQcmljZT4KICAgICAgICAgICAgICAgICAgICA8Y2JjOlByaWNlQW1vdW50IGN1cnJlbmN5SUQ9IkFVRCI+MjkuOTk8L2NiYzpQcmljZUFtb3VudD4KICAgICAgICAgICAgICAgIDwvY2FjOlByaWNlPgogICAgICAgICAgICA8L2NhYzpJbnZvaWNlTGluZT4KICAgICAgICAgICAgPCEtLSBBZGRpdGlvbmFsIEludm9pY2VMaW5lcyBvbWl0dGVkIGZvciBicmV2aXR5IC0tPgogICAgICAgIDwvSW52b2ljZT4="

    result = vs.validate_xml("test.xml", encoded_data, ["AUNZ_PEPPOL_1_0_10"])
    assert result["successful"] is True

def test_xml_validate_function_invalid_rule_fail(client):
    encoded_data = "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KICAgICAgICA8SW52b2ljZSB4bWxuczpjYWM9InVybjpvYXNpczpuYW1lczpzcGVjaWZpY2F0aW9uOnVibDpzY2hlbWE6eHNkOkNvbW1vbkFnZ3JlZ2F0ZUNvbXBvbmVudHMtMiIKICAgICAgICAgICAgeG1sbnM6Y2JjPSJ1cm46b2FzaXM6bmFtZXM6c3BlY2lmaWNhdGlvbjp1Ymw6c2NoZW1hOnhzZDpDb21tb25CYXNpY0NvbXBvbmVudHMtMiIKICAgICAgICAgICAgeG1sbnM9InVybjpvYXNpczpuYW1lczpzcGVjaWZpY2F0aW9uOnVibDpzY2hlbWE6eHNkOkludm9pY2UtMiI+CiAgICAgICAgICAgIDxjYmM6Q3VzdG9taXphdGlvbklEPnVybjpjZW4uZXU6ZW4xNjkzMToyMDE3I2NvbmZvcm1hbnQjdXJuOmZkYzpwZXBwb2wuZXU6MjAxNzpwb2FjYzpiaWxsaW5nOmludGVybmF0aW9uYWw6YXVuejozLjA8L2NiYzpDdXN0b21pemF0aW9uSUQ+CiAgICAgICAgICAgIDxjYmM6UHJvZmlsZUlEPnVybjpmZGM6cGVwcG9sLmV1OjIwMTc6cG9hY2M6YmlsbGluZzowMToxLjA8L2NiYzpQcm9maWxlSUQ+CiAgICAgICAgICAgIDxjYmM6SUQ+SW52b2ljZTAxPC9jYmM6SUQ+CiAgICAgICAgICAgIDxjYmM6SXNzdWVEYXRlPjIwMTktMDctMjk8L2NiYzpJc3N1ZURhdGU+CiAgICAgICAgICAgIDxjYmM6SW52b2ljZVR5cGVDb2RlPjM4MDwvY2JjOkludm9pY2VUeXBlQ29kZT4KICAgICAgICAgICAgPGNiYzpOb3RlPlRheCBpbnZvaWNlPC9jYmM6Tm90ZT4KICAgICAgICAgICAgPGNiYzpEb2N1bWVudEN1cnJlbmN5Q29kZT5BVUQ8L2NiYzpEb2N1bWVudEN1cnJlbmN5Q29kZT4KICAgICAgICAgICAgPGNiYzpCdXllclJlZmVyZW5jZT5TaW1wbGUgc29sYXIgcGxhbjwvY2JjOkJ1eWVyUmVmZXJlbmNlPgogICAgICAgICAgICA8Y2FjOkFjY291bnRpbmdTdXBwbGllclBhcnR5PgogICAgICAgICAgICAgICAgPGNhYzpQYXJ0eT4KICAgICAgICAgICAgICAgICAgICA8Y2JjOkVuZHBvaW50SUQgc2NoZW1lSUQ9IjAxNTEiPjQ3NTU1MjIyMDAwPC9jYmM6RW5kcG9pbnRJRD4KICAgICAgICAgICAgICAgICAgICA8Y2FjOlBhcnR5TmFtZT4KICAgICAgICAgICAgICAgICAgICAgICAgPGNiYzpOYW1lPldpbmRvd3MgdG8gRml0IFB0eSBMdGQ8L2NiYzpOYW1lPgogICAgICAgICAgICAgICAgICAgIDwvY2FjOlBhcnR5TmFtZT4KICAgICAgICAgICAgICAgICAgICA8Y2FjOlBvc3RhbEFkZHJlc3M+CiAgICAgICAgICAgICAgICAgICAgICAgIDxjYmM6U3RyZWV0TmFtZT5NYWluIHN0cmVldCAxPC9jYmM6U3RyZWV0TmFtZT4KICAgICAgICAgICAgICAgICAgICAgICAgPGNiYzpBZGRpdGlvbmFsU3RyZWV0TmFtZT5Qb3N0Ym94IDEyMzwvY2JjOkFkZGl0aW9uYWxTdHJlZXROYW1lPgogICAgICAgICAgICAgICAgICAgICAgICA8Y2JjOkNpdHlOYW1lPkhhcnJpc29uPC9jYmM6Q2l0eU5hbWU+CiAgICAgICAgICAgICAgICAgICAgICAgIDxjYmM6UG9zdGFsWm9uZT4yOTEyPC9jYmM6UG9zdGFsWm9uZT4KICAgICAgICAgICAgICAgICAgICAgICAgPGNhYzpDb3VudHJ5PgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPGNiYzpJZGVudGlmaWNhdGlvbkNvZGU+QVU8L2NiYzpJZGVudGlmaWNhdGlvbkNvZGU+CiAgICAgICAgICAgICAgICAgICAgICAgIDwvY2FjOkNvdW50cnk+CiAgICAgICAgICAgICAgICAgICAgPC9jYWM6UG9zdGFsQWRkcmVzcz4KICAgICAgICAgICAgICAgICAgICA8Y2FjOlBhcnR5TGVnYWxFbnRpdHk+CiAgICAgICAgICAgICAgICAgICAgICAgIDxjYmM6UmVnaXN0cmF0aW9uTmFtZT5XaW5kb3dzIHRvIEZpdCBQdHkgTHRkPC9jYmM6UmVnaXN0cmF0aW9uTmFtZT4KICAgICAgICAgICAgICAgICAgICAgICAgPGNiYzpDb21wYW55SUQgc2NoZW1lSUQ9IjAxNTEiPjQ3NTU1MjIyMDAwPC9jYmM6Q29tcGFueUlEPgogICAgICAgICAgICAgICAgICAgIDwvY2FjOlBhcnR5TGVnYWxFbnRpdHk+CiAgICAgICAgICAgICAgICAgICAgPGNhYzpQYXJ0eVRheFNjaGVtZT4KICAgICAgICAgICAgICAgICAgICAgICAgPGNiYzpDb21wYW55SUQ+NDc1NTUyMjIwMDA8L2NiYzpDb21wYW55SUQ+CiAgICAgICAgICAgICAgICAgICAgICAgIDxjYWM6VGF4U2NoZW1lPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPGNiYzpJRD5HU1Q8L2NiYzpJRD4KICAgICAgICAgICAgICAgICAgICAgICAgPC9jYWM6VGF4U2NoZW1lPgogICAgICAgICAgICAgICAgICAgIDwvY2FjOlBhcnR5VGF4U2NoZW1lPgogICAgICAgICAgICAgICAgPC9jYWM6UGFydHk+CiAgICAgICAgICAgIDwvY2FjOkFjY291bnRpbmdTdXBwbGllclBhcnR5PgogICAgICAgICAgICA8Y2FjOkFjY291bnRpbmdDdXN0b21lclBhcnR5PgogICAgICAgICAgICAgICAgPGNhYzpQYXJ0eT4KICAgICAgICAgICAgICAgICAgICA8Y2JjOkVuZHBvaW50SUQgc2NoZW1lSUQ9IjAxNTEiPjkxODg4MjIyMDAwPC9jYmM6RW5kcG9pbnRJRD4KICAgICAgICAgICAgICAgICAgICA8Y2FjOlBhcnR5TmFtZT4KICAgICAgICAgICAgICAgICAgICAgICAgPGNiYzpOYW1lPlRyb3R0ZXJzIFRyYWRpbmcgQ28gTHRkPC9jYmM6TmFtZT4KICAgICAgICAgICAgICAgICAgICA8L2NhYzpQYXJ0eU5hbWU+CiAgICAgICAgICAgICAgICAgICAgPGNhYzpQb3N0YWxBZGRyZXNzPgogICAgICAgICAgICAgICAgICAgICAgICA8Y2JjOlN0cmVldE5hbWU+MTAwIFF1ZWVuIFN0cmVldDwvY2JjOlN0cmVldE5hbWU+CiAgICAgICAgICAgICAgICAgICAgICAgIDxjYmM6QWRkaXRpb25hbFN0cmVldE5hbWU+UG8gYm94IDg3ODwvY2JjOkFkZGl0aW9uYWxTdHJlZXROYW1lPgogICAgICAgICAgICAgICAgICAgICAgICA8Y2JjOkNpdHlOYW1lPlN5ZG5leTwvY2JjOkNpdHlOYW1lPgogICAgICAgICAgICAgICAgICAgICAgICA8Y2JjOlBvc3RhbFpvbmU+MjAwMDwvY2JjOlBvc3RhbFpvbmU+CiAgICAgICAgICAgICAgICAgICAgICAgIDxjYWM6Q291bnRyeT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxjYmM6SWRlbnRpZmljYXRpb25Db2RlPkFVPC9jYmM6SWRlbnRpZmljYXRpb25Db2RlPgogICAgICAgICAgICAgICAgICAgICAgICA8L2NhYzpDb3VudHJ5PgogICAgICAgICAgICAgICAgICAgIDwvY2FjOlBvc3RhbEFkZHJlc3M+CiAgICAgICAgICAgICAgICAgICAgPGNhYzpQYXJ0eUxlZ2FsRW50aXR5PgogICAgICAgICAgICAgICAgICAgICAgICA8Y2JjOlJlZ2lzdHJhdGlvbk5hbWU+VHJvdHRlcnMgSW5jb3Jwb3JhdGVkPC9jYmM6UmVnaXN0cmF0aW9uTmFtZT4KICAgICAgICAgICAgICAgICAgICAgICAgPGNiYzpDb21wYW55SUQgc2NoZW1lSUQ9IjAxNTEiPjkxODg4MjIyMDAwPC9jYmM6Q29tcGFueUlEPgogICAgICAgICAgICAgICAgICAgIDwvY2FjOlBhcnR5TGVnYWxFbnRpdHk+CiAgICAgICAgICAgICAgICAgICAgPGNhYzpQYXJ0eVRheFNjaGVtZT4KICAgICAgICAgICAgICAgICAgICAgICAgPGNhYzpUYXhTY2hlbWU+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8Y2JjOkNvbXBhbnlJRD45MTg4ODIyMjAwMDwvY2JjOkNvbXBhbnlJRD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxjYmM6SUQ+R1NUPC9jYmM6SUQ+CiAgICAgICAgICAgICAgICAgICAgICAgIDwvY2FjOlRheFNjaGVtZT4KICAgICAgICAgICAgICAgICAgICA8L2NhYzpQYXJ0eVRheFNjaGVtZT4KICAgICAgICAgICAgICAgIDwvY2FjOlBhcnR5PgogICAgICAgICAgICA8L2NhYzpBY2NvdW50aW5nQ3VzdG9tZXJQYXJ0eT4KICAgICAgICAgICAgPGNhYzpUYXhUb3RhbD4KICAgICAgICAgICAgICAgIDxjYmM6VGF4QW1vdW50IGN1cnJlbmN5SUQ9IkFVRCI+MTQ4Ljc0PC9jYmM6VGF4QW1vdW50PgogICAgICAgICAgICAgICAgPGNhYzpUYXhTdWJ0b3RhbD4KICAgICAgICAgICAgICAgICAgICA8Y2JjOlRheGFibGVBbW91bnQgY3VycmVuY3lJRD0iQVVEIj4xNDg3LjQwPC9jYmM6VGF4YWJsZUFtb3VudD4KICAgICAgICAgICAgICAgICAgICA8Y2JjOlRheEFtb3VudCBjdXJyZW5jeUlEPSJBVUQiPjE0OC43NDwvY2JjOlRheEFtb3VudD4KICAgICAgICAgICAgICAgICAgICA8Y2FjOlRheENhdGVnb3J5PgogICAgICAgICAgICAgICAgICAgICAgICA8Y2JjOklEPlM8L2NiYzpJRD4KICAgICAgICAgICAgICAgICAgICAgICAgPGNiYzpQZXJjZW50PjEwPC9jYmM6UGVyY2VudD4KICAgICAgICAgICAgICAgICAgICAgICAgPGNhYzpUYXhTY2hlbWU+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8Y2JjOklEPkdTVDwvY2JjOklEPgogICAgICAgICAgICAgICAgICAgICAgICA8L2NhYzpUYXhTY2hlbWU+CiAgICAgICAgICAgICAgICAgICAgPC9jYWM6VGF4Q2F0ZWdvcnk+CiAgICAgICAgICAgICAgICA8L2NhYzpUYXhTdWJ0b3RhbD4KICAgICAgICAgICAgPC9jYWM6VGF4VG90YWw+CiAgICAgICAgICAgIDxjYWM6TGVnYWxNb25ldGFyeVRvdGFsPgogICAgICAgICAgICAgICAgPGNiYzpMaW5lRXh0ZW5zaW9uQW1vdW50IGN1cnJlbmN5SUQ9IkFVRCI+MTQ4Ny40MDwvY2JjOkxpbmVFeHRlbnNpb25BbW91bnQ+CiAgICAgICAgICAgICAgICA8Y2JjOlRheEV4Y2x1c2l2ZUFtb3VudCBjdXJyZW5jeUlEPSJBVUQiPjE0ODcuNDA8L2NiYzpUYXhFeGNsdXNpdmVBbW91bnQ+CiAgICAgICAgICAgICAgICA8Y2JjOlRheEluY2x1c2l2ZUFtb3VudCBjdXJyZW5jeUlEPSJBVUQiPjE2MzYuMTQ8L2NiYzpUYXhJbmNsdXNpdmVBbW91bnQ+CiAgICAgICAgICAgICAgICA8Y2JjOlBheWFibGVBbW91bnQgY3VycmVuY3lJRD0iQVVEIj4xNjM2LjE0PC9jYmM6UGF5YWJsZUFtb3VudD4KICAgICAgICAgICAgPC9jYWM6TGVnYWxNb25ldGFyeVRvdGFsPgogICAgICAgICAgICA8Y2FjOkludm9pY2VMaW5lPgogICAgICAgICAgICAgICAgPGNiYzpJRD4xPC9jYmM6SUQ+CiAgICAgICAgICAgICAgICA8Y2JjOk5vdGU+VGV4dHMgR2l2aW5nIE1vcmUgSW5mbyBhYm91dCB0aGUgSW52b2ljZSBMaW5lPC9jYmM6Tm90ZT4KICAgICAgICAgICAgICAgIDxjYmM6SW52b2ljZWRRdWFudGl0eSB1bml0Q29kZT0iRTk5Ij4xMDwvY2JjOkludm9pY2VkUXVhbnRpdHk+CiAgICAgICAgICAgICAgICA8Y2JjOkxpbmVFeHRlbnNpb25BbW91bnQgY3VycmVuY3lJRD0iQVVEIj4yOTkuOTA8L2NiYzpMaW5lRXh0ZW5zaW9uQW1vdW50PgogICAgICAgICAgICAgICAgPGNhYzpJdGVtPgogICAgICAgICAgICAgICAgICAgIDxjYmM6RGVzY3JpcHRpb24+V2lkZ2V0cyBUcnVlIGFuZCBGYWlyPC9jYmM6RGVzY3JpcHRpb24+CiAgICAgICAgICAgICAgICAgICAgPGNiYzpOYW1lPlRydWUtV2lkZ2V0czwvY2JjOk5hbWU+CiAgICAgICAgICAgICAgICAgICAgPGNhYzpDbGFzc2lmaWVkVGF4Q2F0ZWdvcnk+CiAgICAgICAgICAgICAgICAgICAgICAgIDxjYmM6SUQ+UzwvY2JjOklEPgogICAgICAgICAgICAgICAgICAgICAgICA8Y2JjOlBlcmNlbnQ+MTA8L2NiYzpQZXJjZW50PgogICAgICAgICAgICAgICAgICAgICAgICA8Y2FjOlRheFNjaGVtZT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxjYmM6SUQ+R1NUPC9jYmM6SUQ+CiAgICAgICAgICAgICAgICAgICAgICAgIDwvY2FjOlRheFNjaGVtZT4KICAgICAgICAgICAgICAgICAgICA8L2NhYzpDbGFzc2lmaWVkVGF4Q2F0ZWdvcnk+CiAgICAgICAgICAgICAgICA8L2NhYzpJdGVtPgogICAgICAgICAgICAgICAgPGNhYzpQcmljZT4KICAgICAgICAgICAgICAgICAgICA8Y2JjOlByaWNlQW1vdW50IGN1cnJlbmN5SUQ9IkFVRCI+MjkuOTk8L2NiYzpQcmljZUFtb3VudD4KICAgICAgICAgICAgICAgIDwvY2FjOlByaWNlPgogICAgICAgICAgICA8L2NhYzpJbnZvaWNlTGluZT4KICAgICAgICAgICAgPCEtLSBBZGRpdGlvbmFsIEludm9pY2VMaW5lcyBvbWl0dGVkIGZvciBicmV2aXR5IC0tPgogICAgICAgIDwvSW52b2ljZT4="

    with pytest.raises(HTTPError) as error:
        vs.validate_xml("test.xml", encoded_data, ["Invalid"])

    assert "500 Server Error" in str(error.value)

def test_xml_validate_function_uncode_xml_fail(client):
    encoded_data = "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KICAgICAgICA8SW52b2ljZSB4bWxuczpjYWM9InVybjpvYXNpczpuYW1lczpzcGVjaWZpY2F0aW9uOnVibDpzY2hlbWE6eHNkOkNvbW1vbkFnZ3JlZ2F0ZUNvbXBvbmVudHMtMiIKICAgICAgICAgICAgeG1sbnM6Y2JjPSJ1cm46b2FzaXM6bmFtZXM6c3BlY2lmaWNhdGlvbjp1Ymw6c2NoZW1hOnhzZDpDb21tb25CYXNpY0NvbXBvbmVudHMtMiIKICAgICAgICAgICAgeG1sbnM9InVybjpvYXNpczpuYW1lczpzcGVjaWZpY2F0aW9uOnVibDpzY2hlbWE6eHNkOkludm9pY2UtMiI+CiAgICAgICAgICAgIDxjYmM6Q3VzdG9taXphdGlvbklEPnVybjpjZW4uZXU6ZW4xNjkzMToyMDE3I2NvbmZvcm1hbnQjdXJuOmZkYzpwZXBwb2wuZXU6MjAxNzpwb2FjYzpiaWxsaW5nOmludGVybmF0aW9uYWw6YXVuejozLjA8L2NiYzpDdXN0b21pemF0aW9uSUQ+CiAgICAgICAgICAgIDxjYmM6UHJvZmlsZUlEPnVybjpmZGM6cGVwcG9sLmV1OjIwMTc6cG9hY2M6YmlsbGluZzowMToxLjA8L2NiYzpQcm9maWxlSUQ+CiAgICAgICAgICAgIDxjYmM6SUQ+SW52b2ljZTAxPC9jYmM6SUQ+CiAgICAgICAgICAgIDxjYmM6SXNzdWVEYXRlPjIwMTktMDctMjk8L2NiYzpJc3N1ZURhdGU+CiAgICAgICAgICAgIDxjYmM6SW52b2ljZVR5cGVDb2RlPjM4MDwvY2JjOkludm9pY2VUeXBlQ29kZT4KICAgICAgICAgICAgPGNiYzpOb3RlPlRheCBpbnZvaWNlPC9jYmM6Tm90ZT4KICAgICAgICAgICAgPGNiYzpEb2N1bWVudEN1cnJlbmN5Q29kZT5BVUQ8L2NiYzpEb2N1bWVudEN1cnJlbmN5Q29kZT4KICAgICAgICAgICAgPGNiYzpCdXllclJlZmVyZW5jZT5TaW1wbGUgc29sYXIgcGxhbjwvY2JjOkJ1eWVyUmVmZXJlbmNlPgogICAgICAgICAgICA8Y2FjOkFjY291bnRpbmdTdXBwbGllclBhcnR5PgogICAgICAgICAgICAgICAgPGNhYzpQYXJ0eT4KICAgICAgICAgICAgICAgICAgICA8Y2JjOkVuZHBvaW50SUQgc2NoZW1lSUQ9IjAxNTEiPjQ3NTU1MjIyMDAwPC9jYmM6RW5kcG9pbnRJRD4KICAgICAgICAgICAgICAgICAgICA8Y2FjOlBhcnR5TmFtZT4KICAgICAgICAgICAgICAgICAgICAgICAgPGNiYzpOYW1lPldpbmRvd3MgdG8gRml0IFB0eSBMdGQ8L2NiYzpOYW1lPgogICAgICAgICAgICAgICAgICAgIDwvY2FjOlBhcnR5TmFtZT4KICAgICAgICAgICAgICAgICAgICA8Y2FjOlBvc3RhbEFkZHJlc3M+CiAgICAgICAgICAgICAgICAgICAgICAgIDxjYmM6U3RyZWV0TmFtZT5NYWluIHN0cmVldCAxPC9jYmM6U3RyZWV0TmFtZT4KICAgICAgICAgICAgICAgICAgICAgICAgPGNiYzpBZGRpdGlvbmFsU3RyZWV0TmFtZT5Qb3N0Ym94IDEyMzwvY2JjOkFkZGl0aW9uYWxTdHJlZXROYW1lPgogICAgICAgICAgICAgICAgICAgICAgICA8Y2JjOkNpdHlOYW1lPkhhcnJpc29uPC9jYmM6Q2l0eU5hbWU+CiAgICAgICAgICAgICAgICAgICAgICAgIDxjYmM6UG9zdGFsWm9uZT4yOTEyPC9jYmM6UG9zdGFsWm9uZT4KICAgICAgICAgICAgICAgICAgICAgICAgPGNhYzpDb3VudHJ5PgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPGNiYzpJZGVudGlmaWNhdGlvbkNvZGU+QVU8L2NiYzpJZGVudGlmaWNhdGlvbkNvZGU+CiAgICAgICAgICAgICAgICAgICAgICAgIDwvY2FjOkNvdW50cnk+CiAgICAgICAgICAgICAgICAgICAgPC9jYWM6UG9zdGFsQWRkcmVzcz4KICAgICAgICAgICAgICAgICAgICA8Y2FjOlBhcnR5TGVnYWxFbnRpdHk+CiAgICAgICAgICAgICAgICAgICAgICAgIDxjYmM6UmVnaXN0cmF0aW9uTmFtZT5XaW5kb3dzIHRvIEZpdCBQdHkgTHRkPC9jYmM6UmVnaXN0cmF0aW9uTmFtZT4KICAgICAgICAgICAgICAgICAgICAgICAgPGNiYzpDb21wYW55SUQgc2NoZW1lSUQ9IjAxNTEiPjQ3NTU1MjIyMDAwPC9jYmM6Q29tcGFueUlEPgogICAgICAgICAgICAgICAgICAgIDwvY2FjOlBhcnR5TGVnYWxFbnRpdHk+CiAgICAgICAgICAgICAgICAgICAgPGNhYzpQYXJ0eVRheFNjaGVtZT4KICAgICAgICAgICAgICAgICAgICAgICAgPGNiYzpDb21wYW55SUQ+NDc1NTUyMjIwMDA8L2NiYzpDb21wYW55SUQ+CiAgICAgICAgICAgICAgICAgICAgICAgIDxjYWM6VGF4U2NoZW1lPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPGNiYzpJRD5HU1Q8L2NiYzpJRD4KICAgICAgICAgICAgICAgICAgICAgICAgPC9jYWM6VGF4U2NoZW1lPgogICAgICAgICAgICAgICAgICAgIDwvY2FjOlBhcnR5VGF4U2NoZW1lPgogICAgICAgICAgICAgICAgPC9jYWM6UGFydHk+CiAgICAgICAgICAgIDwvY2FjOkFjY291bnRpbmdTdXBwbGllclBhcnR5PgogICAgICAgICAgICA8Y2FjOkFjY291bnRpbmdDdXN0b21lclBhcnR5PgogICAgICAgICAgICAgICAgPGNhYzpQYXJ0eT4KICAgICAgICAgICAgICAgICAgICA8Y2JjOkVuZHBvaW50SUQgc2NoZW1lSUQ9IjAxNTEiPjkxODg4MjIyMDAwPC9jYmM6RW5kcG9pbnRJRD4KICAgICAgICAgICAgICAgICAgICA8Y2FjOlBhcnR5TmFtZT4KICAgICAgICAgICAgICAgICAgICAgICAgPGNiYzpOYW1lPlRyb3R0ZXJzIFRyYWRpbmcgQ28gTHRkPC9jYmM6TmFtZT4KICAgICAgICAgICAgICAgICAgICA8L2NhYzpQYXJ0eU5hbWU+CiAgICAgICAgICAgICAgICAgICAgPGNhYzpQb3N0YWxBZGRyZXNzPgogICAgICAgICAgICAgICAgICAgICAgICA8Y2JjOlN0cmVldE5hbWU+MTAwIFF1ZWVuIFN0cmVldDwvY2JjOlN0cmVldE5hbWU+CiAgICAgICAgICAgICAgICAgICAgICAgIDxjYmM6QWRkaXRpb25hbFN0cmVldE5hbWU+UG8gYm94IDg3ODwvY2JjOkFkZGl0aW9uYWxTdHJlZXROYW1lPgogICAgICAgICAgICAgICAgICAgICAgICA8Y2JjOkNpdHlOYW1lPlN5ZG5leTwvY2JjOkNpdHlOYW1lPgogICAgICAgICAgICAgICAgICAgICAgICA8Y2JjOlBvc3RhbFpvbmU+MjAwMDwvY2JjOlBvc3RhbFpvbmU+CiAgICAgICAgICAgICAgICAgICAgICAgIDxjYWM6Q291bnRyeT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxjYmM6SWRlbnRpZmljYXRpb25Db2RlPkFVPC9jYmM6SWRlbnRpZmljYXRpb25Db2RlPgogICAgICAgICAgICAgICAgICAgICAgICA8L2NhYzpDb3VudHJ5PgogICAgICAgICAgICAgICAgICAgIDwvY2FjOlBvc3RhbEFkZHJlc3M+CiAgICAgICAgICAgICAgICAgICAgPGNhYzpQYXJ0eUxlZ2FsRW50aXR5PgogICAgICAgICAgICAgICAgICAgICAgICA8Y2JjOlJlZ2lzdHJhdGlvbk5hbWU+VHJvdHRlcnMgSW5jb3Jwb3JhdGVkPC9jYmM6UmVnaXN0cmF0aW9uTmFtZT4KICAgICAgICAgICAgICAgICAgICAgICAgPGNiYzpDb21wYW55SUQgc2NoZW1lSUQ9IjAxNTEiPjkxODg4MjIyMDAwPC9jYmM6Q29tcGFueUlEPgogICAgICAgICAgICAgICAgICAgIDwvY2FjOlBhcnR5TGVnYWxFbnRpdHk+CiAgICAgICAgICAgICAgICAgICAgPGNhYzpQYXJ0eVRheFNjaGVtZT4KICAgICAgICAgICAgICAgICAgICAgICAgPGNhYzpUYXhTY2hlbWU+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8Y2JjOkNvbXBhbnlJRD45MTg4ODIyMjAwMDwvY2JjOkNvbXBhbnlJRD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxjYmM6SUQ+R1NUPC9jYmM6SUQ+CiAgICAgICAgICAgICAgICAgICAgICAgIDwvY2FjOlRheFNjaGVtZT4KICAgICAgICAgICAgICAgICAgICA8L2NhYzpQYXJ0eVRheFNjaGVtZT4KICAgICAgICAgICAgICAgIDwvY2FjOlBhcnR5PgogICAgICAgICAgICA8L2NhYzpBY2NvdW50aW5nQ3VzdG9tZXJQYXJ0eT4KICAgICAgICAgICAgPGNhYzpUYXhUb3RhbD4KICAgICAgICAgICAgICAgIDxjYmM6VGF4QW1vdW50IGN1cnJlbmN5SUQ9IkFVRCI+MTQ4Ljc0PC9jYmM6VGF4QW1vdW50PgogICAgICAgICAgICAgICAgPGNhYzpUYXhTdWJ0b3RhbD4KICAgICAgICAgICAgICAgICAgICA8Y2JjOlRheGFibGVBbW91bnQgY3VycmVuY3lJRD0iQVVEIj4xNDg3LjQwPC9jYmM6VGF4YWJsZUFtb3VudD4KICAgICAgICAgICAgICAgICAgICA8Y2JjOlRheEFtb3VudCBjdXJyZW5jeUlEPSJBVUQiPjE0OC43NDwvY2JjOlRheEFtb3VudD4KICAgICAgICAgICAgICAgICAgICA8Y2FjOlRheENhdGVnb3J5PgogICAgICAgICAgICAgICAgICAgICAgICA8Y2JjOklEPlM8L2NiYzpJRD4KICAgICAgICAgICAgICAgICAgICAgICAgPGNiYzpQZXJjZW50PjEwPC9jYmM6UGVyY2VudD4KICAgICAgICAgICAgICAgICAgICAgICAgPGNhYzpUYXhTY2hlbWU+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8Y2JjOklEPkdTVDwvY2JjOklEPgogICAgICAgICAgICAgICAgICAgICAgICA8L2NhYzpUYXhTY2hlbWU+CiAgICAgICAgICAgICAgICAgICAgPC9jYWM6VGF4Q2F0ZWdvcnk+CiAgICAgICAgICAgICAgICA8L2NhYzpUYXhTdWJ0b3RhbD4KICAgICAgICAgICAgPC9jYWM6VGF4VG90YWw+CiAgICAgICAgICAgIDxjYWM6TGVnYWxNb25ldGFyeVRvdGFsPgogICAgICAgICAgICAgICAgPGNiYzpMaW5lRXh0ZW5zaW9uQW1vdW50IGN1cnJlbmN5SUQ9IkFVRCI+MTQ4Ny40MDwvY2JjOkxpbmVFeHRlbnNpb25BbW91bnQ+CiAgICAgICAgICAgICAgICA8Y2JjOlRheEV4Y2x1c2l2ZUFtb3VudCBjdXJyZW5jeUlEPSJBVUQiPjE0ODcuNDA8L2NiYzpUYXhFeGNsdXNpdmVBbW91bnQ+CiAgICAgICAgICAgICAgICA8Y2JjOlRheEluY2x1c2l2ZUFtb3VudCBjdXJyZW5jeUlEPSJBVUQiPjE2MzYuMTQ8L2NiYzpUYXhJbmNsdXNpdmVBbW91bnQ+CiAgICAgICAgICAgICAgICA8Y2JjOlBheWFibGVBbW91bnQgY3VycmVuY3lJRD0iQVVEIj4xNjM2LjE0PC9jYmM6UGF5YWJsZUFtb3VudD4KICAgICAgICAgICAgPC9jYWM6TGVnYWxNb25ldGFyeVRvdGFsPgogICAgICAgICAgICA8Y2FjOkludm9pY2VMaW5lPgogICAgICAgICAgICAgICAgPGNiYzpJRD4xPC9jYmM6SUQ+CiAgICAgICAgICAgICAgICA8Y2JjOk5vdGU+VGV4dHMgR2l2aW5nIE1vcmUgSW5mbyBhYm91dCB0aGUgSW52b2ljZSBMaW5lPC9jYmM6Tm90ZT4KICAgICAgICAgICAgICAgIDxjYmM6SW52b2ljZWRRdWFudGl0eSB1bml0Q29kZT0iRTk5Ij4xMDwvY2JjOkludm9pY2VkUXVhbnRpdHk+CiAgICAgICAgICAgICAgICA8Y2JjOkxpbmVFeHRlbnNpb25BbW91bnQgY3VycmVuY3lJRD0iQVVEIj4yOTkuOTA8L2NiYzpMaW5lRXh0ZW5zaW9uQW1vdW50PgogICAgICAgICAgICAgICAgPGNhYzpJdGVtPgogICAgICAgICAgICAgICAgICAgIDxjYmM6RGVzY3JpcHRpb24+V2lkZ2V0cyBUcnVlIGFuZCBGYWlyPC9jYmM6RGVzY3JpcHRpb24+CiAgICAgICAgICAgICAgICAgICAgPGNiYzpOYW1lPlRydWUtV2lkZ2V0czwvY2JjOk5hbWU+CiAgICAgICAgICAgICAgICAgICAgPGNhYzpDbGFzc2lmaWVkVGF4Q2F0ZWdvcnk+CiAgICAgICAgICAgICAgICAgICAgICAgIDxjYmM6SUQ+UzwvY2JjOklEPgogICAgICAgICAgICAgICAgICAgICAgICA8Y2JjOlBlcmNlbnQ+MTA8L2NiYzpQZXJjZW50PgogICAgICAgICAgICAgICAgICAgICAgICA8Y2FjOlRheFNjaGVtZT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxjYmM6SUQ+R1NUPC9jYmM6SUQ+CiAgICAgICAgICAgICAgICAgICAgICAgIDwvY2FjOlRheFNjaGVtZT4KICAgICAgICAgICAgICAgICAgICA8L2NhYzpDbGFzc2lmaWVkVGF4Q2F0ZWdvcnk+CiAgICAgICAgICAgICAgICA8L2NhYzpJdGVtPgogICAgICAgICAgICAgICAgPGNhYzpQcmljZT4KICAgICAgICAgICAgICAgICAgICA8Y2JjOlByaWNlQW1vdW50IGN1cnJlbmN5SUQ9IkFVRCI+MjkuOTk8L2NiYzpQcmljZUFtb3VudD4KICAgICAgICAgICAgICAgIDwvY2FjOlByaWNlPgogICAgICAgICAgICA8L2NhYzpJbnZvaWNlTGluZT4KICAgICAgICAgICAgPCEtLSBBZGRpdGlvbmFsIEludm9pY2VMaW5lcyBvbWl0dGVkIGZvciBicmV2aXR5IC0tPgogICAgICAgIDwvSW52b2ljZT4="
    decoded_data = base64.b64decode(encoded_data)
    xml_data = decoded_data.decode('utf-8')

    with pytest.raises(HTTPError) as error:
        vs.validate_xml("test.xml", xml_data, ["AUNZ_PEPPOL_1_0_10"])

    assert "500 Server Error" in str(error.value)







#def test_xml_validate_success(client):
#    data = {
#        """<?xml version="1.0" encoding="UTF-8"?>
#        <Invoice xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
#            xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"
#            xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2">
#            <cbc:CustomizationID>urn:cen.eu:en16931:2017#conformant#urn:fdc:peppol.eu:2017:poacc:billing:international:aunz:3.0</cbc:CustomizationID>
#            <cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID>
#            <cbc:ID>Invoice01</cbc:ID>
#            <cbc:IssueDate>2019-07-29</cbc:IssueDate>
#            <cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
#            <cbc:Note>Tax invoice</cbc:Note>
#            <cbc:DocumentCurrencyCode>AUD</cbc:DocumentCurrencyCode>
#            <cbc:BuyerReference>Simple solar plan</cbc:BuyerReference>
#            <cac:AccountingSupplierParty>
#                <cac:Party>
#                    <cbc:EndpointID schemeID="0151">47555222000</cbc:EndpointID>
#                    <cac:PartyName>
#                        <cbc:Name>Windows to Fit Pty Ltd</cbc:Name>
#                    </cac:PartyName>
#                    <cac:PostalAddress>
#                        <cbc:StreetName>Main street 1</cbc:StreetName>
#                        <cbc:AdditionalStreetName>Postbox 123</cbc:AdditionalStreetName>
#                        <cbc:CityName>Harrison</cbc:CityName>
#                        <cbc:PostalZone>2912</cbc:PostalZone>
#                        <cac:Country>
#                            <cbc:IdentificationCode>AU</cbc:IdentificationCode>
#                        </cac:Country>
#                    </cac:PostalAddress>
#                    <cac:PartyLegalEntity>
#                        <cbc:RegistrationName>Windows to Fit Pty Ltd</cbc:RegistrationName>
#                        <cbc:CompanyID schemeID="0151">47555222000</cbc:CompanyID>
#                    </cac:PartyLegalEntity>
#                    <cac:PartyTaxScheme>
#                        <cbc:CompanyID>47555222000</cbc:CompanyID>
#                        <cac:TaxScheme>
#                            <cbc:ID>GST</cbc:ID>
#                        </cac:TaxScheme>
#                    </cac:PartyTaxScheme>
#                </cac:Party>
#            </cac:AccountingSupplierParty>
#            <cac:AccountingCustomerParty>
#                <cac:Party>
#                    <cbc:EndpointID schemeID="0151">91888222000</cbc:EndpointID>
#                    <cac:PartyName>
#                        <cbc:Name>Trotters Trading Co Ltd</cbc:Name>
#                    </cac:PartyName>
#                    <cac:PostalAddress>
#                        <cbc:StreetName>100 Queen Street</cbc:StreetName>
#                        <cbc:AdditionalStreetName>Po box 878</cbc:AdditionalStreetName>
#                        <cbc:CityName>Sydney</cbc:CityName>
#                        <cbc:PostalZone>2000</cbc:PostalZone>
#                        <cac:Country>
#                            <cbc:IdentificationCode>AU</cbc:IdentificationCode>
#                        </cac:Country>
#                    </cac:PostalAddress>
#                    <cac:PartyLegalEntity>
#                        <cbc:RegistrationName>Trotters Incorporated</cbc:RegistrationName>
#                        <cbc:CompanyID schemeID="0151">91888222000</cbc:CompanyID>
#                    </cac:PartyLegalEntity>
#                    <cac:PartyTaxScheme>
#                        <cac:TaxScheme>
#                            <cbc:CompanyID>91888222000</cbc:CompanyID>
#                            <cbc:ID>GST</cbc:ID>
#                        </cac:TaxScheme>
#                    </cac:PartyTaxScheme>
#                </cac:Party>
#            </cac:AccountingCustomerParty>
#            <cac:TaxTotal>
#                <cbc:TaxAmount currencyID="AUD">148.74</cbc:TaxAmount>
#                <cac:TaxSubtotal>
#                    <cbc:TaxableAmount currencyID="AUD">1487.40</cbc:TaxableAmount>
#                    <cbc:TaxAmount currencyID="AUD">148.74</cbc:TaxAmount>
#                    <cac:TaxCategory>
#                        <cbc:ID>S</cbc:ID>
#                        <cbc:Percent>10</cbc:Percent>
#                        <cac:TaxScheme>
#                            <cbc:ID>GST</cbc:ID>
#                        </cac:TaxScheme>
#                    </cac:TaxCategory>
#                </cac:TaxSubtotal>
#            </cac:TaxTotal>
#            <cac:LegalMonetaryTotal>
#                <cbc:LineExtensionAmount currencyID="AUD">1487.40</cbc:LineExtensionAmount>
#                <cbc:TaxExclusiveAmount currencyID="AUD">1487.40</cbc:TaxExclusiveAmount>
#                <cbc:TaxInclusiveAmount currencyID="AUD">1636.14</cbc:TaxInclusiveAmount>
#                <cbc:PayableAmount currencyID="AUD">1636.14</cbc:PayableAmount>
#            </cac:LegalMonetaryTotal>
#            <cac:InvoiceLine>
#                <cbc:ID>1</cbc:ID>
#                <cbc:Note>Texts Giving More Info about the Invoice Line</cbc:Note>
#                <cbc:InvoicedQuantity unitCode="E99">10</cbc:InvoicedQuantity>
#                <cbc:LineExtensionAmount currencyID="AUD">299.90</cbc:LineExtensionAmount>
#                <cac:Item>
#                    <cbc:Description>Widgets True and Fair</cbc:Description>
#                    <cbc:Name>True-Widgets</cbc:Name>
#                    <cac:ClassifiedTaxCategory>
#                        <cbc:ID>S</cbc:ID>
#                        <cbc:Percent>10</cbc:Percent>
#                        <cac:TaxScheme>
#                            <cbc:ID>GST</cbc:ID>
#                        </cac:TaxScheme>
#                    </cac:ClassifiedTaxCategory>
#                </cac:Item>
#                <cac:Price>
#                    <cbc:PriceAmount currencyID="AUD">29.99</cbc:PriceAmount>
#                </cac:Price>
#            </cac:InvoiceLine>
#            <!-- Additional InvoiceLines omitted for brevity -->
#        </Invoice>"""
#    }
#    data_list = list(data)
#    res = client.post(
#        VALIDATION_PATH,
#        data=json.dumps(data_list),
#        content_type="application/json"
#    )
#  
#    assert res.status_code == 201
#
#
#def test_empty_xml_fail(client):
#    data = {}
#    res = client.post(
#        VALIDATION_PATH,
#        data=json.dumps(data),
#        content_type="application/json"
#    )
#  
#    assert res.status_code == 400
#
#def test_xml_missing_data_fail(client):
#    data = {
#        """<?xml version="1.0" encoding="UTF-8"?>
#        <Invoice xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
#            xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"
#            xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2">
#            <cbc:CustomizationID>urn:cen.eu:en16931:2017#conformant#urn:fdc:peppol.eu:2017:poacc:billing:international:aunz:3.0</cbc:CustomizationID>
#            <cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID>
#            <cbc:ID>Invoice01</cbc:ID>
#            <cbc:IssueDate>2019-07-29</cbc:IssueDate>
#            <cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
#            <cbc:Note>Tax invoice</cbc:Note>
#            <cbc:DocumentCurrencyCode>AUD</cbc:DocumentCurrencyCode>
#            <cbc:BuyerReference>Simple solar plan</cbc:BuyerReference>
#            <cac:AccountingSupplierParty>
#                <cac:Party>
#                    <cbc:EndpointID schemeID="0151">47555222000</cbc:EndpointID>
#                    <cac:PostalAddress>
#                        <cbc:StreetName>Main street 1</cbc:StreetName>
#                        <cbc:AdditionalStreetName>Postbox 123</cbc:AdditionalStreetName>
#                        <cbc:CityName>Harrison</cbc:CityName>
#                        <cbc:PostalZone>2912</cbc:PostalZone>
#                        <cac:Country>
#                            <cbc:IdentificationCode>AU</cbc:IdentificationCode>
#                        </cac:Country>
#                    </cac:PostalAddress>
#                    <cac:PartyLegalEntity>
#                        <cbc:RegistrationName>Windows to Fit Pty Ltd</cbc:RegistrationName>
#                        <cbc:CompanyID schemeID="0151">47555222000</cbc:CompanyID>
#                    </cac:PartyLegalEntity>
#                    <cac:PartyTaxScheme>
#                        <cbc:CompanyID>47555222000</cbc:CompanyID>
#                        <cac:TaxScheme>
#                            <cbc:ID>GST</cbc:ID>
#                        </cac:TaxScheme>
#                    </cac:PartyTaxScheme>
#                </cac:Party>
#            </cac:AccountingSupplierParty>
#            <cac:AccountingCustomerParty>
#                <cac:Party>
#                    <cbc:EndpointID schemeID="0151">91888222000</cbc:EndpointID>
#                    <cac:PartyLegalEntity>
#                        <cbc:RegistrationName>Trotters Incorporated</cbc:RegistrationName>
#                        <cbc:CompanyID schemeID="0151">91888222000</cbc:CompanyID>
#                    </cac:PartyLegalEntity>
#                    <cac:PartyTaxScheme>
#                        <cac:TaxScheme>
#                            <cbc:CompanyID>91888222000</cbc:CompanyID>
#                            <cbc:ID>GST</cbc:ID>
#                        </cac:TaxScheme>
#                    </cac:PartyTaxScheme>
#                </cac:Party>
#            </cac:AccountingCustomerParty>
#            <cac:TaxTotal>
#                <cbc:TaxAmount currencyID="AUD">148.74</cbc:TaxAmount>
#                <cac:TaxSubtotal>
#                    <cbc:TaxableAmount currencyID="AUD">1487.40</cbc:TaxableAmount>
#                    <cbc:TaxAmount currencyID="AUD">148.74</cbc:TaxAmount>
#                    <cac:TaxCategory>
#                        <cbc:ID>S</cbc:ID>
#                        <cbc:Percent>10</cbc:Percent>
#                        <cac:TaxScheme>
#                            <cbc:ID>GST</cbc:ID>
#                        </cac:TaxScheme>
#                    </cac:TaxCategory>
#                </cac:TaxSubtotal>
#            </cac:TaxTotal>
#            <cac:InvoiceLine>
#                <cbc:ID>1</cbc:ID>
#                <cbc:Note>Texts Giving More Info about the Invoice Line</cbc:Note>
#                <cbc:InvoicedQuantity unitCode="E99">10</cbc:InvoicedQuantity>
#                <cbc:LineExtensionAmount currencyID="AUD">299.90</cbc:LineExtensionAmount>
#                <cac:Price>
#                    <cbc:PriceAmount currencyID="AUD">29.99</cbc:PriceAmount>
#                </cac:Price>
#            </cac:InvoiceLine>
#            <!-- Additional InvoiceLines omitted for brevity -->
#        </Invoice>"""
#    }
#    my_list = list(data)
#    res = client.post(
#        VALIDATION_PATH,
#        data=json.dumps(my_list),
#        content_type="application/json"
#    )
#  
#  
#    assert res.status_code == 400