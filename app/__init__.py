from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
import os

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    return app

app = create_app(os.getenv('GOURMET_CONFIG') or 'default')

from . import views
