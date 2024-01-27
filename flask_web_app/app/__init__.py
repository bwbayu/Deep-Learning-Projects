# file main website
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__, static_url_path='/static') # init flask
app.secret_key = 'your_secret_key'
app.config.from_object(Config) # init config database

db = SQLAlchemy(app) # init sqlalchemy pada app
migrate = Migrate(app, db) # init migrasi database

from app.model import user_sentiment, user_image # init model user_sentiment dan user_image
from app import routes # init routes
