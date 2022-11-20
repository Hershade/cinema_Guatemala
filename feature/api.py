from flask import  request
from database import db
from models.models import Feature
def show_features():
    if request.method == 'GET':
        features = Feature.query.all()
        results= [
            {
                "id" : feature.id,
                "date_time": feature.date_time,
                'movie_id': feature.movies_id
            }
            for feature in features
        ]
    return {"count": len(results), "features": results}