import pytest
import json
from app import app, db, Product, User

from flask_bcrypt import Bcrypt
import jwt
import datetime

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
    user = User(first_name='John', last_name='Doe', email='john.doe@example.com', password=hashed_password)
    db.session.add(user)
    db.session.commit()

def test_register_success(client):
    response = client.post('/register', json={
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'password': 'newpassword'
    })
    data = response.get_json()

    assert response.status_code == 201
    assert data['message'] == 'User registered successfully'

def test_register_duplicate_email(client, setup_users):
    response = client.post('/register', json={
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'password': 'newpassword'
    })
    data = response.get_json()

    assert response.status_code == 400
    assert data['message'] == 'Email already exists'