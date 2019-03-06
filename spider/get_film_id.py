import requests
from bs4 import BeautifulSoup
import time
from redis import Redis

# 本代码用于获取猫眼电影的编码，存入redis中作为任务队列


def get_film_id(**kwargs):

    redis = Redis.from_url("redis://:fxb_fh@120.24.1.93:6379", decode_responses=True)

    # redis.sadd("film_id", "6379")
    # print(redis.spop("film_id"))
    # 清空这两个列表
    while redis.lpop("film_id") is not None:
        pass

    while redis.lpop("ms") is not None:
        pass

    for year_id in [11, 12, 13, 14, 100]:
        for offset in range(0, 1980, 30):
            url = 'https://maoyan.com/films?showType=3&sortId=1&yearId='+str(year_id)+'&offset='+str(offset)
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                                    ' (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'}
            html = requests.get(url, headers=header)
            soup = BeautifulSoup(str(html.text), 'lxml')
            for a in soup.select('.channel-detail a'):
                f_id = a['data-val'].replace("{movieId:", "").replace("}", "")

                # 放入一份到任务队列
                redis.lpush("film_id", f_id)

                # 同时复制一份到ms队列用以爬虫页面展示
                redis.lpush("ms", f_id)

                print(f_id)
                time.sleep(2)

    print("所有任务添加完成")


if __name__ == "__main__":
    get_film_id()
