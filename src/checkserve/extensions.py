from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize the db and migrate objects
db = SQLAlchemy()
migrate = Migrate()