from model import db, Product, Shop, Category
from app import app
import random
import cloudinary
import cloudinary.uploader


# Configure Cloudinary
cloudinary.config(
    cloud_name='dows56r9v',
    api_key='352337169378987',
    api_secret='zRPXOHtgbFiTbRoq3q7NGG3hLeg'
)

def upload_image_to_cloudinary(image_path):
    response = cloudinary.uploader.upload(image_path, folder="shopHorizon")
    return response['secure_url']

def seed_data():
    with app.app_context():
        print("Clearing existing data...")
        Product.query.delete()
        Shop.query.delete()
        Category.query.delete()
        db.session.commit()
        print("Data cleared.")

        print("Adding categories...")
        electronics = Category(name="Electronics", category_image=upload_image_to_cloudinary("https://ecelectronics.com/wp-content/uploads/2020/04/Modern-Electronics-EC-.jpg"))
        clothing = Category(name="Clothing", category_image=upload_image_to_cloudinary("https://t3.ftcdn.net/jpg/02/10/85/26/360_F_210852662_KWN4O1tjxIQt8axc2r82afdSwRSLVy7g.jpg"))
        sports_and_outdoors = Category(name="Sports and Outdoors", category_image=upload_image_to_cloudinary("https://img.freepik.com/free-photo/young-healthy-man-athlete-doing-exercise-with-ropes-gym-single-male-model-practicing-hard-training-his-upper-body-concept-healthy-lifestyle-sport-fitness-bodybuilding-wellbeing_155003-27879.jpg"))
        furniture = Category(name="Furniture", category_image=upload_image_to_cloudinary("https://st4.depositphotos.com/1023934/37752/i/450/depositphotos_377527168-stock-photo-interior-design-modern-living-room.jpg"))
        others = Category(name="Others", category_image=upload_image_to_cloudinary("https://www.shutterstock.com/image-photo/male-female-accessories-on-white-260nw-1888761748.jpg"))

        db.session.add_all([electronics, clothing, sports_and_outdoors, furniture, others])
        db.session.commit()
        print("Categories added.")

        print("Adding shops...")
        shop1 = Shop(name="Amazon")
        shop2 = Shop(name="Alibaba")
        shop3 = Shop(name="Shopify")

        db.session.add_all([shop1, shop2, shop3])
        db.session.commit()
        print("Shops added.")

        print("Adding products...")
        
       
        product_templates = [
            {"name": "Samsung A05", "category": electronics, "product_image": "https://m-cdn.phonearena.com/images/articles/406312-image/Samsung-Galaxy-A05s.jpg"},
            {"name": "Hp EliteBook 840 G3", "category": electronics, "product_image": "https://m.media-amazon.com/images/S/aplus-media-library-service-media/3967678b-5f5b-4a23-8d96-bab21662328c.__CR0,0,970,600_PT0_SX970_V1___.jpg"},
            {"name": "Cannon E0S R7", "category": electronics, "product_image": "https://t3.ftcdn.net/jpg/00/79/36/04/360_F_79360425_13tH0FGR7nYTNlXWKOWtLmzk7BAikO1b.jpg"},
            {"name": "Quartz", "category": electronics, "product_image": "https://img.kwcdn.com/product/fancy/c8614497-5aec-4ec3-8562-ec12f5f61f91.jpg"},
            {"name": "Men's T-shirt", "category": clothing, "product_image": "https://files.sophie.co.ke/2024/02/1880922072_179_7365-595x595.webp"},
            {"name": "Women's Dress", "category": clothing, "product_image": "https://st.depositphotos.com/2515135/2791/v/950/depositphotos_27912009-stock-illustration-woman-beautiful-dresses-on-hanger.jpg"},
             {"name": "Kids Cloths", "category": clothing, "product_image": "https://www.sheknows.com/wp-content/uploads/2023/09/Screen-Shot-2023-09-21-at-2.42.38-PM.png?w=1440"},
            {"name": "Yoga Mat", "category": sports_and_outdoors, "product_image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT6Ebv5b152nJHbnWRdnadrzr-PkwZ3m8s9Tg&s"},
            {"name": "Ball", "category": sports_and_outdoors, "product_image": "https://cdn.britannica.com/51/190751-131-B431C216/soccer-ball-goal.jpg"},
            {"name": "Weight lfting", "category": sports_and_outdoors, "product_image": "https://5.imimg.com/data5/SELLER/Default/2024/3/405978903/CC/UB/QY/150323968/weight-lifting-equipment-500x500.jpg"},
            {"name": "Office Chair", "category": furniture, "product_image": "https://dignity.co.ke/wp-content/uploads/2024/05/HIGH-BACK-OFFICE-CHAIR-BLACK-GREEN-DG-3004-1-657x544.webp"},
            {"name": "HarMony King Bed", "category": furniture, "product_image": "https://furniturepalacekenya.com/wp-content/uploads/2023/05/CF-9148-P-DOREL.jpg-800x533.jpg"},
            {"name": "5-Seater Corporate Sofa", "category": furniture, "product_image": "https://nicmaahomeandofficefurniturelimited.co.ke/wp-content/uploads/2023/10/Modern-Design-Commercial-Furniture-Office-Sofa-Set-Sofa-Chair-Office-Seating.webp"},
            {"name": "table", "category": furniture, "product_image": "https://i.pinimg.com/736x/1e/9f/26/1e9f260095ba08b16b1d2783b22b4cba.jpg"},
            {"name": "Jewelry", "category": others, "product_image": "https://nypost.com/wp-content/uploads/sites/2/2023/11/Untitled-design-42.jpg"},
            {"name": "Phone Covers", "category": others, "product_image": "https://t4.ftcdn.net/jpg/03/68/09/49/360_F_368094934_RLbGLbrs68hPicpZd1vg7rn9njFgZRCr.jpg"},
            {"name": "Phone Charger", "category": others, "product_image": "https://imageio.forbes.com/specials-images/imageserve/1048621702/USB-cable-charger-for-a-smartphone/960x0.jpg?format=jpg&width=960"},
            {"name": "Speaker", "category": others, "product_image": "https://images.news18.com/ibnlive/uploads/2014/09/speakers-020914.jpg?impolicy=website&width=640&height=480"},
        ]

        
        for template in product_templates:
            for shop in [shop1, shop2, shop3]:
                product = Product(
                    name=template["name"],
                    price=round(random.uniform(10.0, 1000.0), 2),
                    ratings=round(random.uniform(3.0, 5.0), 1),
                    mode_of_payment=random.choice(["Upfront", "After Delivery"]),
                    categoryId=template["category"].id,
                    shopId=shop.id,
                    product_image=upload_image_to_cloudinary(template["product_image"])
                )
                db.session.add(product)

        db.session.commit()
        print("Products added.")

if __name__ == "__main__":
    seed_data()
