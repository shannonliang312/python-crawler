from bs4 import BeautifulSoup
import requests

proxy = {
    "http": "socks5://127.0.0.1:1080"
}

loginUrl = 'http://ttmeiju.com/index.php/user/login.html'
loginForm = {
    'username': 'dfsn123',
    'password': 'liangshengnan',
    'loginsubmit': '登录'
}

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,ja;q=0.2",
    "Cache-Control": "max-age=0",
    "Content-Length": "72",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "ttmeiju.com",
    "Origin":"http://ttmeiju.com",
    "Proxy-Connection": "keep-alive",
    "Referer": "http://ttmeiju.com/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
}

s = requests.session()
# result = s.post(url=loginUrl, data=loginForm, headers=headers, proxies=proxy)
# content = result.content
result = s.get('http://ttmeiju.com/', headers=headers, proxies=proxy)
content = result.content

s = BeautifulSoup(content, 'lxml')

print(s.prettify())
