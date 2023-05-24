""" from flask_mongoengine import MongoEngine


db = MongoEngine()

"""
from flask_sqlalchemy import SQLAlchemy


def initialize_db():
    from DataLineageAPI import app

    db = SQLAlchemy(app)

    with app.app_context():
        db.create_all()

    return db
