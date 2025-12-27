from datetime import datetime
from .extensions import db

class Wishlist(db.Model):
    __tablename__ = 'wishlists'  # Явное имя таблицы

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    slug = db.Column(db.String(32), unique=True, nullable=False, index=True)

    gifts = db.relationship('Gift', backref='wishlist', cascade='all, delete-orphan')


class Gift(db.Model):
    __tablename__ = 'gifts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(255))
    is_reserved = db.Column(db.Boolean, default=False)
    reserved_name = db.Column(db.String(100))
    wishlist_id = db.Column(db.Integer, db.ForeignKey('wishlists.id'), nullable=False)  # FK на Wishlist