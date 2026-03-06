from flask import Flask
import os

from app.config import DevelopmentConfig, ProductionConfig
from .extensions import db, migrate


def create_app():

    app = Flask(__name__)

    if os.environ.get("FLASK_ENV") == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    migrate.init_app(app, db)

    from . import models
    _ = models

    from .wishlist import wishlist
    app.register_blueprint(wishlist)

    return app