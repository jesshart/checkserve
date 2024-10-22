import os

from flask import Flask, render_template, request

from checkserve.config import DevelopmentConfig, ProductionConfig, TestingConfig, UATConfig
from checkserve.extensions import db, migrate
from checkserve.models import Client


def create_app(config_name=None):
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__)

    # Load configuration based on the config_name or FLASK_ENV environment variable
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    if config_name == "development":
        app.config.from_object(DevelopmentConfig)
    elif config_name == "uat":
        app.config.from_object(UATConfig)
    elif config_name == "production":
        app.config.from_object(ProductionConfig)
    elif config_name == "testing":
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # Initialize the db and migrations with the app
    db.init_app(app)
    migrate.init_app(app, db)

    # Register routes
    register_routes(app)

    return app


def register_routes(app):
    """Define the routes for the app."""

    @app.route("/", methods=["GET", "POST"])
    def hello_world():
        if request.method == "POST":
            # Capture the user input and print it to the terminal
            user_input = request.form.get("userInput")
            print(f"User input received: {user_input}")  # For now, just print it in the console

        return render_template("index.html")

    @app.route("/search", methods=["GET"])
    def search():
        query = request.args.get("query")

        if query:
            # Search for matching clients in the database
            results = Client.query.filter(
                (Client.name_first.ilike(f"%{query}%")) | (Client.name_last.ilike(f"%{query}%"))
            ).all()

            # Convert the results to a list of names
            results_list = [{"id": client.id, "name": f"{client.name_first} {client.name_last}"} for client in results]

            # Return JSON response
            return {"results": results_list}
        return {"results": []}


# This creates an application instance that can be used by other modules and tests
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
