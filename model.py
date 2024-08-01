from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import MetaData

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

class User(db.Model, SerializerMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    # products = db.relationship("Product", back_populates = "user", cascade = "all, delete-orphan")

    def __repr__(self):
        return f'<User {self.id},{self.first_name}, {self.last_name}>'
    
class Product(db.Model, SerializerMixin):
    __tablename__= "products"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    ratings = db.Column(db.Float)
    mode_of_payment = db.Column(db.String)
    categoryId = db.Column(db.Integer, db.ForeignKey('categories.id'))
    shopId = db.Column(db.Integer, db.ForeignKey('shops.id'))
    product_image = db.Column(db.String)
    user = db.relationship("Searches", back_populates = "products")
    shop = db.relationship("Shop", back_populates = "products")
    serialize_rules = ('-user, -shop',)

    def __repr__(self):
        return f'<Product {self.name}, {self.price}>'
    
class Shop(db.Model, SerializerMixin):
    __tablename__ = "shops"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    products = db.relationship("Product", back_populates = "shop")
    serialize_rules = ("-products",)

    def __repr__(self):
        return f'Shop {self.name}'

class Category(db.Model, SerializerMixin):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    category_image = db.Column(db.String)

class Searches(db.Model, SerializerMixin):
    __tablename__ = "searches"
    id = db.Column(db.Integer, primary_key=True)
    productId = db.Column(db.Integer, db.ForeignKey('products.id'))
    userId = db.Column(db.Integer, db.ForeignKey('users.id')) 
    products = db.relationship("Product", back_populates="user")
    user = db.relationship("User") 

    serialize_rules = ("-products", "-user")  

    def __repr__(self):
        return f'<Search {self.id}, User {self.userId}, Product {self.productId}>'


    