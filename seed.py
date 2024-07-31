import cloudinary
import cloudinary.uploader
import cloudinary
import cloudinary.uploader
from model import db, Product, Shop, Category
from app import app

# Configure Cloudinary
cloudinary.config(
    cloud_name='dows56r9v',
    api_key='352337169378987',
    api_secret='zRPXOHtgbFiTbRoq3q7NGG3hLeg'
)

def upload_image_to_cloudinary(image_path, folder):
    result = cloudinary.uploader.upload(
        image_path,
        folder=folder
    )
    return result['url']

with app.app_context():
    print("Deleting data.....")
    Product.query.delete()
    Shop.query.delete()
    Category.query.delete()
    db.session.commit()

    print("Creating data .....")

    s1 = Shop(name="Amazon")
    s2 = Shop(name="Alibaba")

    # Upload images for categories
    c1_image_url = upload_image_to_cloudinary('https://i.ebayimg.com/thumbs/images/g/A4AAAOSwiYNmOozq/s-l640.jpg', folder='categories')
    c2_image_url = upload_image_to_cloudinary('https://www.gearpatrol.com/wp-content/uploads/sites/2/2023/07/best-furniture-refresh-lead-1659534331-jpg.webp', folder='categories')

    c1 = Category(name="Electronics", category_image=c1_image_url)
    c2 = Category(name="Furniture", category_image=c2_image_url)

    # Upload images for products
    e1_image_url = upload_image_to_cloudinary('https://m-cdn.phonearena.com/images/articles/406312-image/Samsung-Galaxy-A05s.jpg',folder='products')
    e2_image_url = upload_image_to_cloudinary('https://m.media-amazon.com/images/S/aplus-media-library-service-media/3967678b-5f5b-4a23-8d96-bab21662328c.__CR0,0,970,600_PT0_SX970_V1___.jpg', folder='products')
    f1_image_url = upload_image_to_cloudinary('https://cdn.fairdealfurniture.co.ke/wp-content/uploads/2024/05/10105626/1-4-jpg.webp',folder='products')
    f2_image_url = upload_image_to_cloudinary('https://furniturepalacekenya.com/wp-content/uploads/2023/03/CAIN-BED-3-1-800x533.jpg',folder='products')

    e1 = Product(
        name="Samsung A05",
        price=30000.00,
        ratings=4.7,
        mode_of_payment="After delivery",
        categoryId=1,
        shopId=1,
        product_image=e1_image_url
    )
    e2 = Product(
        name="Samsung A05",
        price=33000.00,
        ratings=4.7,
        mode_of_payment="After delivery",
        categoryId=1,
        shopId=2,
        product_image=e1_image_url
    )
    e3 = Product(
        name="Hp EliteBook 840 G3",
        price=29999.00,
        ratings=4,
        mode_of_payment="After Delivery",
        categoryId=1,
        shopId=1,
        product_image=e2_image_url
    )
    e4 = Product(
        name="Hp EliteBook 840 G3",
        price=29000.00,
        ratings=4,
        mode_of_payment="After Delivery",
        categoryId=1,
        shopId=2,
        product_image=e2_image_url
    )
    f1 = Product(
        name="5-Seater Corporate Sofa",
        price=69999.00,
        ratings=3,
        mode_of_payment="Upfront",
        categoryId=2,
        shopId=1,
        product_image=f1_image_url
    )
    f2 = Product(
        name="5-Seater Corporate Sofa",
        price=70000.00,
        ratings=3,
        mode_of_payment="Upfront",
        categoryId=2,
        shopId=2,
        product_image=f1_image_url
    )
    f3 = Product(
        name="HarMony King Bed Only",
        price=75000.00,
        ratings=5,
        categoryId=2,
        mode_of_payment="After Delivery",
        shopId=1,
        product_image=f2_image_url
    )
    f4 = Product(
        name="HarMony King Bed Only",
        price=75000.00,
        ratings=5,
        categoryId=2,
        shopId=2,
        mode_of_payment="Upfront",
        product_image=f2_image_url
    )

    categories = [c1, c2]
    shops = [s1, s2]
    electronics = [e1, e2, e3, e4]
    furnitures = [f1, f2, f3, f4]

    db.session.add_all(electronics)
    db.session.add_all(furnitures)
    db.session.add_all(shops)
    db.session.add_all(categories)

    db.session.commit()

    print("Seeding done")
