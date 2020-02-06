from app import app
from flask import Flask, render_template, request, redirect, url_for
# from scraper import scrape
from . import scraper

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
        data = scraper.scrape('https://www.bbc.co.uk/search?q=' + search_query + '&filter=news')
        print(data)
        return render_template('index.html', data=data)
