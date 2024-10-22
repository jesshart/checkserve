from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Initialize the db and migrate objects
db = SQLAlchemy()
migrate = Migrate()
