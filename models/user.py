import datetime
import mongoengine as mongo
import mongoengine_goodjson as gj

from app_config import FlaskConfig

def create_expire_index(field, expire_after_key):
    datetime_obj = FlaskConfig.__dict__[expire_after_key]
    return { 'fields': [field], 'expireAfterSeconds': int(datetime_obj.total_seconds()) }

class User(gj.Document):
    email    = mongo.EmailField(primary_key=True)
    password = mongo.StringField(required=True)

    registered_on = mongo.DateTimeField(default=datetime.datetime.utcnow)
    confirmed     = mongo.BooleanField(default=False)
    confirmed_on  = mongo.DateTimeField(default=None)

class PreVerifiedEmail(gj.Document):
    email = mongo.EmailField(unique=True)

class AccessJTI(gj.Document):
    owner = mongo.ReferenceField(User, required=True)
    token_id = mongo.StringField(required=True)
    expired = mongo.BooleanField(default=False)
    expiry_time = mongo.DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'collection': 'access_jti',
        'indexes': [create_expire_index('expiry_time', 'JWT_ACCESS_TOKEN_EXPIRES')]
    }

class RefreshJTI(gj.Document):
    owner = mongo.ReferenceField(User, required=True)
    token_id = mongo.StringField(required=True)
    expired = mongo.BooleanField(default=False)
    expiry_time = mongo.DateTimeField(default=datetime.datetime.now)

    meta = {
        'collection': 'refresh_jti',
        'indexes': [create_expire_index('expiry_time', 'JWT_REFRESH_TOKEN_EXPIRES')]
    }

class ConfirmEmailToken(gj.Document):
    token = mongo.StringField(required=True)
    used = mongo.BooleanField(default=False)
    expiry_time = mongo.DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'indexes': [create_expire_index('expiry_time', 'CONFIRM_EMAIL_EXPIRY')]
    }

class ResetPasswordToken(gj.Document):
    token = mongo.StringField(required=True)
    used = mongo.BooleanField(default=False)
    expiry_time = mongo.DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'indexes': [create_expire_index('expiry_time', 'RESET_PASSWORD_EXPIRY')]
    }
