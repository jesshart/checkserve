import sys
from datetime import datetime

from checkserve.app import app
from checkserve.extensions import db
from checkserve.models import Client, ClientDetails, ServeStatus, Visits

# Dummy Data Insertion Script


def insert_dummy_data():
    with app.app_context():
        # Clear the tables before inserting dummy data
        db.session.query(Visits).delete()
        db.session.query(ServeStatus).delete()
        db.session.query(ClientDetails).delete()
        db.session.query(Client).delete()

        # Inserting dummy clients
        clients = [
            Client(name_last="Doe", name_first="John"),
            Client(name_last="Smith", name_first="Jane"),
            Client(name_last="Johnson", name_first="Michael"),
        ]
        db.session.add_all(clients)
        db.session.commit()

        # Inserting dummy client details
        details = [
            ClientDetails(
                id_client=clients[0].id,
                date_added=datetime.utcnow(),
                date_updated=datetime.utcnow(),
                internal_note="Regular visitor",
                count_adults=2,
                count_children=1,
                count_seniors=0,
                needs_food_cat=False,
                needs_food_dog=True,
            ),
            ClientDetails(
                id_client=clients[1].id,
                date_added=datetime.utcnow(),
                date_updated=datetime.utcnow(),
                internal_note="First-time visitor",
                count_adults=1,
                count_children=2,
                count_seniors=1,
                needs_food_cat=True,
                needs_food_dog=False,
            ),
        ]
        db.session.add_all(details)
        db.session.commit()

        # Inserting dummy serve status
        serve_status = [
            ServeStatus(
                id_client=clients[0].id,
                time_check_in=datetime.utcnow(),
                time_estimated_serve=datetime.utcnow(),
                has_been_served=False,
            ),
            ServeStatus(
                id_client=clients[1].id,
                time_check_in=datetime.utcnow(),
                time_estimated_serve=datetime.utcnow(),
                has_been_served=True,
            ),
        ]
        db.session.add_all(serve_status)
        db.session.commit()

        # Inserting dummy visits
        visits = [
            Visits(id_client=clients[0].id, id_serve=serve_status[0].id, date=datetime.utcnow(), was_served=False),
            Visits(id_client=clients[1].id, id_serve=serve_status[1].id, date=datetime.utcnow(), was_served=True),
        ]
        db.session.add_all(visits)
        db.session.commit()

        print("Dummy data inserted successfully!")


def confirm_and_run():
    # Warning message
    print(
        "WARNING: This action will delete all data from the 'clients', 'client_details', 'serve_status', and 'visits' tables."
    )
    response = input("Do you want to proceed? (yes/no): ").strip().lower()

    if response == "yes":
        # Proceed with the dummy data insertion
        insert_dummy_data()
    else:
        print("Operation cancelled.")
        sys.exit(0)


if __name__ == "__main__":
    confirm_and_run()
