from extensions import db

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, nullable=False)
    label = db.Column(db.String(64), nullable=False)
    value = db.Column(db.String(64), nullable=False, default="")
