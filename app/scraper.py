import requests
from bs4 import BeautifulSoup

def scrape(url):
    urls = []
    result = requests.get(url)
    src = result.content
    soup = BeautifulSoup(src, "html.parser")
    for article in soup.find_all("article"):
        a_tag = article.find('a')
        urls.append(a_tag.attrs['href'])
    data = urls[0:3]
    print(len(urls))
    print(urls)
    return urls

# scrape("https://www.bbc.co.uk/search?q=trump&filter=news&suggid=")