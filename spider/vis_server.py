from flask import *
from flask_cors import *
from redis import Redis
import get_film_id
import get_all_info
import threading
import time
import inspect
import ctypes

app = Flask(__name__)
CORS(app, supports_credentials=True)


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res_ = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res_ == 0:
        # raise ValueError("invalid thread id")
        pass
    elif res_ != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        # raise SystemError("PyThreadState_SetAsyncExc failed")
        pass


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


def test():
    while True:
        print('-------')
        time.sleep(0.5)


def my_start():
    get_film_id.get_film_id()


@app.route('/')
def index():
    response = make_response("hello world")
    return response


@app.route('/ms', methods=['GET'])
def ms():

    response = make_response(str(redis.lpop("ms")))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/s1', methods=['GET'])
def s1():
    response = make_response(str(redis.lpop("s1")))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/s2', methods=['GET'])
def s2():
    response = make_response(str(redis.lpop("s2")))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/res', methods=['GET'])
def res():
    response = make_response(str(redis.lpop("res")))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/start', methods=['GET'])
def start():
    global threads
    # 开启线程，将线程id存入数据库中

    # 先清理一遍输出
    while redis.lpop("ms") is not None:
        pass
    while redis.lpop("s1") is not None:
        pass
    while redis.lpop("s2") is not None:
        pass
    while redis.lpop("res") is not None:
        pass

    # mster
    t1 = threading.Thread(target=get_film_id.get_film_id)
    threads.append(t1)
    t1.start()

    # slave1
    t2 = threading.Thread(target=get_all_info.start, args=("s1",))
    threads.append(t2)
    t2.start()

    # slave2
    t3 = threading.Thread(target=get_all_info.start, args=("s2",))
    threads.append(t3)
    t3.start()

    response = make_response("")
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/stop', methods=['GET'])
def stop():
    global threads
    # 从redis中读取线程id，全部关掉
    for t in threads:
        stop_thread(t)

    response = make_response("")
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':

    threads = []

    redis = Redis.from_url("redis://:fxb_fh@120.24.1.93:6379", decode_responses=True)
    # start()
    # 开始监听
    app.run(host='0.0.0.0', port=32222)
