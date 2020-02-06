import requests
from bs4 import BeautifulSoup

result = requests.get("https://www.bbc.co.uk/search?q=trump&filter=news&suggid=")
src = result.content
soup = BeautifulSoup(src)

urls = []

for article in soup.find_all("article"):
    a_tag = article.find('a')
    urls.append(a_tag.attrs['href'])

print(len(urls))
print(urls)