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
