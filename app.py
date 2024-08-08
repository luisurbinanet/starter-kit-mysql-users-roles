import os
from flask import Flask, render_template, g
from config import Config
from extensions import db, migrate, csrf
from models import Settings
from seeder import seed_all
from sqlalchemy.exc import ProgrammingError

def load_settings(app):
    try:
        settings = {setting.key: setting.value for setting in Settings.query.all()}
        app.config['APP_SETTINGS'] = settings
        app.config['APP_NAME'] = settings.get('app_name', 'Default App Name')
        app.config['APP_LOGO'] = settings.get('logo', None)
    except ProgrammingError as e:
        app.logger.error(f"Error loading settings: {e}")
        with app.app_context():
            seed_all()  # Ejecutar seeders
        settings = {setting.key: setting.value for setting in Settings.query.all()}
        app.config['APP_SETTINGS'] = settings
        app.config['APP_NAME'] = settings.get('app_name', 'Default App Name')
        app.config['APP_LOGO'] = settings.get('logo', None)

def create_app():
    app = Flask(__name__)
    
    from dotenv import load_dotenv
    load_dotenv()
    secret_key = os.getenv('APP_SECRET_KEY')
    if not secret_key:
        raise RuntimeError("No APP_SECRET_KEY set for Flask application. Did you forget to set it in .env?")
    app.config['APP_SECRET_KEY'] = secret_key
    
    app.config.from_object(Config)

    app.logger.info(f"APP_SECRET_KEY: {app.config['APP_SECRET_KEY']}")

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    with app.app_context():
        load_settings(app)

    @app.before_request
    def before_request():
        if getattr(g, 'settings_updated', False):
            load_settings(app)
            g.settings_updated = False

    @app.context_processor
    def inject_settings():
        return dict(settings=app.config.get('APP_SETTINGS', {}))

    from blueprints.dashboard import dashboard_bp
    from blueprints.users import users_bp
    from blueprints.roles import roles_bp
    from blueprints.permissions import permissions_bp
    from blueprints.settings.views import settings_bp

    app.register_blueprint(dashboard_bp, url_prefix='/')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(roles_bp, url_prefix='/roles')
    app.register_blueprint(permissions_bp, url_prefix='/permissions')
    app.register_blueprint(settings_bp, url_prefix='/settings')

    from commands import seed
    app.cli.add_command(seed)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
