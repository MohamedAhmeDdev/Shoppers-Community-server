from app import app
from model import db, User, Searches
from flask_jwt_extended import create_access_token
import pytest
import uuid  # Import the uuid module

@pytest.fixture
def client():
    unique_email = f"test{uuid.uuid4()}@example.com"
    with app.test_client() as client:
        with app.app_context():
            existing_user = User.query.filter_by(email=unique_email).first()
            if existing_user:
                db.session.delete(existing_user)
                db.session.commit()
            
            user = User(first_name="Test", last_name="User", email=unique_email, password="password")
            db.session.add(user)
            db.session.commit()
            token = create_access_token(identity=user.id)

            yield client, token

def test_search_history_endpoint_exists(client):
    client, token = client
    response = client.get('/searchhistory', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    response_json = response.get_json()
    assert isinstance(response_json, dict)
    assert "products" in response_json
    assert isinstance(response_json["products"], list)
