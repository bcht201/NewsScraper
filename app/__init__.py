from flask import Flask

app = Flask(__name__)
from . import routes
from . import scraper
from app import app
