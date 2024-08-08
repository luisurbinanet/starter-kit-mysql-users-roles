from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, g
from extensions import db
from models import Settings
from .forms import generate_settings_form, AddSettingForm
from sqlalchemy.exc import IntegrityError
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

settings_bp = Blueprint('settings', __name__)

model_label = 'Configuración'
plural_model_label = model_label

# Valores predeterminados
# default_settings = [
#     {'key': 'app_name', 'label': 'Nombre de la Aplicación', 'value': 'My Application'},
#     {'key': 'logo', 'label': 'Logo', 'value': ''},
#     {'key': 'primary_color', 'label': 'Color Primario', 'value': '#0000FF'},
#     {'key': 'secondary_color', 'label': 'Color Secundario', 'value': '#00FF00'},
#     {'key': 'success_color', 'label': 'Color Operacion Exitosa', 'value': '#00FF00'},
#     {'key': 'warning_color', 'label': 'Color para Advertencia', 'value': '#FFFF00'},
#     {'key': 'danger_color', 'label': 'Color para Peligro', 'value': '#FF0000'},
#     {'key': 'error_color', 'label': 'Color para Error', 'value': '#FF0000'},
# ]

# def initialize_default_settings():
#     if not Settings.query.first():
#         for setting in default_settings:
#             new_setting = Settings(key=setting['key'], value=setting['value'], label=setting['label'])
#             db.session.add(new_setting)
#         db.session.commit()

@settings_bp.route('/', methods=['GET', 'POST'])
def config():
    # initialize_default_settings()
    settings = Settings.query.all()
    SettingsForm = generate_settings_form(settings)
    form = SettingsForm()

    # Prepopulate the form with existing settings values
    if request.method == 'GET':
        for setting in settings:
            form_field = getattr(form, setting.key)
            form_field.data = setting.value
    
    if form.validate_on_submit():
        try:
            with db.session.no_autoflush:
                for setting in settings:
                    form_field = getattr(form, setting.key)
                    if form_field.data is not None:
                        if setting.key == 'logo':
                            if 'delete_logo' in request.form and request.form['delete_logo'] == 'on':
                                setting.value = ""
                            elif isinstance(form_field.data, FileStorage):
                                file = form_field.data
                                if file.filename != '':
                                    filename = secure_filename(file.filename)
                                    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'logo', filename)
                                    file.save(file_path)
                                    setting.value = filename
                        else:
                            setting.value = form_field.data
                    else:
                        setting.value = ""
            db.session.commit()
            g.settings_updated = True
            flash('Settings updated successfully.')
        except IntegrityError:
            db.session.rollback()
            flash('An error occurred while updating settings.', 'error')
        return redirect(url_for('settings.config'))

    return render_template('settings/form.html', form=form, modelLabel=model_label, pluralModelLabel=plural_model_label)

@settings_bp.route('/add', methods=['GET', 'POST'])
def add_setting():
    form = AddSettingForm()
    if form.validate_on_submit():
        key = form.key.data
        value = form.value.data
        label = form.label.data
        
        if key and label:
            setting = Settings(key=key, value=value, label=label)
            db.session.add(setting)
            db.session.commit()
            g.settings_updated = True
            flash('Setting added successfully.')
            return redirect(url_for('settings.config'))
    
    return render_template('settings/add_setting.html', form=form, action='Agregar', modelLabel=model_label, pluralModelLabel=plural_model_label)
