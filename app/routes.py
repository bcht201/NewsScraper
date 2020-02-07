from app import app
from flask import Flask, render_template, request, redirect, url_for
from . import scraper
import time
import random
# from app.db_classes.db_class import Data_Scrape
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scrapes.db'

db = SQLAlchemy(app)

@app.before_first_request
def create_table():
    db.create_all()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search_query = request.form['search']
    search_query = search_query.replace(' ', '+')
    if search_query is None:
        return redirect('/')
    else:
        time.sleep(random.randint(0, 3))
        data = scraper.scrape('https://www.bbc.co.uk/search?q=' + search_query + '&filter=news')


        return render_template('index.html', infos=data)
	
