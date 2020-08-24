import datetime
import os

DEV_MODE = True

if DEV_MODE:
    ENV_FILE = '.env.dev'
else:
    ENV_FILE = '.env.prod'

from dotenv import load_dotenv
load_dotenv(dotenv_path=ENV_FILE)

class BaseConfig(object):
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY')
    FLASK_SECRET = os.getenv('SECRET_KEY')
    JSON_ADD_STATUS = False
    CORS_HEADERS = '*' # TODO: [Security] - Tweak headers "specifically"
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_IMG_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # Max upload size if 16 MB

    # Email token settings
    CONFIRM_EMAIL_SALT = os.getenv('CONFIRM_EMAIL_SALT')
    RESET_PASSWORD_SALT = os.getenv('RESET_PASSWORD_SALT')
    CONFIRM_EMAIL_EXPIRY = datetime.timedelta(days=3)
    RESET_PASSWORD_EXPIRY = datetime.timedelta(minutes=30)

    # JWT settings
    JWT_SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=15)

    # Mail SMTP server settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = f'"sproul.club" <{os.getenv("MAIL_USERNAME")}>'

    # AWS S3 settings
    S3_REGION     = os.getenv('S3_REGION')
    S3_BUCKET     = os.getenv('S3_BUCKET')
    S3_ACCESS_KEY = os.getenv('S3_KEY')
    S3_SECRET_KEY = os.getenv('S3_SECRET')

# Development config object for Flask app
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    ENV = 'development'
    BASE_URL = 'https://sc-backend-dev.herokuapp.com'

# Production config object for Flask app
class ProductionConfig(BaseConfig):
    DEBUG = False
    ENV = 'production'
    BASE_URL = 'https://sc-backend-prod.herokuapp.com'

if DEV_MODE:
    CurrentConfig = DevelopmentConfig
else:
    CurrentConfig = ProductionConfig