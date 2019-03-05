from flask import *
from flask_cors import *
import json
import requests
import re
import threading
from redis import Redis
import get_film_id
import get_all_info


app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/myapi', methods=['GET', 'POST'])
def myapi():
    if request.method == 'POST':

        req = request.get_data().decode("utf-8")
        datax = json.loads(req)

    response = make_response("")
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/')
def index():
    response = make_response("hello world")
    return response

# 这里取
@app.route('/ms', methods=['GET', 'POST'])
def ms():

    # 从队列里面取一个元素
    print(redis.lpop("ms"))

    response = make_response("")
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


def send_msg(msg, mtype, uid):
    s = requests.Session()
    url = "http://127.0.0.1:5700/send_msg"

    data = {
        "message_type": mtype,
        "user_id": uid,
        "group_id": uid,
        "message": msg,
        "auto_escape": "false"
    }

    s.post(url, data=data)
    s.close()


if __name__ == '__main__':

    redis = Redis.from_url("redis://:fxb_fh@120.24.1.93:6379", decode_responses=True)

    # 开始监听
    app.run(host='0.0.0.0', port=32222)
