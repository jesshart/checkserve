import os

from flask import Flask, render_template

from .config import DevelopmentConfig, ProductionConfig, UATConfig

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

@app.route('/')
def hello_world():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
