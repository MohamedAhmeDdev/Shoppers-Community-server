import os


from dotenv import load_dotenv
load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')
DATABASE_URI = os.getenv('DATABASE_URI')



MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.googlemail.com')
MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False') == 'True'
