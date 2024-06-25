import base64
import pytest
import json
import os
import io

from tests.fixtures import client  
from werkzeug.datastructures import FileStorage

CREATION_PATH = '/creation/creationupload'


def test_file_upload_successful(client):
    file = FileStorage(
        stream=open("file1.pdf", "rb"),
        filename="file1.pdf",
        content_type="application/pdf",
    )
    data = {}
    data['files'] = [file]
    res = client.post(
        CREATION_PATH,
        data=data,  
        content_type='multipart/form-data',
        follow_redirects=True
    )
    response_body = res.get_json()

    assert res.status_code == 200
    assert response_body['message'] == 'Files received'

    
def test_file_upload_successful(client):
    data = {}
    data['files'] = [(io.BytesIO(b"abcdef"), 'test.pdf'),(io.BytesIO(b"abcdef"), 'd.json')]
    
    res = client.post(
        CREATION_PATH,
        data=data,
        content_type='multipart/form-data',
        follow_redirects=True
    )
    response_body = res.get_json()

    assert res.status_code == 200
    assert response_body['message'] == 'Files received'
    
    
def test_empty_file_upload_fail(client):
    data = {}
    data['files'] = []
    
    res = client.post(
        CREATION_PATH,
        data=data,
        content_type='multipart/form-data',
        follow_redirects=True
    )
    response_body = res.get_json()

    assert res.status_code == 400
    assert response_body['message'] == 'No files found in the request'
    
    
def test_invalid_file_upload_fail(client):
    data = {}
    data['files'] = [(io.BytesIO(b"abcdef"), 'test.jpg')]
    
    res = client.post(
        CREATION_PATH,
        data=data,
        content_type='multipart/form-data',
        follow_redirects=True
    )
    response_body = res.get_json()

    assert res.status_code == 400
    assert response_body['message'] == 'File test.jpg is not a PDF or JSON'