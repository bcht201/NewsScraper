from flask import Flask

app = Flask(__name__)
from . import scraper
from . import routes
from app import app
