from app import app
from flask import Flask, render_template, request, redirect, url_for
from . import scraper
import time
import datetime
import random
# from app.db_classes.db_class import Data_Scrape
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import requests
from bs4 import BeautifulSoup

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

class scrapeData(db.Model):
    __tablename__ = "scraped_data_all"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    link = db.Column(db.String(500), nullable=False)
    source = db.Column(db.String(200), nullable=False)
    keyword = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.datetime.utcnow)

def scrape(url, keyword):
    result = requests.get(url)
    src = result.content
    soup = BeautifulSoup(src, "html.parser")
    for article in soup.find_all("article"):
        obj = {}
        a_tag = article.find('a')
        url = a_tag.attrs['href']
        title = article.attrs['data-bbc-title']
        content = scrapeData(
            title = title,
            link = url,
            source = "BBC",
            keyword = keyword
        )
        db.session.add(content)
        db.session.commit()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['search']
    scrape('https://www.bbc.co.uk/search?q=' + keyword + '&filter=news', keyword)
    return render_template('index.html', )





    # scrape()
    # search_query = request.form['search']
    # sql = text("SELECT keyword FROM scrapeData WHERE keyword LIKE '%" + search_query + "%'")
    # execute = db.engine.execute(sql)
    # result = [row for rows in execute]
    # print(result)
    return "Hello"
    # already_scraped = db.data_scrape.filter(db.data_scrape.keyword == search_query)
    # print(already_scraped)
    # if len(already_scraped) > 1:
    #     return "Already scraped"
    # else:
    #     return "Not scraped yet"

    # search_query = request.form['search']
    # search_query = search_query.replace(' ', '+')
    # if search_query is None:
    #     return redirect('/')
    # else:
    #     time.sleep(random.randint(0, 3))
    #     data = scraper.scrape('https://www.bbc.co.uk/search?q=' + search_query + '&filter=news')


    #     return render_template('index.html', infos=data)
	

@app.route('/populate', methods=["POST"])
def add_data():
    content = scrapeData(
        title=request.form["title"],
        link=request.form["link"],
        source=request.form["source"],
        keyword=request.form["keyword"]
    )
    db.session.add(content)
    db.session.commit()
    return "you populated the db"