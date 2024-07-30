from model import db, Product, Shop, Category
from app import app


with app.app_context():
    print("Deleting data.....")

    Product.query.delete()
    Shop.query.delete()
    Category.query.delete()

    print("Creating data .....")

    s1 = Shop(name = "Amazon")
    s2 = Shop(name = "Alibaba")

    c1 = Category(name = "Electronics")
    c2 = Category(name = "Furniture")

    e1 = Product(
        name = "Samsung A05",
        price = 30000.00,
        ratings = 4.7,
        mode_of_payment = "After delivery",
        categoryId = 1,
        shopId = 1,
        product_image = ""


    )
    e2 = Product(
        name = "Samsung A05",
        price = 33000.00,
        ratings = 4.7,
        mode_of_payment = "After delivery",
        categoryId = 1,
        shopId = 2,
        product_image = ""


    )

    e3 = Product(
        name = "Hp EliteBook 840 G3",
        price = 29999.00,
        ratings = 4,
        mode_of_payment = "After Delivery",
        categoryId = 1,
        shopId = 1,
        product_image = ''
    )


    e4 = Product(
        name = "Hp EliteBook 840 G3",
        price = 29000.00,
        ratings = 4,
        mode_of_payment = "After Delivery",
        categoryId = 1,
        shopId = 2,
        product_image = ''
    )


    f1 = Product(
        name= "5-Seater Corporate Sofa",
        price = 69999.00,
        ratings = 3,
        mode_of_payment = "Upfront",
        categoryId = 2,
        shopId = 1,
        product_image = ""
    )



    f2 = Product(
        name= "5-Seater Corporate Sofa",
        price = 70000.00,
        ratings = 3,
        mode_of_payment = "Upfront",
        categoryId = 2,
        shopId = 2,
        product_image = ""
    )
    f3 = Product(
        name = "HarMony King Bed Only",
        price = 75000.00,
        ratings = 5,
        categoryId = 2,
        mode_of_payment = "After Delivery",
        shopId = 1,
        product_image = ""
    )

    f4 = Product(
        name = "HarMony King Bed Only",
        price = 75000.00,
        ratings = 5,
        categoryId = 2,
        shopId = 2,
        mode_of_payment = "Upfront",
        product_image = ""
    )

    categories = [c1,c2]
    shops = [s1,s2]
    electronics = [e1,e2,e3,e4]
    furnitures = [f1,f2,f3,f4]

    db.session.add_all(electronics)
    db.session.add_all(furnitures)
    db.session.add_all(shops)
    db.session.add_all(categories)

    db.session.commit()

    print("Seeding done")