from sqlalchemy import text
from application import db


def read_db(sql):
    return db.engine.execute(sql)

def write_db(content):
    db.session.add(content)
    db.session.commit()

def recent_keywords():
    sql = text("SELECT DISTINCT source, keyword FROM scraped_data_all WHERE source='BBC'")
    results = read_db(sql)
    return [row for row in results]

def get_what_you_just_searched(keyword):
    sql = text("SELECT title, link, keyword, source FROM scraped_data_all WHERE keyword='" + keyword + "'")
    execute = read_db(sql)
    return [row for row in execute]

def delete():
    sql = text("DELETE FROM scraped_data_all")
    execute = db.engine.execute(sql)
