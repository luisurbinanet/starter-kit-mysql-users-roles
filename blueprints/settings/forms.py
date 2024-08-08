from flask_wtf import FlaskForm
from wtforms import StringField, FileField, ColorField, validators
from wtforms.validators import ValidationError
import re

def generate_settings_form(settings):
    class SettingsForm(FlaskForm):
        pass

    for setting in settings:
        if setting.key == 'logo':
            field = FileField(setting.label, validators=[validators.Optional()])
        elif 'color' in setting.key:
            field = ColorField(setting.label, validators=[validators.DataRequired()])
        else:
            field = StringField(setting.label, validators=[validators.DataRequired()])
        setattr(SettingsForm, setting.key, field)

    return SettingsForm

def validate_key(form, field):
    if re.search(r'\s', field.data):
        raise ValidationError('Key must not contain spaces.')
    field.data = re.sub(r'\s+', '-', field.data.strip().lower())
class AddSettingForm(FlaskForm):
    key = StringField('Key', validators=[validators.DataRequired()])
    label = StringField('Label', validators=[validators.DataRequired()])
    value = StringField('Value', validators=[validators.Optional()])