from app import app
from flask import Flask, render_template, request, redirect, url_for
# from scraper import scrape
from . import scraper

@app.route('/')
def index():
    data = scraper.scrape("https://www.bbc.co.uk/search?q=boris&sa_f=search-product&filter=news&suggid=")
    return render_template('index.html', data=data)