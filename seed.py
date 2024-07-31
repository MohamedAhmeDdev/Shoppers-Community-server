from model import db, Product, Shop, Category 
from app import app


with app.app_context():

    Product.query.delete()
    Shop.query.delete()
    Category.query.delete()

s3 = Shop(name ="Jumia")
s4 = Shop(name ="Kilimall") 

c3 =Product(name ="Clothing")
c4 =Product(name ="Sports and Outdoors")

cl1 = Product(
    name = "Fashion Men's Simple T-Shirt Short Sleeve",
    price = 847.00,
    ratings = 4.2,
    mode_of_payment = "Upfront",
    category = 3,
    shopId = 3,
    product_image = ""

)

cl2 = Product(
    name = "Fashion Men's Simple T-Shirt Short Sleeve",
    price = 500.00,
    ratings = 4.0,
    mode_of_payment = "Before delivery",
    category = 3,
    shopId = 4,
    product_image = ""

)

cl3 = Product(
    name = "khaki trouser",
    price = 1000.00,
    ratings = 4.8,
    mode_of_payment = "After delivery",
    category = 3,
    shopId = 3,
    product_image = ""
)

cl4 = Product(
    name = "khaki trouser",
    price = 800.00,
    ratings = 4.0,
    mode_of_payment = "Before delivery",
    category = 3,
    shopId = 4,
    product_image = ""
)

cl5 = Product(
    name = "adidas samba-white/red/grey",
    price = 5000.00,
    ratings = 5.0,
    mode_of_payment = "After delivery",
    category = 3,
    shopId = 3,
    product_image = ""
)

cl6 = Product(
    name = "adidas samba-white/red/grey",
    price = 3000.00,
    ratings = 4.5,
    mode_of_payment = "Before delivery",
    category = 3,
    shopId = 4,
    product_image = ""
)

cl7 = Product(
    name = "ladies cotton tanktop",
    price = 1400.00,
    ratings = 5.0,
    mode_of_payment = "After delivery",
    category = 3,
    shopId = 3,
    product_image = ""
)

cl8 = Product(
    name = "ladies cotton tanktop",
    price = 1200.00,
    ratings = 4.3,
    mode_of_payment = "Before delivery",
    category = 3,
    shopId = 4,
    product_image = ""
)

cl9 = Product(
    name = "High Waist Jeans",
    price = 1900.00,
    ratings = 5.0,
    mode_of_payment = "After delivery",
    category = 3,
    shopId = 3,
    product_image = ""
)

cl10 = Product(
    name = "High Waist Jeans",
    price = 1500.00,
    ratings = 3.8,
    mode_of_payment = "Before delivery",
    category = 3,
    shopId = 4,
    product_image = ""
)

cl11 = Product(
    name = "Womens air max 1",
    price = 21000.00,
    ratings = 5.5,
    mode_of_payment = "After delivery",
    category = 3,
    shopId = 3,
    product_image = ""
)

cl12 = Product(
    name = "Womens air max 1",
    price = 18000.00,
    ratings = 3.5,
    mode_of_payment = "Before delivery",
    category = 3,
    shopId = 4,
    product_image = ""
) 

cl13 = Product(
    name = "Marvel Spiderman Shirts",
    price = 4736.00,
    ratings = 4.5,
    mode_of_payment = "After delivery",
    category = 3,
    shopId = 3,
    product_image = ""
)

cl14 = Product(
    name = "Marvel Spiderman Shirts",
    price = 2812.00,
    ratings = 3.2,
    mode_of_payment = "Before delivery",
    category = 3,
    shopId = 4,
    product_image = ""
) 

cl15 = Product(
    name = "Denim black trouser",
    price = 1299.00,
    ratings = 4.0,
    mode_of_payment = "After delivery",
    category = 3,
    shopId = 3,
    product_image = ""
) 

cl16 = Product(
    name = "Denim black trouser",
    price = 1085.00,
    ratings = 3.3,
    mode_of_payment = "Before delivery",
    category = 3,
    shopId = 4,
    product_image = ""
) 

cl17 = Product(
    name = "Air Force 1 - Black",
    price = 3000.00,
    ratings = 5.0,
    mode_of_payment = "After delivery",
    category = 3,
    shopId = 3,
    product_image = ""
) 

cl18 = Product(
    name = "Air Force 1 - Black",
    price = 1800.00,
    ratings = 3.5,
    mode_of_payment = "Before delivery",
    category = 3,
    shopId = 4,
    product_image = ""
) 

sp1 = Product(
    name = "Huge family tent canvas",
    price = 27499.00,
    ratings = 5,
    mode_of_payment = "After delivery",
    category = 4,
    shopId = 3,
    product_image = ""
)

sp2 = Product(
    name = "Huge family tent canvas",
    price = 20000.00,
    ratings = 4,
    mode_of_payment = "Before delivery",
    category = 4,
    shopId = 4,
    product_image = ""
)

sp3 = Product(
    name = "Weightlifting Belt",
    price = 2981.00,
    ratings = 5,
    mode_of_payment = "After delivery",
    category = 4,
    shopId = 3,
    product_image = ""
)

sp4 = Product(
    name = "Weightlifting Belt",
    price = 2100.00,
    ratings = 3,
    mode_of_payment = "Before delivery",
    category = 4,
    shopId = 4,
    product_image = ""
)

sp5 = Product(
    name = "Molten Indoors & Outdoors Basketball",
    price = 2700.00,
    ratings = 5,
    mode_of_payment = "After delivery",
    category = 4,
    shopId = 3,
    product_image = ""
)

sp6 = Product(
    name = "Molten Indoors & Outdoors Basketball",
    price = 2000.00,
    ratings = 4,
    mode_of_payment = "Before delivery",
    category = 4,
    shopId = 4,
    product_image = ""
)

categories = [c3 , c4]
shops = [s3 , s4]
clothings = [cl1,cl2,cl3,cl4,cl5,cl6,cl7,cl8,cl9,cl10,cl11,cl12,cl13,cl14,cl15,cl16,cl17,cl18]
sports and outdoors = [sp1,sp2,sp3,sp4,sp5]

db.session.add_all(clothings)
db.session.add_all(sports and outdoors)
db.session.add_all(shops)
db.session.add_all(categories)

db.session.commit()

print("Seeding done")