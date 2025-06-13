from dotenv import load_dotenv
import os
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # --- Database & Migrations ---
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- CSRF & Sessions ---
    SECRET_KEY = os.getenv('SECRET_KEY', 'dummy-key')
    WTF_CSRF_TIME_LIMIT = None
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # --- Bcrypt Hashing ---
    BCRYPT_LOG_ROUNDS = 12
