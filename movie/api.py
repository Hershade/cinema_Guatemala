from flask import request

from database import db
from models.models import Movie, Feature


# Function to convert to Json
def features_view(model, id):
    all_features = model.query.filter_by(movies_id=id).all()
    results = [
        {
            "id": feature.id,
            "date_time": feature.date_time,
            "created_at": feature.created_at,
            "movies_id": feature.movies_id,
        }
        for feature in all_features]
    return results


# @app.route('/movies', methods=['POST', 'GET'])


def show_movies():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_movie = Movie(title=data['title'], url_image=data['url_image'],
                              classification=data['classification'])
            db.session.add(new_movie)
            db.session.commit()
            return {"message": f"Movie {new_movie.title} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}
    elif request.method == 'GET':
        movies = Movie.query.all()

        results = [
            {
                "id": movie.id,
                "title": movie.title,
                "url_image": movie.url_image,
                "classification": movie.classification,
                "created_at": movie.created_at,
                "features": features_view(Feature, movie.id)

            }
            for movie in movies]

        return {"Count": len(results), "movies": results}
