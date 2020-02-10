from flask import Flask

app = Flask(__name__)

from . import routes
from . import scraper
from application.routes import db
from application.routes import scrapeData
from application import app
