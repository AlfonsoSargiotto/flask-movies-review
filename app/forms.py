"""
Forms for CRUD operations
"""


from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    BooleanField,
    DateField,
    SelectField,
    TextAreaField,
    IntegerField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    ValidationError,
    NumberRange,
)
from app.models import Director, Movie


class DirectorForm(FlaskForm):
    name = StringField(
        "Full name/s",
        validators=[DataRequired(), Length(min=1, max=255)],
        render_kw={"placeholder": "Introduce full name"},
    )
    birth_date = DateField("Birth date", validators=[DataRequired()])
    is_alive = BooleanField(
        "is alive?",
    )
    submit = SubmitField("Confirm")

    def validate_name(self, name):
        director = Director.query.filter_by(name=name.data).first()
        if director:
            raise ValidationError(f"Director '{name.data}' is already in our database")


class MovieForm(FlaskForm):
    title = StringField(
        "Full name",
        validators=[DataRequired(), Length(min=1, max=150)],
        render_kw={"placeholder": "Introduce Movie/TV Show's title"},
    )
    director_id = "[]"
    category_id = SelectField(
        "Category",
        validators=[DataRequired()],
        render_kw={"placeholder": "Please choose a category"},
        choices=[],
    )
    show_type = SelectField(
        "Show Type",
        validators=[DataRequired()],
        render_kw={"placeholder": "Please choose show type"},
        choices=["Movie", "TV Show"],
    )
    cast = StringField(
        "Cast",
        validators=[DataRequired(), Length(min=1, max=1000)],
        render_kw={"placeholder": "Main roles cast"},
    )
    country = StringField(
        "Origin country",
        validators=[DataRequired(), Length(min=1, max=150)],
        render_kw={"placeholder": "Country where was produced"},
    )
    release_year = IntegerField(
        validators=[DataRequired(), NumberRange(min=1850, max=2023)],
        render_kw={"placeholder": "Release year (YYYY format)"},
    )
    rating = SelectField(
        "Rating",
        validators=[DataRequired()],
        render_kw={"placeholder": "Please choose an option"},
        choices=["PG", "PG-13", "R", "TV-14", "TV-G", "TV-M", "TV-MA", "TV-Y", "TV-Y7"],
    )
    score = IntegerField(
        validators=[DataRequired(), NumberRange(min=0, max=10)],
        render_kw={"placeholder": "Release year (YYYY format)"},
    )
    duration = StringField(
        "Movie-TV Show duration",
        validators=[DataRequired(), Length(min=1, max=255)],
        render_kw={
            "placeholder": "Movie/TV Show's duration. Can be seasons,episodes or minutes."
        },
    )
    description = TextAreaField(
        "Movie description",
        validators=[DataRequired(), Length(min=1, max=1000)],
        render_kw={
            "placeholder": "Write a short description about the Movie/Tv Show. 1000 characters max."
        },
    )
    submit = SubmitField("Confirm")

    def validate_title(self, title):
        movie = Movie.query.filter_by(title=title.data).first()
        if movie:
            raise ValidationError(
                f"The Movie/TV Show named '{title.data}' is already in our database"
            )
