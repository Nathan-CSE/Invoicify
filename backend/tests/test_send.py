import base64
import pytest
import json
import os
import io

from tests.fixtures import client  
from werkzeug.datastructures import FileStorage
from models import db, User
from src.services.utils import salt_and_hash, db_insert

CREATION_PATH = '/creation/creationupload'

@pytest.fixture
def user(client):
    user = User(email="abc@gmail.com", password=salt_and_hash("abc"), token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFiY0BnbWFpbC5jb20ifQ.t5iNUNMkVVEVGNcPx8UdmwWgIMJ22j36xn4kXB-e-qM")
    
    db_insert(user)
    return user

def test_file_upload_no_perms(client):
    data = {}
    data['files'] = [(io.BytesIO(b"abcdef"), 'test.pdf')]
    
    res = client.post(
        CREATION_PATH,
        data=data,  
        content_type='multipart/form-data',
        follow_redirects=True
    )

    assert res.status_code == 403

def test_file_upload_successful(client, user):
    data = {}
    data['files'] = [(io.BytesIO(b"abcdef"), 'test.pdf')]
    
    res = client.post(
        CREATION_PATH,
        headers={
            "Authorisation": user.token
        },
        data=data,  
        content_type='multipart/form-data',
        follow_redirects=True
    )
    response_body = res.get_json()

    assert res.status_code == 200
    assert response_body['message'] == 'XMLs created'

    
def test_multiple_files_upload_successful(client, user):
    data = {}
    data['files'] = [(io.BytesIO(b"abcdef"), 'test.pdf'),(io.BytesIO(b"abcdef"), 'd.json')]
    
    res = client.post(
        CREATION_PATH,
        headers={
            "Authorisation": user.token
        },
        data=data,
        content_type='multipart/form-data',
        follow_redirects=True
    )
    response_body = res.get_json()

    assert res.status_code == 200
    assert response_body['message'] == 'XMLs created'
    
    
def test_empty_file_upload_fail(client, user):
    data = {}
    data['files'] = []
    
    res = client.post(
        CREATION_PATH,
        headers={
            "Authorisation": user.token
        },
        data=data,
        content_type='multipart/form-data',
        follow_redirects=True
    )
    response_body = res.get_json()

    assert res.status_code == 400
    assert response_body['message'] == 'No files were uploaded'
    
    
def test_invalid_file_upload_fail(client, user):
    data = {}
    data['files'] = [(io.BytesIO(b"abcdef"), 'test.jpg')]
    
    res = client.post(
        CREATION_PATH,
        headers={
            "Authorisation": user.token
        },
        data=data,
        content_type='multipart/form-data',
        follow_redirects=True
    )
    response_body = res.get_json()

    assert res.status_code == 400
    assert response_body['message'] == 'test.jpg is not a PDF or JSON, please remove that file and try again'