import pytest
from checkserve.extensions import db
from checkserve.models import Client, ClientDetails, Visits, ServeStatus
from datetime import datetime, UTC
from checkserve.app import create_app

@pytest.fixture(scope='module')
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def session(app):
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()
        session = db.scoped_session(
            lambda: db.create_session(bind=connection)
        )
        db.session = session
        yield session
        transaction.rollback()
        connection.close()
        session.remove()

@pytest.fixture
def client(session):
    client = Client(name_last="Doe", name_first="John")
    session.add(client)
    session.commit()
    return client

@pytest.fixture
def serve_status(session, client):
    serve_status = ServeStatus(
        id_client=client.id,
        time_check_in=datetime.now(UTC),
        has_been_served=False
    )
    session.add(serve_status)
    session.commit()
    return serve_status

def test_create_client(session, client):
    assert client.name_last == "Doe"
    assert client.name_first == "John"

def test_client_has_details(session, client):
    details = ClientDetails(
        id_client=client.id,
        internal_note="Regular client",
        count_adults=2,
        count_children=0,
        count_seniors=0,
        needs_food_cat=False,
        needs_food_dog=True
    )
    session.add(details)
    session.commit()

    assert details.id_client == client.id
    assert details.count_adults == 2
    assert details.needs_food_dog is True

def test_client_has_visits(session, client, serve_status):
    visit = Visits(
        id_client=client.id,
        id_serve=serve_status.id,
        date=datetime.now(UTC),
        was_served=False
    )
    session.add(visit)
    session.commit()

    assert visit.id_client == client.id
    assert visit.was_served is False

def test_serve_status(session, client, serve_status):
    assert serve_status.id_client == client.id
    assert serve_status.has_been_served is False