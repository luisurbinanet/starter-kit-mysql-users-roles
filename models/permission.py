from extensions import db

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    roles = db.relationship('Role', secondary='roles_permissions', back_populates='permissions')
    users = db.relationship('User', secondary='users_permissions', back_populates='permissions')
