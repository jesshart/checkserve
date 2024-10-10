import os


class Config:
    DEBUG = False
    TESTING = False
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
