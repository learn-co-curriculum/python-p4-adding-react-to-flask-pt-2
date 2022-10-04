#!/usr/bin/env python3

from random import choice as rc

from faker import Faker

from app import app
from models import db, Movie

db.init_app(app)

fake = Faker()

def make_movies():

    Movie.query.delete()
    
    movies = []
    for i in range(50):
        m = Movie(title=fake.sentence(nb_words=4).title())
        movies.append(m)

    db.session.add_all(movies)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        make_movies()
