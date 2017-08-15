from bs4 import BeautifulSoup
import requests

proxy = {
    "http": "socks5://127.0.0.1:1080"
}

loginUrl = 'http://hk-bc.xyz/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'
loginForm = {
    'fastloginfield': 'username',
    'username': 'dingfengsaniao',
    'password': 'liangshengnan',
    'quickforward': 'yes',
    'handlekey': '1s'
}

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,ja;q=0.2",
    "Cache-Control":"max-age=0",
    "Connection":"keep-alive",
    "Content-Length":"106",
    "Content-Type":"application/x-www-form-urlencoded",
    "Cookie":"Ovo6_2132_saltkey=q8Y50sIz; Ovo6_2132_lastvisit=1502071138; PHPSESSID=ldoqebosbc2g727ugfa3tvec34; Ovo6_2132_lastact=1502704239%09member.php%09logging",
    "Host":"hk-bc.xyz",
    "Origin":"http://hk-bc.xyz",
    "Referer":"http://hk-bc.xyz/forum.php?gid=1",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
}

headers_content = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,ja;q=0.2",
    "Cache-Control":"max-age=0",
    "Connection":"keep-alive",
    "Host":"hk-bc.xyz",
    # "Origin":"http://hk-bc.xyz",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
}



# result = requests.get('http://www.hk-bc.xyz')
s = requests.session()
# s = requests
cookies = s.post(url=loginUrl, data=loginForm, headers=headers).cookies

# print(cookies)

result = s.get(url='http://hk-bc.xyz/forum-2-1.html', headers=headers_content)
content = result.content

res = BeautifulSoup(content, 'lxml')

for item in res.find_all("a", "xst"):
    print(item)

# print(res.prettify())


