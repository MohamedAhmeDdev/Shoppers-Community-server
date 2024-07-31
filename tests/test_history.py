from app import index,app
from model import Searches
import pytest

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_search_history_endpoint_exists(client):
    response = client.get('/searchhistory')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)