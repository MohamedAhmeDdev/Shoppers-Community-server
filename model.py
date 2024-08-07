from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import MetaData
from datetime import datetime

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)
db = SQLAlchemy(metadata=metadata)
class User(db.Model, SerializerMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(100), nullable=True)
    reset_token = db.Column(db.String(255), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)
    searches = db.relationship("Searches", back_populates="user", cascade="all, delete-orphan")
    serialize_rules = ("-searches.user",)
    def __repr__(self):
        return f'<User {self.id}, {self.first_name}, {self.last_name}>'
class Product(db.Model, SerializerMixin):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    ratings = db.Column(db.Float, nullable=True)
    mode_of_payment = db.Column(db.String, nullable=True)
    categoryId = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    shopId = db.Column(db.Integer, db.ForeignKey('shops.id'), nullable=False)
    product_image = db.Column(db.String, nullable=True)
    searches = db.relationship("Searches", back_populates="product")
    shop = db.relationship("Shop", back_populates="products")
    serialize_rules = ("-searches", "-shop.products",)
    def __repr__(self):
        return f'<Product {self.id}, {self.name}, {self.price}>'
class Shop(db.Model, SerializerMixin):
    __tablename__ = "shops"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    products = db.relationship("Product", back_populates="shop")
    serialize_rules = ("-products.shop",)
    def __repr__(self):
        return f'<Shop {self.id}, {self.name}>'
class Category(db.Model, SerializerMixin):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category_image = db.Column(db.String, nullable=True)
    def __repr__(self):
        return f'<Category {self.id}, {self.name}>'
class Searches(db.Model, SerializerMixin):
    __tablename__ = "searches"
    id = db.Column(db.Integer, primary_key=True)
    productId = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    product = db.relationship("Product", back_populates="searches")
    user = db.relationship("User", back_populates="searches")

    serialize_rules = ("-product", "-user",)
    def __repr__(self):
        return f'<Search {self.id}, User {self.userId}, Product {self.productId}>'