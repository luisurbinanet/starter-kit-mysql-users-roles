# blueprints/dashboard/views.py

from flask import render_template
from . import dashboard_bp

module = 'Escritorio'

@dashboard_bp.route('/')
def index():
    return render_template('dashboard/form.html', title=module, breadcrumb_title=module)
