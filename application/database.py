from sqlalchemy import text
from application import db
from application.models import Keyword, User_Search, User


def read_db(sql):
    execute = db.engine.execute(sql)
    return [row for row in execute]

def write_db(content):
    db.session.add(content)
    db.session.commit()

def db_check_keyword(keyword):
    sql = text("SELECT id, keyword FROM keyword WHERE keyword='" + keyword + "'")
    return read_db(sql)

def write_keyword(keyword):
    obj = Keyword(
        keyword = keyword
    )
    write_db(obj)

def get_next_kw_id():
    sql = text("SELECT id FROM keyword ORDER BY id DESC")
    return read_db(sql)

def write_user_keyword(keyword, user_id):
    keyword_and_id = db_check_keyword(keyword)
    obj = User_Search(
        user_id = user_id,
        keyword_id = keyword_and_id[0].id
    )
    write_db(obj)
    
def get_keyword_id(keyword):
    sql = text("SELECT id FROM keyword WHERE keyword='" + keyword + "'")
    return read_db(sql)

def recent_keywords(user_id):
    sql = text("SELECT DISTINCT user_search.id, keyword.keyword FROM user_search JOIN keyword ON user_search.keyword_id = keyword.id WHERE user_search.user_id = " + user_id)
    return read_db(sql)

def get_what_you_just_searched(key_id):
    sql = text("SELECT title, link, keyword, source FROM scraped_data_all WHERE keyword=" + str(key_id))
    return read_db(sql)

def db_update_settings(BBC, DM, TS, user_id):
    x = db.session.query(User).get(user_id)
    x.BBC_quant = BBC
    x.TS_quant = TS
    x.DM_quant = DM
    db.session.commit()

def check_user(email):
    sql = text("SELECT * FROM user WHERE email='" + email + "'")
    return read_db(sql)

def get_current_settings(user_id):
    sql = text('SELECT BBC_quant, TS_quant, DM_quant FROM user WHERE id = ' + str(user_id))
    return read_db(sql)

def delete():
    sql = text("DELETE FROM scraped_data_all")
    execute = db.engine.execute(sql)

