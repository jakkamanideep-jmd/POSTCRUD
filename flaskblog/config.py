
import os
class config():
    SECRET_KEY = '4631a00de3e108827d1ca43f00c468863ecc9f84'
    SQLALCHEMY_DATABASE_URI="sqlite:///site.db"
    MAIL_SERVER="smtp.googlemail.com"
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME=os.environ.get('Email_username')
    MAIL_PASSWORD=os.environ.get('Email_password')
    MAIL_DEFAULT_SENDER="jakkamanideep@gmail.com"