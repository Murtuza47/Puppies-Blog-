import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from project.core.views import core
from project.error_pages.handlers import error_pages
from flask_login import LoginManager

app = Flask(__name__)
login_manager = LoginManager()

####################### Data Base Setup ##############################

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SECRET_KEY"] = ""
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://" + os.path.join(BASE_DIR, "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

app.register_blueprint(core)
app.register_blueprint(error_pages)

login_manager.init_app(app)
login_manager.login_view = 'users.login'

Migrate(app, db)
