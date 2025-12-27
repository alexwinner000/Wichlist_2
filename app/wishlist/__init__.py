from flask import Blueprint

wishlist = Blueprint(
    'wishlist',
    __name__,
    template_folder='../templates'
)

from . import routes
