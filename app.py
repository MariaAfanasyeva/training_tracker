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


@app.route("/")
def hello():
    return "Hello, world"
