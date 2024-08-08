from flask import Blueprint

permissions_bp = Blueprint('permissions', __name__)

from . import views
