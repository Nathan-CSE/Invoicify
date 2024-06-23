import pytest

from app import create_app

@pytest.fixture
def client():
    app = create_app(":memory:")
    with app.app_context():
        yield app.test_client()