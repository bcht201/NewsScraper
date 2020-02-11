from application.database import write_db
import requests
from bs4 import BeautifulSoup
from application.models import scrapeData

def scrape_web(keyword):
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

    scrape_dm(dm_url, keyword, soup_dm)
    scrape_ts(ts_url, keyword, soup_ts)
    scrape_bbc(bbc_url, keyword, soup_bbc)


def scrape_dm(url_dm, keyword, soup_dm):
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
        write_db(content_dm)

def scrape_ts(url_ts, keyword, soup_ts):
    for article_ts in soup_ts.find_all('a', {'class': 'text-anchor-wrap'}):
        obj = {}
        url_ts = article_ts.attrs['href']
        title_location = article_ts.find('p')
        title_ts = title_location.getText()
        content_ts = scrapeData(
            title = title_ts,
            link = url_ts,
            source = "The Sun",
            keyword = keyword
        )
        write_db(content_ts)


def scrape_bbc(url_bbc, keyword, soup_bbc):
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
        write_db(content_bbc)