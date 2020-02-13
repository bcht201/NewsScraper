from application import app
from flask import Flask, render_template, request, redirect, url_for, Blueprint
import time
import random
from flask_sqlalchemy import SQLAlchemy
from application import database
from application import scraper
from flask_login import login_required, current_user
from application.helper_functions import check_keyword, cut_down, batch_write, empty_results

routes = Blueprint("routes", __name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/home', methods=['GET'])
@login_required
def index_home():
    settings = database.get_current_settings(current_user.id)
    return render_template('index.html', user=current_user, settings=settings[0])


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
    next_key_id = 0
    keyword = request.form['search']
    recents = database.recent_keywords(str(current_user.id))
    result = database.get_next_kw_id()

    if len(result) == 0:
        next_key_id = 1
    else:
        next_key_id = result[0].id + 1
    if not database.db_check_keyword(keyword):
        time.sleep(random.randint(0, 3))
        search_results = scraper.scrape_web(keyword, next_key_id)
        if empty_results(search_results):
            return render_template('profile.html', error=1, recents=recents)
        else:
            database.write_keyword(keyword)
            database.write_user_keyword(keyword, current_user.id)
            batch_write(search_results)
            information = database.get_what_you_just_searched(next_key_id)
            current_settings = database.get_current_settings(current_user.id)
            bbc_setting = current_settings[0].BBC_quant
            ts_setting = current_settings[0].TS_quant
            dm_setting = current_settings[0].DM_quant
            bbc_sources = cut_down(information, "BBC", bbc_setting)
            the_sun_sources = cut_down(information, "The Sun", ts_setting)
            daily_mail_sources = cut_down(information, "Daily Mail", dm_setting)
            infos = daily_mail_sources + the_sun_sources + bbc_sources
            return render_template('profile.html', infos=infos, recents=recents)
    else:
        id_search = database.get_keyword_id(keyword)
        kw_id = id_search[0].id
        information = database.get_what_you_just_searched(kw_id)
        current_settings = database.get_current_settings(current_user.id)
        bbc_setting = current_settings[0].BBC_quant
        ts_setting = current_settings[0].TS_quant
        dm_setting = current_settings[0].DM_quant
        bbc_sources = cut_down(information, "BBC", bbc_setting)
        the_sun_sources = cut_down(information, "The Sun", ts_setting)
        daily_mail_sources = cut_down(information, "Daily Mail", dm_setting)
        infos = daily_mail_sources + the_sun_sources + bbc_sources
        return render_template('profile.html', infos=infos, recents=recents)

@app.route('/search_recent')
@login_required
def search_recent():
    recents = database.recent_keywords(str(current_user.id))
    keyword = request.args.get('term')
    key_id = database.get_keyword_id(keyword)
    infos = database.get_what_you_just_searched(str(key_id[0].id))
    current_settings = database.get_current_settings(current_user.id)
    bbc_setting = current_settings[0].BBC_quant
    ts_setting = current_settings[0].TS_quant
    dm_setting = current_settings[0].DM_quant
    bbc_sources = cut_down(infos, "BBC", bbc_setting)
    the_sun_sources = cut_down(infos, "The Sun", ts_setting)
    daily_mail_sources = cut_down(infos, "Daily Mail", dm_setting)
    infos = daily_mail_sources + the_sun_sources + bbc_sources
    return render_template('profile.html', infos=infos, recents=recents)

@app.route('/settings_update', methods=['POST'])
def update_settings():
    recents = database.recent_keywords(str(current_user.id))
    BBC = request.form.get("BBC")
    DM = request.form.get("DM")
    TS = request.form.get("TS")
    database.db_update_settings(BBC, DM, TS, current_user.id)
    current_settings = database.get_current_settings(current_user.id)
    return render_template('settings.html', current_settings=current_settings[0], updated=1)