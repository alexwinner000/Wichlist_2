from flask import Flask
from config import DevelopmentConfig
from .extensions import db, migrate 


def create_app(config_class=DevelopmentConfig):
    app = Flask (__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app,db)

    from . import models
    _ = models  # чтобы Pylance не ругался на "unused import"

    from .wishlist import wishlist
    app.register_blueprint(wishlist)

    return app

