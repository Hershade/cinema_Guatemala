import datetime
from functools import wraps

import jwt
from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from werkzeug.security import check_password_hash

from database import db
from feature.api import show_features
from models.models import User, BuyTicket, Room, BuyTicketDetail
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
            app.logger.debug(data)
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
            {'user_token': user.user_token, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=5)},
            app.config['SECRET_KEY'], "HS256")

        return jsonify({'token': token})
    return make_response('could not verify', 401, {'Authentication': 'login required'})


@token_required
def buy_tickets(current_user):
    if request.method == 'POST':

        if request.is_json:
            data = request.get_json()
            for i in data:
                room = Room.query.get(i["room_id"])
                # validate_seat(i["room_id"])
                if room is None:
                    return make_response('This seat does not exist', 400, {'room_id': 'object does not exist'})
                elif room is not None:
                    if not room.is_empty:
                        return make_response(f'This seat {room.id} is not available', 400)

            new_purchase = BuyTicket(user_id=current_user.id)
            db.session.add(new_purchase)
            db.session.commit()
            for i in data:
                new_detail = BuyTicketDetail(room_id=i["room_id"], buy_tickets_id=new_purchase.id)
                db.session.add(new_detail)
                db.session.commit()
                # change the status of the seat to True
                room = Room.query.get(i["room_id"])
                room.is_empty = False
                db.session.commit()
            return make_response("Your tickets was bought successfully")
        else:
            return {"error": "The request payload is not in Json format"}

# Method to cancel the user's purchase
@token_required
def buy_tickets_view(current_user, id):
    if request.method == 'PATCH':
        purchase = BuyTicket.query.filter_by(id=id).first()
        if purchase is None:
            return make_response('This purchase does not exist', 400, {'purchase': 'object does not exist'})
        elif purchase is not None:
            app.logger.debug(purchase.canceled)
            if purchase.canceled:
                return make_response(f'This purchase {purchase.id} has already been cancelled', 400)
            elif not purchase.canceled:
                purchase_detail = BuyTicketDetail.query.filter_by(buy_tickets_id=id).all()
                for detail in purchase_detail:
                    # detail.room_id
                    seats = Room.query.filter_by(id=detail.room_id).first()
                    seats.is_empty = True
                    db.session.commit()
                    purchase.canceled = True
                    db.session.commit()
                return make_response("Your purchase was canceled successfully")
            else:
                return {"error": "The request payload is not in Json format"}
    elif request.method == 'GET':
        purchase = BuyTicket.query.filter_by(id=id).first()
        if purchase is None:
            return make_response('This purchase does not exist', 400, {'purchase': 'object does not exist'})
        elif purchase is not None:
            purchase_details = BuyTicketDetail.query.filter_by(buy_tickets_id=id).all()
            data = {
                "id": purchase.id,
                "canceled": purchase.canceled
            }
            results = []
            for detail in purchase_details:
                room_object = Room.query.get(detail.room_id)
                ticket = {
                    "ticket_id": detail.id,
                    "seats": room_object.seat.name,
                    "B-Feature": {
                        "feature_id": room_object.feature.id,
                        "date_time": room_object.feature.date_time,
                        "C-Movie": {
                            "movie_id": room_object.feature.movie.id,
                            "movie_title": room_object.feature.movie.title,
                            "movie_url_image": room_object.feature.movie.url_image,
                            "movie_classification": room_object.feature.movie.classification,
                        }
                    },
                }
                results.append(ticket)
                data.update({"detail": results})
            return make_response(data)


# Routes of my endpoints
app.add_url_rule('/movies', 'movies', show_movies, methods=['POST', 'GET'])
app.add_url_rule('/features', 'features', show_features, methods=['GET'])
app.add_url_rule('/registration', 'registration', register_user, methods=['POST', 'GET'])
app.add_url_rule('/login', 'logins', login_user, methods=['POST'])
app.add_url_rule('/buy', 'buys', buy_tickets, methods=['POST'])
app.add_url_rule('/sale/<int:id>/', 'sale', buy_tickets_view, methods=['PATCH', 'GET'])
