import base64
import pytest
import json
import os
import io

from tests.fixtures import client  # Assuming you have a fixture for Flask test client

CREATION_PATH = '/creation/creationupload'

def test_file_upload(client):
    data = {}
    data['file'] = (io.BytesIO(b"abcdef"), 'test.pdf')
    
    res = client.post(
        CREATION_PATH,
        data=data,
        content_type='multipart/form-data',
        follow_redirects=True
    )
    response_body = res.get_json()

    assert res.status_code == 200
    assert response_body['message'] == 'Files received'