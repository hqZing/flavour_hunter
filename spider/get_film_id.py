import requests
from bs4 import BeautifulSoup
import time
from redis import Redis

# 本代码用于获取猫眼电影的编码，存入redis中作为任务队列


redis = Redis.from_url("redis://:1234@120.24.1.93:7003", decode_responses=True)

# redis.sadd("film_id", "333")
# print(redis.spop("film_id"))
# exit()


f_id = None
for year_id in [11, 12, 13, 14, 100]:
    for offset in range(0, 1980, 30):
        url = 'https://maoyan.com/films?showType=3&sortId=1&yearId='+str(year_id)+'&offset='+str(offset)
        time.sleep(1)
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                                ' (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'}
        html = requests.get(url, headers=header)
        soup = BeautifulSoup(str(html.text), 'lxml')
        items = soup.select('.channel-detail a')
        for a in soup.select('.channel-detail a'):
            f_id = a['data-val'].replace("{movieId:", "").replace("}", "")
            redis.sadd("film_id", f_id)
            print(f_id)

print("所有任务添加完成")
