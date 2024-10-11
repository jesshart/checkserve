import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from checkserve.config import DevelopmentConfig, ProductionConfig, UATConfig

app = Flask(__name__)

# Load configuration based on the FLASK_ENV environment variable
env = os.getenv('FLASK_ENV', 'development')

if env == 'development':
    app.config.from_object(DevelopmentConfig)
elif env == 'uat':
    app.config.from_object(UATConfig)
elif env == 'production':
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

# Initialize the SQLAlchemy object
db = SQLAlchemy(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Apply migrations at startup
with app.app_context():
    upgrade()


@app.route('/')
def hello_world():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
