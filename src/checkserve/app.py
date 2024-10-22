import os
from datetime import datetime

from flask import Flask, jsonify, render_template, request

from checkserve.config import DevelopmentConfig, ProductionConfig, TestingConfig, UATConfig
from checkserve.extensions import db, migrate
from checkserve.models import Client, ClientDetails


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

    @app.route('/add-client', methods=['POST'])
    def add_client():
        print("Add Client route called")  # Debugging step

        # Extract form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        count_adults = request.form.get('count_adults')
        count_children = request.form.get('count_children')
        count_seniors = request.form.get('count_seniors')
        internal_note = request.form.get('internal_note')
        needs_food_cat = bool(request.form.get('needs_food_cat'))
        needs_food_dog = bool(request.form.get('needs_food_dog'))

        print(f"Received data: {first_name}, {last_name}, {count_adults}, {count_children}, {count_seniors}")

        # Validate the required fields
        if not first_name or not last_name or not count_adults or not count_children or not count_seniors:
            return jsonify({"error": "Missing required fields"}), 400

        try:
            # Create a new Client
            new_client = Client(name_first=first_name, name_last=last_name)
            db.session.add(new_client)
            db.session.commit()  # Commit the client to get its ID

            # Create ClientDetails associated with the Client
            client_details = ClientDetails(
                id_client=new_client.id,
                count_adults=count_adults,
                count_children=count_children,
                count_seniors=count_seniors,
                internal_note=internal_note,
                needs_food_cat=needs_food_cat,
                needs_food_dog=needs_food_dog,
                date_added=datetime.utcnow(),
            )
            db.session.add(client_details)
            db.session.commit()  # Commit the client details

            print(f"Client {first_name} {last_name} added successfully.")
            return jsonify({"message": "Client added successfully!"}), 200

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            db.session.rollback()  # Rollback if any error occurs
            return jsonify({"error": "An error occurred while adding the client."}), 500


# This creates an application instance that can be used by other modules and tests
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
