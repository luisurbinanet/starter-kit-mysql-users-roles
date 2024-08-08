import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('APP_SECRET_KEY', 'you-will-never-guess')
    DB_USERNAME = os.getenv('DB_USERNAME', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', 3306)
    DB_NAME = os.getenv('DB_NAME', 'urp_db')

    SQLALCHEMY_DATABASE_URI = f"mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    UPLOAD_FOLDER_LOGO = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/images/logo')
    UPLOAD_FOLDER_AVATAR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/images/avatar')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

