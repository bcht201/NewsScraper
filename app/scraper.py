import requests
from bs4 import BeautifulSoup

def scrape(url):
    urls = []
    titles = []
    result = requests.get(url)
    src = result.content
    soup = BeautifulSoup(src, "html.parser")
    for article in soup.find_all("article"):
        a_tag = article.find('a')
        urls.append(a_tag.attrs['href'])
        title = article.attrs['data-bbc-title']
        titles.append(title)
    data = urls[0:3]
    print(titles)
    return urls, titles

# scrape("https://www.bbc.co.uk/search?q=trump&filter=news&suggid=")