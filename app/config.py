import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///wishlist.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:123@localhost:5432/wishlist_2"

class TestingConfig(Config):
    TESTING = True
    DEBUG = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
