"""
DataBase models declaration
"""

from app import db

class Movie(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    director_id = db.Column(db.Integer(), db.ForeignKey("director.id"), default=1, nullable=False)
    category_id = db.Column(db.Integer(), db.ForeignKey("category.id"), default=1, nullable=False)
    show_type = db.Column(db.String(20))
    cast = db.Column(db.String(1000))
    country = db.Column(db.String(150))
    release_year = db.Column(db.Integer())
    rating = db.Column(db.String(50))
    duration = db.Column(db.String(50))
    description = db.Column(db.String(255))

class Director(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    birth_date = db.Column(db.Date())
    is_alive = db.Column(db.Boolean(), default=True)
    
class Category(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(30), nullable=True)



