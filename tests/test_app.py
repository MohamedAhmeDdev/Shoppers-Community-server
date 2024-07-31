from app import index, searches
from model import Searches


def test_index():
    assert index() == "Hello, world!"

def test_searches():
    # Create some sample search data
    Searches.query.all.return_value = [
        Searches(products="Product 1"),
        Searches(products="Product 2")
    ]

    # Test the searches function
    response = searches()
    assert response.status_code == 200
    assert response.json == [
        {"products": "Product 1"},
        {"products": "Product 2"}
    ]

