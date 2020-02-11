from application import app
from flask import Flask, render_template, request, redirect, url_for
import time
import random
from flask_sqlalchemy import SQLAlchemy
from application import database
from application import scraper


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

@app.route('/', methods=['GET'])
def index():
    recents = database.recent_keywords()
    return render_template('index.html', recents=recents)


@app.route('/search', methods=['POST'])
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
    return render_template('index.html', infos=infos, recents=recents)

@app.route('/search_recent')
def search_recent():
    recents = database.recent_keywords()
    keyword = request.args.get('term')
    infos = database.get_what_you_just_searched(keyword)
    daily_mail_sources = cut_down(infos, "Daily Mail")
    the_sun_sources = cut_down(infos, "The Sun")
    bbc_sources = cut_down(infos, "BBC")
    infos = daily_mail_sources + the_sun_sources + bbc_sources
    return render_template('index.html', infos=infos, recents=recents)


@app.route('/delete')
def delete():
    database.delete()
    return redirect('/')















# def scrape_dm(url_dm, keyword):
#     result_dm = requests.get(url_dm)
#     src_dm = result_dm.content
#     soup_dm = BeautifulSoup(src_dm, "html.parser")
#     for article_dm in soup_dm.find_all('h3', {'class': 'sch-res-title'}):
#         obj = {}
#         a_tag_dm = article_dm.find('a')
#         url_dm = a_tag_dm.attrs['href']
#         url_dm_to_save = "https://www.dailymail.co.uk/" + url_dm
#         title_dm = a_tag_dm.getText()
#         content_dm = scrapeData(
#             title = title_dm,
#             link = url_dm_to_save,
#             source = "Daily Mail",
#             keyword = keyword
#         )
#         db.session.add(content_dm)
#         db.session.commit()

# def scrape_ts(url_ts, keyword):
#     result_ts = requests.get(url_ts)
#     src_ts = result_ts.content
#     soup_ts = BeautifulSoup(src_ts, "html.parser")
#     for article_ts in soup_ts.find_all('a', {'class': 'text-anchor-wrap'}):
#         obj = {}
#         url_ts = article_ts.attrs['href']
#         title_location = article_ts.find('p')
#         title_ts = title_location.getText()
#         content_ts = scrapeData(
#             title = title_ts,
#             link = url_ts,
#             source = "The Sun",
#             keyword = keyword
#         )
#         db.session.add(content_ts)
#         db.session.commit()


# def scrape_bbc(url_bbc, keyword):
#     result_bbc = requests.get(url_bbc)
#     src_bbc = result_bbc.content
#     soup_bbc = BeautifulSoup(src_bbc, "html.parser")
#     for article_bbc in soup_bbc.find_all("article"):
#         obj = {}
#         a_tag_bbc = article_bbc.find('a')
#         url_bbc = a_tag_bbc.attrs['href']
#         title_bbc = article_bbc.attrs['data-bbc-title']
#         content_bbc = scrapeData(
#             title = title_bbc,
#             link = url_bbc,
#             source = "BBC",
#             keyword = keyword
#         )
#         db.session.add(content_bbc)
#         db.session.commit()




# def recent_keywords():
#     sql = text("SELECT DISTINCT source, keyword FROM scraped_data_all WHERE source='BBC'")
#     execute = db.engine.execute(sql)
#     return [row for row in execute]
