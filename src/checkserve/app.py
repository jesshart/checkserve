import os
from flask import Flask, render_template
from checkserve.config import DevelopmentConfig, ProductionConfig, UATConfig, TestingConfig
from checkserve.extensions import db, migrate
from checkserve.models import *  # Import models after db is initialized

def create_app(config_name=None):
    app = Flask(__name__)

    # Load configuration based on the config_name or FLASK_ENV environment variable
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    if config_name == 'development':
        app.config.from_object(DevelopmentConfig)
    elif config_name == 'uat':
        app.config.from_object(UATConfig)
    elif config_name == 'production':
        app.config.from_object(ProductionConfig)
    elif config_name == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # Initialize the db and migrations with the app
    db.init_app(app)
    migrate.init_app(app, db)

    @app.route('/')
    def hello_world():
        return render_template('index.html')

    return app

# This creates an application instance that can be used by other modules
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)