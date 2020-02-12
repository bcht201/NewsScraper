from application.database import write_db

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

def batch_write(search_results):
    for source in search_results:
        for article in source:
            write_db(article)

def empty_results(results):
    blank = 0
    for source in results:
        if len(source) == 0:
            blank += 1
    if blank == 3:
        return True
    else:
        return False