import os
from flask import Flask, render_template
from checkserve.config import DevelopmentConfig, ProductionConfig, UATConfig
from checkserve.extensions import db, migrate
from checkserve.models import User, Visit  # Import models after db is initialized

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

# Initialize the db and migrations with the app
db.init_app(app)
migrate.init_app(app, db)

@app.route('/')
def hello_world():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)