from flask import Flask
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from POSTCRUD.config import config

db= SQLAlchemy()
bcrypt=Bcrypt()
login_manager=LoginManager()
login_manager.login_view="users.login"
login_manager.login_message_category="_info"

mail=Mail()

def create_app(config_class=config):
    app=Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from POSTCRUD.users.routes import users
    from POSTCRUD.posts.routes import posts
    from POSTCRUD.main.routes import main
    from POSTCRUD.errors.handler import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app



