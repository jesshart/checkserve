from checkserve.extensions import db
from datetime import datetime

class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    name_last = db.Column(db.String(80), nullable=False)
    name_first = db.Column(db.String(80), nullable=False)
    
    # Relationship to ClientDetails and Visits
    details = db.relationship('ClientDetails', backref='client', lazy=True, uselist=False)
    visits = db.relationship('Visits', backref='client', lazy=True)

    def __repr__(self):
        return f'<Client {self.name_last}, {self.name_first}>'


class ClientDetails(db.Model):
    __tablename__ = 'client_details'
    id = db.Column(db.Integer, primary_key=True)
    id_client = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, onupdate=datetime.utcnow)
    internal_note = db.Column(db.String(255), nullable=True)
    count_adults = db.Column(db.Integer, nullable=False)
    count_children = db.Column(db.Integer, nullable=False)
    count_seniors = db.Column(db.Integer, nullable=False)
    needs_food_cat = db.Column(db.Boolean, nullable=False, default=False)
    needs_food_dog = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<ClientDetails for Client {self.id_client}>'


class Visits(db.Model):
    __tablename__ = 'visits'
    id = db.Column(db.Integer, primary_key=True)
    id_client = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    id_serve = db.Column(db.Integer, db.ForeignKey('serve_status.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    was_served = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Visit by Client {self.id_client} on {self.date}>'


class ServeStatus(db.Model):
    __tablename__ = 'serve_status'
    id = db.Column(db.Integer, primary_key=True)
    id_client = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    time_check_in = db.Column(db.DateTime, default=datetime.utcnow)
    time_estimated_serve = db.Column(db.DateTime, nullable=True)
    has_been_served = db.Column(db.Boolean, nullable=False, default=False)
    
    # Relationship with Visits
    visits = db.relationship('Visits', backref='serve_status', lazy=True)

    def __repr__(self):
        return f'<ServeStatus for Client {self.id_client} at {self.time_check_in}>'