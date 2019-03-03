#本代码用于获取猫眼电影的编码
import requests
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
from urllib.error import HTTPError
from requests.exceptions import RequestException
import time

id = []
for yearid in [11,12,13,14,100]:
    for offset in range(0,1980,30):
        url = 'https://maoyan.com/films?showType=3&sortId=1&yearId='+str(yearid)+'&offset='+str(offset)
        time.sleep(1)
        header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'}
        html = requests.get(url,headers = header)
        soup = BeautifulSoup(str(html.text),'lxml')
        items = soup.select('.channel-detail a')
        for a in soup.select('.channel-detail a'):
            id.append(a['data-val'].replace("{movieId:","").replace("}",""))
            #print(id)
print(id)

with open('2016id.txt','a',encoding='utf-8') as file:
    file.write('\n'.join(id))
