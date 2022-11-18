from flask import request, app

from database import db
from models.models import Movie


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
                "created_at": movie.created_at

            }
            for movie in movies]

        return {"Count": len(results), "movies": results}