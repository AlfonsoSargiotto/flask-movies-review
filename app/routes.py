from flask import (
    render_template,
    url_for,
    abort,
    flash,
    redirect,
    request,
)
from sqlalchemy import or_

from app import app, db
from app.forms import MovieForm
from app.models import Director, Movie, Category
from app.helpers.models_formatter import get_tuples


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


@app.route("/new_movie", methods=["GET", "POST"])
def new_movie():
    categories_list = get_tuples(Category.query.order_by(Category.name.asc()).all())
    directors_list = get_tuples(Director.query.order_by(Director.name.asc()).all())
    form = MovieForm()
    form.category_id.choices = categories_list
    form.director_id.choices = directors_list
    if form.validate_on_submit():
        movie = Movie(
            title=form.title.data,
            director_id=form.director_id.data,
            category_id=form.category_id.data,
            rating=form.rating.data,
            show_type=form.show_type.data,
            cast=form.cast.data,
            country=form.country.data,
            release_year=form.release_year.data,
            score=form.score.data,
            duration=form.duration.data,
            description=form.description.data,
        )

        db.session.add(movie)
        db.session.commit()
        flash("Movie succesfully created!", "success")
        return redirect(url_for("movie"))

    template_title = "New Movie"
    return render_template("new_movie.html", form=form, template_title=template_title)


@app.route("/movie/edit/<movie_id>", methods=["GET", "POST"])
def edit_movie(movie_id):
    categories_list = get_tuples(Category.query.order_by(Category.name.asc()).all())
    directors_list = get_tuples(Director.query.order_by(Director.name.asc()).all())
    movie = Movie.query.filter_by(id=movie_id).first()
    form = MovieForm(obj=movie)
    form.category_id.choices = categories_list
    form.director_id.choices = directors_list

    if request.method == "POST" and form.validate_on_submit():
        form.populate_obj(movie)
        db.session.commit()

        flash("Movie succesfully modified!", "info")
        return redirect(url_for("movie"))

    template_title = "Update Movie"
    return render_template("new_movie.html", form=form, template_title=template_title)
