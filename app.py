import datetime
from functools import wraps

import jwt
from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from werkzeug.security import check_password_hash

from database import db
from feature.api import show_features
from models.models import User
from movie.api import show_movies
from user.api import register_user

app = Flask(__name__)

# configuration our db
USER_DB = 'postgres'
PASS_DB = 'admin'
URL_DB = 'localhost'
NAME_DB = 'cinema_guatemala'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

# configuration our app
app.config['SECRET_KEY'] = 'b1a143838a58d5bcfac7744982538af67171d9c0efa323ee666fe1dd16d64159'
app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

# inicialization of the object db from sqlachemy
db.init_app(app)

# configuration flask-migrate
migrate = Migrate()

# we initialize the object to be able to execute the migrations to the database
migrate.init_app(app, db)


# Method to require a token to access
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(user_token=data['user_token']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorator

# Create a token when the user is log in
def login_user():
    auth = request.authorization
    app.logger.debug(f'this is {auth}')
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'Authentication': 'login required'})

    user = User.query.filter_by(email=auth.username).first()
    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {'user_token': user.user_token, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)},
            app.config['SECRET_KEY'], "HS256")

        return jsonify({'token': token})
    return make_response('could not verify', 401, {'Authentication': 'login required'})


# Routes of my endpoints
app.add_url_rule('/movies', 'movies', show_movies, methods=['POST', 'GET'])
app.add_url_rule('/features', 'features', show_features, methods=['GET'])
app.add_url_rule('/registration', 'registration', register_user, methods=['POST', 'GET'])
app.add_url_rule('/login', 'logins', login_user, methods=['POST'])
