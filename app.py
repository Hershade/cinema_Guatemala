from flask import Flask
from flask_migrate import Migrate

from database import db
from movie.api import show_movies

app = Flask(__name__)

# configuration our db
USER_DB = 'postgres'
PASS_DB = 'admin'
URL_DB = 'localhost'
NAME_DB = 'cinema_guatemala'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

# configuration our app
app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

# inicialization of the object db from sqlachemy
db.init_app(app)

# configuration flask-migrate
migrate = Migrate()

# we initialize the object to be able to execute the migrations to the database
migrate.init_app(app, db)


app.add_url_rule('/movies', 'movies', show_movies, methods=['POST', 'GET'])
