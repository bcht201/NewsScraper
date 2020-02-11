from application import app
from flask import Flask, render_template, request, redirect, url_for, Blueprint
import time
import random
from flask_sqlalchemy import SQLAlchemy
from application import database
from application import scraper
from flask_login import login_required, current_user

routes = Blueprint("routes", __name__)

def check_keyword(keyword, recents):
    status = False
    for term in recents:
        if keyword == term.keyword:
            status = True
    return status

def cut_down(results, source):
    result_list = [result for result in results if result.source==source]
    array = []
    count = 0
    while len(array) < 4:
        array.append(result_list[count])
        count += 1
    return array

@app.route('/', )
def index():
    return render_template('index.html')

@app.route('/profile', methods=['GET'])
@login_required
def profile():
    recents = database.recent_keywords()
    return render_template('profile.html', recents=recents)

@app.route('/settings', methods=['GET'])
@login_required
def settings():
    return render_template('settings.html')


@app.route('/search', methods=['POST'])
@login_required
def search():
    keyword = request.form['search']
    recents = database.recent_keywords()
    if keyword is None:
        return redirect('/')
    elif check_keyword(keyword, recents) == False:
        time.sleep(random.randint(0, 3))
        scraper.scrape_web( keyword )
    infos = database.get_what_you_just_searched(keyword)
    daily_mail_sources = cut_down(infos, "Daily Mail")
    the_sun_sources = cut_down(infos, "The Sun")
    bbc_sources = cut_down(infos, "BBC")
    infos = daily_mail_sources + the_sun_sources + bbc_sources
    return render_template('profile.html', infos=infos, recents=recents)

@app.route('/search_recent')
@login_required
def search_recent():
    recents = database.recent_keywords()
    keyword = request.args.get('term')
    infos = database.get_what_you_just_searched(keyword)
    daily_mail_sources = cut_down(infos, "Daily Mail")
    the_sun_sources = cut_down(infos, "The Sun")
    bbc_sources = cut_down(infos, "BBC")
    infos = daily_mail_sources + the_sun_sources + bbc_sources
    return render_template('profile.html', infos=infos, recents=recents)


@app.route('/delete')
def delete():
    database.delete()
    return redirect('/')