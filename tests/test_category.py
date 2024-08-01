import pytest
from app import app, db, Category

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

@pytest.fixture
def setup_categories(client):
    category1 = Category(id=1, name="Electronics")
    category2 = Category(id=2, name="Clothing")
    db.session.add(category1)
    db.session.add(category2)
    db.session.commit()

def test_get_categories(client, setup_categories):
    response = client.get('/categories')
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]['name'] == "Electronics"
    assert data[1]['name'] == "Clothing"

def test_get_categories_no_results(client):
    Category.query.delete()
    db.session.commit()

    response = client.get('/categories')
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 0
