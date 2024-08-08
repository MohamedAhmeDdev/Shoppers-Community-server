import pytest
import json
from app import app, db
from flask_bcrypt import Bcrypt
import jwt
import datetime
from resources.user import User

bcrypt = Bcrypt(app)

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

@pytest.fixture
def setup_users(client):
    # Add a test user
    hashed_password = bcrypt.generate_password_hash('testpassword').decode('utf-8')
    user = User(first_name='John', last_name='Doe', email='john.doe@example.com', password=hashed_password, is_verified=True)
    db.session.add(user)
    db.session.commit()

@pytest.fixture
def setup_unverified_user(client):
    # Add an unverified user
    hashed_password = bcrypt.generate_password_hash('testpassword').decode('utf-8')
    user = User(first_name='Jane', last_name='Doe', email='jane.doe@example.com', password=hashed_password, is_verified=False)
    db.session.add(user)
    db.session.commit()

def test_login_success(client, setup_users):
    response = client.post('/login', json={
        'email': 'john.doe@example.com',
        'password': 'testpassword'
    })
    data = response.get_json()

    assert response.status_code == 200
    assert 'token' in data

def test_login_invalid_credentials(client, setup_users):
    response = client.post('/login', json={
        'email': 'john.doe@example.com',
        'password': 'wrongpassword'
    })
    data = response.get_json()

    assert response.status_code == 401
    assert data['message'] == 'Invalid credentials'

def test_login_nonexistent_user(client):
    response = client.post('/login', json={
        'email': 'nonexistent@example.com',
        'password': 'somepassword'
    })
    data = response.get_json()

    assert response.status_code == 401
    assert data['message'] == 'Invalid credentials'

def test_login_unverified_user(client, setup_unverified_user):
    response = client.post('/login', json={
        'email': 'jane.doe@example.com',
        'password': 'testpassword'
    })
    data = response.get_json()

    assert response.status_code == 403
    assert data['message'] == 'Account not Verified. Please check your email.'
