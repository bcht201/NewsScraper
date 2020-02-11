from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['DEBUG'] = True

db = SQLAlchemy(app)

from . import routes
from . import scraper
from . import database
from application import app