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
    while len(array) < 2:
        array.append(result_list[count])
        count += 1
    return array

@app.route('/', )
def index():
    return render_template('index.html', user=current_user)

@app.route('/profile', methods=['GET'])
@login_required
def profile():
    recents = database.recent_keywords(str(current_user.id))
    return render_template('profile.html', recents=recents, user=current_user)

@app.route('/settings', methods=['GET'])
@login_required
def settings():
    results = database.get_current_settings(current_user.id)
    return render_template('settings.html', current_settings = results[0])


@app.route('/search', methods=['POST'])
@login_required
def search():
    keyword = request.form['search']
    recents = database.recent_keywords(str(current_user.id))
    # key_id = database.write_user_keyword(keyword, current_user.id)
    if keyword is None:
        return redirect('/')
    elif not database.db_check_keyword(keyword):
        database.write_keyword(keyword)
        key_id = database.write_user_keyword(keyword, current_user.id)
        time.sleep(random.randint(0, 3))
        scraper.scrape_web(keyword, key_id)
    
    kw_id = database.write_user_keyword(keyword, current_user.id)
    infos = database.get_what_you_just_searched(kw_id)
    print('infos before...:')
    print(infos)
    if len(infos) == 0:
        return render_template('profile.html', error=1, recents=recents)
    else:
        
        # daily_mail_sources = cut_down(infos, "Daily Mail")
        the_sun_sources = cut_down(infos, "The Sun")
        bbc_sources = cut_down(infos, "BBC")
        infos = the_sun_sources + bbc_sources
        print('infos after...:')
        print(infos)
        return render_template('profile.html', infos=infos, recents=recents)

@app.route('/search_recent')
@login_required
def search_recent():
    recents = database.recent_keywords(str(current_user.id))
    keyword = request.args.get('term')
    key_id = database.get_keyword_id(keyword)
    infos = database.get_what_you_just_searched(str(key_id[0].id))
    daily_mail_sources = cut_down(infos, "Daily Mail")
    the_sun_sources = cut_down(infos, "The Sun")
    bbc_sources = cut_down(infos, "BBC")
    infos = daily_mail_sources + the_sun_sources + bbc_sources
    return render_template('profile.html', infos=infos, recents=recents)

@app.route('/settings_update', methods=['POST'])
def update_settings():
    recents = database.recent_keywords(str(current_user.id))
    BBC = request.form.get("BBC")
    DM = request.form.get("DM")
    TS = request.form.get("TS")
    database.db_update_settings(BBC, DM, TS, current_user.id)
    return render_template('profile.html', recents=recents, updated=1)

@app.route('/delete')
def delete():
    database.delete()
    return redirect('/')