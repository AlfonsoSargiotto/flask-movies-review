from flask import (
    render_template,
    abort,
    flash,
    request,
)
from sqlalchemy import or_

from app import app, db
from app.models import Director, Movie, Category


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/login")
def login():
    return render_template("error/404.html")


@app.route("/show-error")
def show_error_500():
    abort(500)


@app.route("/movie", methods=["GET", "POST"])
@app.route("/movie/<movie_id>")
def movie(movie_id=None):
    error_msg = None
    if movie_id is not None:
        movie = Movie.query.filter(Movie.id == movie_id).first()
        if movie:
            return render_template("movie.html", movie=movie)
        else:
            error_msg = (
                "Sorry, the movie you have chosen doesn't exist, please try again."
            )

    page = request.args.get("page", 1, type=int)
    movies = Movie.query.paginate(page=page, per_page=50)

    search_parameter = request.args.get("search_parameter", type=str)
    if search_parameter:
        movies = Movie.query.filter(
            or_(
                Movie.title.like(f"%{search_parameter}%"),
                Movie.cast.like(f"%{search_parameter}%"),
                Movie.director.has(Director.name.like(f"%{search_parameter}%")),
                Movie.category.has(Category.name.like(f"%{search_parameter}%")),
            )
        ).paginate(page=page, per_page=25)

    if error_msg:
        flash(error_msg)

    return render_template(
        "movies.html", movies=movies, search_parameter=search_parameter
    )


@app.route("/movie/top-ten")
def top_ten():
    top_ten_movies = Movie.query.order_by(Movie.score.desc()).limit(10)

    return render_template("top_ten_movies.html", movies=top_ten_movies)
