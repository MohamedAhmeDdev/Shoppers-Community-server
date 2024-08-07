import pytest
import json
from app import app, db, User
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
import secrets

bcrypt = Bcrypt(app)
mail = Mail(app)

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

@pytest.fixture
def setup_users(client):
    hashed_password = bcrypt.generate_password_hash('testpassword').decode('utf-8')
    user = User(first_name='John', last_name='Doe', email='john.doe@example.com', password=hashed_password)
    db.session.add(user)
    db.session.commit()

def test_register_success(client):
    response = client.post('/register', json={
        'first_name': 'Jane',
        'last_name': 'Doe',
        'email': 'jane.doe@example.com',
        'password': 'newpassword'
    })
    data = response.get_json()

    assert response.status_code == 201
    assert data['message'] == 'User registered successfully. Please check your email to verify your account.'

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
