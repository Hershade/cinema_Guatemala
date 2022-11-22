import datetime

from database import db


# we define the class of model
class Movie(db.Model):
    # We need to specifY the Primary Key
    # __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    url_image = db.Column(db.String(250))
    classification = db.Column(db.String(250))
    created_at = db.Column(db.types.DateTime(timezone=True), default=datetime.datetime.utcnow)
    features = db.relationship('Feature', backref='movie')

    #     Auto string method
    def __init__(self, title, url_image, classification):
        self.title = title
        self.url_image = url_image
        self.classification = classification

    def __str__(self):
        return (
            f'id:{self.id}, '
            f'title: {self.title}, '
            f'url_image: {self.url_image}, '
            f'classification: {self.classification}, '
            f'created_at: {self.created_at}, '
        )


class Feature(db.Model):
    # __tablename__ = 'features'
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.types.DateTime(timezone=True))
    created_at = db.Column(db.types.DateTime(timezone=True), default=datetime.datetime.utcnow)
    movies_id = db.Column(db.Integer(), db.ForeignKey(Movie.id))
    rooms = db.relationship('Room', backref='seat')

    def __init__(self, date_time, movies_id):
        self.date_time = date_time
        self.movies_id = movies_id

    #     Auto string method
    def __str__(self):
        return (
            f'id: {self.id}, '
            f'created_at: {self.created_at}, '
            f'movies_id : {self.movies_id}'
        )


class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    is_active = db.Column(db.Boolean(), default=True)
    rooms = db.relationship('Room', backref='seat_room')
    created_at = db.Column(db.types.DateTime(timezone=True), default=datetime.datetime.utcnow)


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    features_id = db.Column(db.Integer(), db.ForeignKey(Feature.id))
    seats_id = db.Column(db.Integer(), db.ForeignKey(Seat.id))
    is_empty = db.Column(db.Boolean(), default=True)
    buy_tickets_details = db.relationship('BuyTicketDetail', backref='room')
    created_at = db.Column(db.types.DateTime(timezone=True), default=datetime.datetime.utcnow)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250))
    password = db.Column(db.String(250), nullable=False)
    user_token = db.Column(db.String(250))
    email = db.Column(db.String(250), unique=True, nullable=False)
    phone = db.Column(db.String(250))
    buy_tickets = db.relationship('BuyTicket', backref='user')
    created_at = db.Column(db.types.DateTime(timezone=True), default=datetime.datetime.utcnow)

    def __init__(self, name, last_name, password, email, phone, user_token ):
        self.name = name
        self.last_name = last_name
        self.password = password
        self.email = email
        self.phone = phone
        self.user_token = user_token


class BuyTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    created_at = db.Column(db.types.DateTime(timezone=True), default=datetime.datetime.utcnow)
    buy_tickets_details = db.relationship('BuyTicketDetail', backref='buy_ticket')
    canceled = db.Column(db.Boolean(), default=False)


class BuyTicketDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer(), db.ForeignKey(Room.id))
    buy_tickets_id = db.Column(db.Integer(), db.ForeignKey(BuyTicket.id))

    def __init__(self, room_id, buy_tickets_id):
        self.room_id = room_id
        self.buy_tickets_id = buy_tickets_id

