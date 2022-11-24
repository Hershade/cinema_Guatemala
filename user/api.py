
import uuid

from flask import request
from werkzeug.security import generate_password_hash

from database import db
from models.models import User


def register_user():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            hashed_password = generate_password_hash(data['password'], method='sha256')
            new_user = User(name=data['name'], last_name=data['last_name'], password=hashed_password,
                            user_token=str(uuid.uuid4()), email=data['email'], phone=data['phone'])
            db.session.add(new_user)
            db.session.commit()
            return {"message": f"Welcome {new_user.name} your user has been created successfully."}
        else:
            return {"error": "The request payload is not in Json format"}
    elif request.method == 'GET':
        users = User.query.all()

        results = [
            {
                "name": user.name,
                "last_name": user.last_name,
                "email": user.email,
                "phone": user.phone
            }
            for user in users
        ]
        return {"Count": len(results), "users": results}


