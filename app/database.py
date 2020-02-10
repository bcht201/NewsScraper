def read_db(sql):
    return db.engine.execute(sql)

def write_db(sql):
    print('written')


def recent_keywords():
    sql = text("SELECT DISTINCT source, keyword FROM scraped_data_all WHERE source='BBC'") # alter accordingly
    results = read_db(sql)
    return [row for row in results]
    

def get_what_you_just_searched(keyword):
    sql = text("SELECT title, link, keyword, source FROM scraped_data_all WHERE keyword='" + keyword + "'")
    new_stuff = read_db(sql)
    return [row for row in execute]
