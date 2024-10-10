import pytest

from src.checkserve.app import app


@pytest.fixture
def client():
    """Creates a test client for the Flask app."""
    with app.test_client() as client:
        yield client

def test_app_exists():
    """Test that the app instance exists."""
    assert app is not None

def test_homepage_status_code(client):
    """Test that the homepage returns a 200 status code."""
    response = client.get('/')
    assert response.status_code == 200

def test_homepage_content(client):
    """Test that the homepage contains 'Hello World!'."""
    response = client.get('/')
    assert b'Hello World!' in response.data
