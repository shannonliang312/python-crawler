from bs4 import BeautifulSoup
import requests

s = requests
url = 'https://www.pornhub.com'

proxy = {
    "http": "http://127.0.0.1:1080"
}

result = s.get(url=url)
content = result.content
res = BeautifulSoup(content, 'lxml')

print(res.prettify())