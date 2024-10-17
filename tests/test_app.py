import pytest
from checkserve.app import create_app

@pytest.fixture
def app():
    app = create_app('testing')
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_hello_world(client):
    response = client.get('/')
    assert response.status_code == 200