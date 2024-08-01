from app import app
from model import db, User, Searches
from flask_jwt_extended import create_access_token
import pytest

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            user = User(first_name="Test", last_name="User", email="test@example.com", password="password")
            db.session.add(user)
            db.session.commit()
            token = create_access_token(identity=user.id)

            yield client, token

def test_search_history_endpoint_exists(client):
    client, token = client
    response = client.get('/searchhistory', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
