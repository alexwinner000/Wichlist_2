import os

class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL'
    ) or "postgresql://postgres:123@localhost:5432/wishlist_2"

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False