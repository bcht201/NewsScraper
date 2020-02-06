from app import app
from flask import Flask, render_template, request, redirect, url_for
from . import scraper
import time
import random

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
        links, titles = scraper.scrape('https://www.bbc.co.uk/search?q=' + search_query + '&filter=news')
        return render_template('index.html', titles=titles, links=links)
