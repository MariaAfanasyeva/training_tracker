import os

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_ENGINE")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["DEBUG"] = os.getenv("DEBUG")

db = SQLAlchemy(app)
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
