import os
from . import users_bp
from .forms import UserForm
# from faker import Faker
from flask import render_template, redirect, url_for, flash, request, current_app
from extensions import db
from models import User, Permission
from utils.helpers import pluralize
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

import random

model_label = 'Usuario'
plural_model_label = pluralize(model_label)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@users_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = User.query.paginate(page, per_page, error_out=False)
    users = pagination.items
    return render_template(
            'users/list.html', 
            users=users, 
            pagination=pagination, 
            endpoint='users.index', 
            modelLabel=model_label, 
            pluralModelLabel=plural_model_label
        )

@users_bp.route('/create', methods=['GET', 'POST'])
def create():
    form = UserForm()
    if form.validate_on_submit():
        file = form.avatar.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER_AVATAR'], filename)
            file.save(file_path)
            
        # hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(
                name=form.name.data,
                email=form.email.data,
                password=generate_password_hash(form.password.data, method='sha256'),
                avatar=filename,
                role_id=form.role_id.data
            )
        
        # Asignar permisos al usuario
        permissions = Permission.query.filter(Permission.id.in_(form.permissions.data)).all()
        new_user.permissions.extend(permissions)
            
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully.')
        
        return redirect(url_for('users.index'))
    
    return render_template('users/form.html', form=form, action='Crear', modelLabel=model_label, pluralModelLabel=plural_model_label )

@users_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    '''Edit User'''
    user = User.query.get_or_404(id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data

        if form.password.data:
            user.password = generate_password_hash(form.password.data, method='sha256')

        # Manejar la subida del avatar
        if form.avatar.data:
            file = form.avatar.data
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER_AVATAR'], filename)
                file.save(file_path)
                user.avatar = filename

        user.role_id = form.role_id.data
        user.permissions = Permission.query.filter(Permission.id.in_(form.permissions.data)).all()
        
        db.session.commit()
        flash('User updated successfully.')

        return redirect(url_for('users.index'))
    
    form.role_id.data = user.role_id
    form.permissions.data = [perm.id for perm in user.permissions]
    return render_template('users/form.html', form=form, action='Editar', modelLabel=model_label, pluralModelLabel=plural_model_label)

@users_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.')
    return redirect(url_for('users.index'))
