from bs4 import BeautifulSoup
import requests

s = requests
url = 'https://www.pornhub.com/categories'

proxies = {
    "http": "http://127.0.0.1:1080/"
}

result = s.get(url=url)
content = result.content
res = BeautifulSoup(content, 'lxml')

categories = res.find_all('li', class_='cat_pic')

print(categories)
