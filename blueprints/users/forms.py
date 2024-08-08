from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Optional
from models import Role, Permission
from email_validator import validate_email, EmailNotValidError

class UserForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Optional()])
    avatar = FileField('Avatar')
    role_id = SelectField('Rol', coerce=int, validators=[DataRequired()])
    permissions = SelectMultipleField('Permisos', coerce=int, validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.role_id.choices = [(role.id, role.name) for role in Role.query.all()]
        self.permissions.choices = [(perm.id, perm.name) for perm in Permission.query.all()]
