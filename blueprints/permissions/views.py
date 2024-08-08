from faker import Faker
from flask import render_template, redirect, url_for, flash
from . import permissions_bp
from .forms import PermissionForm
from extensions import db
from models import Permission
from utils.helpers import pluralize

model_label = 'Permiso'
plural_model_label = pluralize(model_label)

@permissions_bp.route('/')
def index():
    # initialize_permissions()
    permissions = Permission.query.all()
    return render_template('permissions/list.html', permissions=permissions, modelLabel=model_label, pluralModelLabel=plural_model_label)

@permissions_bp.route('/create', methods=['GET', 'POST'])
def create():
    form = PermissionForm()
    if form.validate_on_submit():
        permission = Permission(
            name=form.name.data
        )
        db.session.add(permission)
        db.session.commit()
        flash('Permission created successfully.')
        return redirect(url_for('permissions.index'))
    return render_template('permissions/form.html', form=form, action='Crear', modelLabel=model_label, pluralModelLabel=plural_model_label)

@permissions_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    permission = Permission.query.get_or_404(id)
    form = PermissionForm(obj=permission)
    if form.validate_on_submit():
        form.populate_obj(permission)
        db.session.commit()
        flash('Permission updated successfully.')
        return redirect(url_for('permissions.index'))
    return render_template('permissions/form.html', form=form, action='Editar', modelLabel=model_label, pluralModelLabel=plural_model_label)

@permissions_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    permission = Permission.query.get_or_404(id)
    db.session.delete(permission)
    db.session.commit()
    flash('Permission deleted successfully.')
    return redirect(url_for('permissions.index'))
