from application.database import write_db
import requests
from bs4 import BeautifulSoup
from application.models import scrapeData

def scrape_web(keyword, keyword_id):
    dm_url = 'https://www.dailymail.co.uk/home/search.html?sel=site&searchPhrase=' + keyword
    ts_url =  'https://www.thesun.co.uk/?s=' + keyword
    bbc_url = 'https://www.bbc.co.uk/search?q=' + keyword + '&filter=news'
    
    result = requests.get(dm_url)
    src = result.content
    soup_dm = BeautifulSoup(src, "html.parser")

    result = requests.get(ts_url)
    src = result.content
    soup_ts = BeautifulSoup(src, "html.parser")

    result = requests.get(bbc_url)
    src = result.content
    soup_bbc = BeautifulSoup(src, "html.parser")

    dm_results = scrape_dm(dm_url, keyword_id, soup_dm)
    ts_reults = scrape_ts(ts_url, keyword_id, soup_ts)
    bbc_results = scrape_bbc(bbc_url, keyword_id, soup_bbc)

    final_results = []
    final_results.extend([dm_results, ts_reults, bbc_results])
    return final_results

def scrape_dm(url_dm, keyword_id, soup_dm):
    array = []
    for article_dm in soup_dm.find_all('h3', {'class': 'sch-res-title'}):
        a_tag_dm = article_dm.find('a')
        url_dm = a_tag_dm.attrs['href']
        url_dm_to_save = "https://www.dailymail.co.uk/" + url_dm
        title_dm = a_tag_dm.getText()
        if(title_dm is not None and url_dm is not None):
            content_dm = scrapeData(
                title = title_dm,
                link = url_dm_to_save,
                source = "Daily Mail",
                keyword = keyword_id
            )
            array.append(content_dm)
        print(len(array))
    return array

def scrape_ts(url_ts, keyword_id, soup_ts):
    array = []
    for article_ts in soup_ts.find_all('a', {'class': 'text-anchor-wrap'}):
        url_ts = article_ts.attrs['href']
        title_location = article_ts.find('p')
        title_ts = title_location.getText()
        if(title_ts is not None and url_ts is not None):
            content_ts = scrapeData(
                title = title_ts,
                link = url_ts,
                source = "The Sun",
                keyword = keyword_id
            )
            array.append(content_ts)
        print(len(array))
    return array


def scrape_bbc(url_bbc, keyword_id, soup_bbc):
    array = []
    for article_bbc in soup_bbc.find_all("article"):
        a_tag_bbc = article_bbc.find('a')
        url_bbc = a_tag_bbc.attrs['href']
        title_bbc = article_bbc.attrs['data-bbc-title']
        if(title_bbc is not None and url_bbc is not None):
            content_bbc = scrapeData(
                title = title_bbc,
                link = url_bbc,
                source = "BBC",
                keyword = keyword_id
            )
            array.append(content_bbc)
        print(len(array))
    return array