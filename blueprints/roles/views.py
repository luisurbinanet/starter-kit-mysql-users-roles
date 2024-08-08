from flask import render_template, redirect, url_for, flash
from . import roles_bp
from .forms import RoleForm
from extensions import db
from models import Role
from utils.helpers import pluralize

model_label = 'Rol'
plural_model_label = pluralize(model_label)

# roles = [
#     {'name': 'Super Administrador'},
#     {'name': 'Administrador'},
#     {'name': 'Gerente'},
#     {'name': 'Operador'}
# ]

# def initialize_roles():
#     if not Role.query.first():
#         for role in roles:
#             new_role = Role(name=role['name'])
#             db.session.add(new_role)
#         db.session.commit()

@roles_bp.route('/')
def index():
    # initialize_roles()
    roles = Role.query.all()
    return render_template('roles/list.html', roles=roles, modelLabel=model_label, pluralModelLabel=plural_model_label)

@roles_bp.route('/create', methods=['GET', 'POST'])
def create():
    form = RoleForm()
    if form.validate_on_submit():
        role = Role(
            name=form.name.data
        )
        db.session.add(role)
        db.session.commit()
        flash('Role created successfully.')
        return redirect(url_for('roles.index'))
    return render_template('roles/form.html', form=form, action='Crear', modelLabel=model_label, pluralModelLabel=plural_model_label)

@roles_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        form.populate_obj(role)
        db.session.commit()
        flash('Role updated successfully.')
        return redirect(url_for('roles.index'))
    return render_template('roles/form.html', form=form, action='Editar', modelLabel=model_label, pluralModelLabel=plural_model_label)

@roles_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('Role deleted successfully.')
    return redirect(url_for('roles.index'))
