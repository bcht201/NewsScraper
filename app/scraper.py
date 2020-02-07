# import requests

# from bs4 import BeautifulSoup


    # search_data = []
    # result = requests.get(url)
    # src = result.content
    # soup = BeautifulSoup(src, "html.parser")
    # for article in soup.find_all("article"):
    #     obj = {}
    #     a_tag = article.find('a')
    #     url = a_tag.attrs['href']
    #     title = article.attrs['data-bbc-title']
    #     obj["title"] = title
    #     obj["link"] = url
    #     search_data.append(obj)
    # print(search_data)
    # print(type(search_data))
    # return search_data

