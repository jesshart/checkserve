import os
from pathlib import Path

# Base directory for your app
basedir = Path(__file__).resolve().parent

class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{basedir / "app.db"}'
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'

class UATConfig(Config):
    DEBUG = True
    ENV = 'uat'

class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
