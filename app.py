import os

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy
from extensions import db

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    db.init_app(app)
    migrate = Migrate(app, db)
    from views.auth import auth

    app.register_blueprint(auth)
    from views.trainings import training

    app.register_blueprint(training)
    from views.groups import group

    app.register_blueprint(group)
    from views.distances import distance

    app.register_blueprint(distance)
    from views.exercises import exercise

    app.register_blueprint(exercise)
    from views.sets import set

    app.register_blueprint(set)
    from views.weights import weight

    app.register_blueprint(weight)
    
    return app
