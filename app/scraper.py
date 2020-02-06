import requests
from bs4 import BeautifulSoup

urls = []
def scrape(url):
    result = requests.get(url)
    src = result.content
    soup = BeautifulSoup(src, "html.parser")
    for article in soup.find_all("article"):
        a_tag = article.find('a')
        urls.append(a_tag.attrs['href'])
    print(len(urls))
    print(urls)

# scrape("https://www.bbc.co.uk/search?q=trump&filter=news&suggid=")