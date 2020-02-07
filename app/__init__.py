from flask import Flask

app = Flask(__name__)
from . import routes
from . import scraper
from app.routes import db
from app.routes import scrapeData
from app import app
