# # test_product.py

# import pytest
# from app import app, db, Product, Shop
# # from resources.shop import Shop

# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         with app.app_context():
#             db.create_all()
#             yield client

            

# @pytest.fixture
# def setup_db(client):
 
#     if not Shop.query.filter_by(id=1).first():
#         shop1 = Shop(id=1, name="Shop 1")
#         db.session.add(shop1)
#     if not Shop.query.filter_by(id=2).first():
#         shop2 = Shop(id=2, name="Shop 2")
#         db.session.add(shop2)
    
   
#     if not Product.query.filter_by(id=1).first():
#         product1 = Product(id=1, name="Product 1", price=100, ratings=4.5, mode_of_payment="Credit", categoryId=1, shopId=1)
#         db.session.add(product1)
#     if not Product.query.filter_by(id=2).first():
#         product2 = Product(id=2, name="Product 2", price=200, ratings=3.5, mode_of_payment="Cash", categoryId=1, shopId=2)
#         db.session.add(product2)
    
#     db.session.commit()



# def test_get_products_by_category(client, setup_db):
#     response = client.get('/categories/1/')
#     data = response.get_json()

#     assert response.status_code == 200
#     assert 'products_by_shop' in data
#     assert 'product_names' in data
#     assert len(data['products_by_shop']) == 2  
#     assert 'Product 1' in data['product_names']
#     assert 'Product 2' in data['product_names']

# def test_get_products_by_category_no_products(client):
#     response = client.get('/categories/999/')
#     data = response.get_json()

#     assert response.status_code == 404
#     assert data['message'] == "No products found for this category with the applied filters"

