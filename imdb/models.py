from datetime import datetime
from imdb import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    production = db.Column(db.String(60), nullable=False)
    genre = db.Column(db.String(30), nullable=False)
    popularity = db.Column(db.String(20), nullable=False)
    year = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"Movie('{self.name}', '{self.production}, '{self.genre}', '{self.popularity}', '{self.year}')"
