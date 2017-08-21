from bs4 import BeautifulSoup
from pprint import pprint
from pymongo import MongoClient
import requests
import os

s = requests
url = 'https://www.pornhub.com/categories'

proxies = {
    "http": "http://127.0.0.1:1080/"
}

result = s.get(url=url)
content = result.content
res = BeautifulSoup(content, 'lxml')

# 获取页面频道节点
categories = res.find_all('li', class_='cat_pic')

res_list = []

# 新建文本文件保存目录信息
fp = open('category_info.txt', 'w+')

#遍历节点
for category in categories:
    img_url = category.find('img')['src']
    tmp = {}
    tmp['id'] = category["data-category"]
    tmp['title'] = category.find("strong").text
    tmp['href'] = 'https://www.pornhub.com' + category.find_all("a")[0]["href"]
    tmp['cover_url'] = img_url
    
    img_title = tmp['title'].replace('/', '_')
    dirname = './cover_img'
    
    res_list.append(tmp)
    fp.write(str(tmp) + '\n')
    
    if not os.path.exists(dirname):
        os.mkdir(dirname)
        
    img = requests.get(img_url)
    if img.status_code == 200:
        img_fp = open(dirname + '/' + img_title + '.jpg', 'wb')
        img_fp.write(img.content)
        img_fp.close()
        print("{0} done!".format(img_title))

# 按照id号对频道列表排序
res_list_sorted = sorted(res_list, key = lambda item: int(item['id']))
# pprint(res_list_sorted)

fp.close()

# 连接数据库
db_uri = "mongodb://pornhuber:lsn1990312?@localhost:27017/pornhub?authMechanism=SCRAM-SHA-1"

client = MongoClient(db_uri)
pornhub_db = client['pornhub']

# 将频道目录信息存入数据库
categories_col = pornhub_db['categories']
categories_col.insert_many(res_list_sorted)

# 获取所有频道的页码总数
cate_page_info = []

for i in res_list_sorted:
    tmp_info = {}
    tmp_info['title'] = i['title']
    tmp_info['url'] = i['href']
    
	# 以下几个频道根url为特殊形式
    if i['title'] in ['Babe', 'Pornstar', 'Hentai', 'Teen', 'HD Porn', 'Gay', 'College', 'Shemale', 'Virtual Reality', 'Interactive', 'Described Video']:
        page_url = i['href'] + '?page=2'
    else:
        page_url = i['href'] + '&page=2'
        
    tmp_content = s.get(url=page_url).content
    tmp_res = BeautifulSoup(tmp_content, 'lxml')
    
    pagination = int(tmp_res.find('div', class_='pagination3').find_all('li')[-2].text)
    tmp_info['page'] = pagination    
    
    # 缓存频道总页数信息
    cate_page_info.append(tmp_info)

# 循环获取每个频道下所有页面的全部视频简介信息，包括题目、url、封面url、观看总数、评分、上传时间
for cate_item in cate_page_info:    

    category_title = cate_item['title']
    pagination = cate_item['page']
    base_url =  cate_item['url']
    
    new_collection = pornhub_db[category_title]
    total = 0
    for page in range(1, pagination):
        
        page_url = base_url + '&page=' + str(page)

        tmp_content = s.get(url=page_url).content
        tmp_res = BeautifulSoup(tmp_content, 'lxml')

        video_boxes = tmp_res.find_all('div', class_='phimage')    

        for i in video_boxes:
            tmp = {}
            tmp['title'] = i.find('span', class_='title').text
            tmp['url'] = 'https://www.pornhub.com' + i.find('span', class_='title').find('a')['href']
            tmp['cover_url'] = i.find('a', class_='img').find('img')['data-path']    
            tmp['views'] = int(i.find('span', class_='views').find('var').text.replace(',', ''))
            tmp['rating'] = float(i.find('div', class_='value').text.replace('%', ''))/100
            tmp['upload_time'] = i.find('var', class_='added').text
            
            total += 1
            new_collection.insert_one(tmp)
#         print('current  page: {0}'.format(page))

    print('{0} Done! Total Pages: {1}, Total Videoes: {2}'.format(category_title, pagination,  total))