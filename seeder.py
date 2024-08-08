from extensions import db
from models import User, Role, Permission, Settings
from faker import Faker
from werkzeug.security import generate_password_hash
import random

def seed_settings():
    settings = [
        {'key': 'app_name', 'label': 'Nombre de la Aplicación', 'value': 'My Application'},
        {'key': 'logo', 'label': 'Logo', 'value': ''},
        {'key': 'primary_color', 'label': 'Color Primario', 'value': '#0000FF'},
        {'key': 'secondary_color', 'label': 'Color Secundario', 'value': '#00FF00'},
        {'key': 'success_color', 'label': 'Color Operacion Exitosa', 'value': '#00FF00'},
        {'key': 'warning_color', 'label': 'Color para Advertencia', 'value': '#FFFF00'},
        {'key': 'danger_color', 'label': 'Color para Peligro', 'value': '#FF0000'},
        {'key': 'error_color', 'label': 'Color para Error', 'value': '#FF0000'},
    ]
    for setting in settings:
        new_setting = Settings(**setting)
        db.session.add(new_setting)
    db.session.commit()

def seed_roles():
    roles = [
        {'name': 'Super Administrador'},
        {'name': 'Administrador'},
        {'name': 'Gerente'},
        {'name': 'Operador'}
    ]
    
    for role in roles:
        new_role = Role(name=role['name'])
        db.session.add(new_role)
    db.session.commit()

def seed_permissions():
    default_actions = [
        {'name': 'Ver'},
        {'name': 'Crear'},
        {'name': 'Editar'},
        {'name': 'Eliminar'}
    ]

    modules = [
        {'module': 'Usuarios'},
        {'module': 'Roles'},
        {'module': 'Permisos'},
    ]

    combined_list = [f"{action['name']} {module['module']}" for module in modules for action in default_actions]
    
    for permission_name in combined_list:
        new_permission = Permission(name=permission_name)
        db.session.add(new_permission)
    db.session.commit()

def seed_users():
    fake = Faker()
    all_permissions = Permission.query.all()
    roles = Role.query.all()
    
    for _ in range(25):
        fake_name = fake.name()
        fake_email = fake.unique.email()
        fake_password = generate_password_hash('password', method='sha256')
        fake_role = random.choice(roles)
        new_user = User(
            name=fake_name,
            email=fake_email,
            password=fake_password,
            role_id=fake_role.id
        )
        random_permissions = random.sample(all_permissions, k=random.randint(1, len(all_permissions)))
        new_user.permissions.extend(random_permissions)
        db.session.add(new_user)
    
    db.session.commit()

def seed_all():
    seed_settings()
    seed_permissions()
    seed_roles()
    seed_users()

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_all()
