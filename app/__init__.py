from flask import Flask

app = Flask(__name__)
from . import routes
from . import scraper
from app.db_classes.db_class import Data_Scrape
from app import app
