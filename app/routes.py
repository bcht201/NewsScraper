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

def scrape_dm(url_dm, keyword):
    result_dm = requests.get(url_dm)
    src_dm = result_dm.content
    soup_dm = BeautifulSoup(src_dm, "html.parser")
    for article_dm in soup_dm.find_all('h3', {'class': 'sch-res-title'}):
        obj = {}
        a_tag_dm = article_dm.find('a')
        url_dm = a_tag_dm.attrs['href']
        url_dm_to_save = "https://www.dailymail.co.uk/" + url_dm
        title_dm = a_tag_dm.getText()

        content_dm = scrapeData(
            title = title_dm,
            link = url_dm_to_save,
            source = "Daily Mail",
            keyword = keyword
        )
        db.session.add(content_dm)
        db.session.commit()

def scrape_ts(url_ts, keyword):
    result_ts = requests.get(url_ts)
    src_ts = result_ts.content
    soup_ts = BeautifulSoup(src_ts, "html.parser")
    for article_ts in soup_ts.find_all('a', {'class': 'text-anchor-wrap'}):
        obj = {}
        url_ts = article_ts.attrs['href']
        # url_ts_to_save = "https://www.dailymail.co.uk/" + url_ts
        title_location = article_ts.find('p')
        title_ts = title_location.getText()

        content_ts = scrapeData(
            title = title_ts,
            link = url_ts,
            source = "The Sun",
            keyword = keyword
        )
        db.session.add(content_ts)
        db.session.commit()


def scrape_bbc(url_bbc, keyword):
    result_bbc = requests.get(url_bbc)
    src_bbc = result_bbc.content
    soup_bbc = BeautifulSoup(src_bbc, "html.parser")
    for article_bbc in soup_bbc.find_all("article"):
        obj = {}
        a_tag_bbc = article_bbc.find('a')
        url_bbc = a_tag_bbc.attrs['href']
        title_bbc = article_bbc.attrs['data-bbc-title']
        content_bbc = scrapeData(
            title = title_bbc,
            link = url_bbc,
            source = "BBC",
            keyword = keyword
        )
        db.session.add(content_bbc)
        db.session.commit()

def recent_keywords():
    sql = text("SELECT DISTINCT source, keyword FROM scraped_data_all WHERE source='BBC'")
    execute = db.engine.execute(sql)
    return [row for row in execute]

def check_keyword(keyword, recents):
    status = False
    for term in recents:
        if keyword == term.keyword:
            status = True
    return status

@app.route('/', methods=['GET'])
def index():
    sql = text("SELECT DISTINCT keyword FROM scraped_data_all")
    execute = db.engine.execute(sql)
    recents = [row for row in execute]
    return render_template('index.html', recents=recents)

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['search']
    recents = recent_keywords()
    # print(recents)
    # print(type(recents))
    # print(recents[0])
    # print(type(recents[0]))
    # print(recents[0].keyword)
    if keyword is None:
        return redirect('/')
    elif check_keyword(keyword, recents) == False:
        time.sleep(random.randint(0, 3))
        scrape_dm('https://www.dailymail.co.uk/home/search.html?sel=site&searchPhrase=' + keyword, keyword)
        scrape_ts('https://www.thesun.co.uk/?s=' + keyword, keyword)
        scrape_bbc('https://www.bbc.co.uk/search?q=' + keyword + '&filter=news', keyword)
    sql = text("SELECT title, link, keyword, source FROM scraped_data_all WHERE keyword='" + keyword + "'")
    execute = db.engine.execute(sql)
    infos = [row for row in execute]
    # print(infos)
    return render_template('index.html', infos=infos, recents=recents)




@app.route('/delete')
def delete():
    sql = text("DELETE FROM scraped_data_all")
    execute = db.engine.execute(sql)
    return redirect('/')

