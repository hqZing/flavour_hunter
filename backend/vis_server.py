from flask import *
from flask_cors import *
from redis import Redis
import get_film_id_vis
import get_all_info_vis
import threading
import time
import inspect
import ctypes

app = Flask(__name__)
CORS(app, supports_credentials=True)

# 程序本身的设定设定
# 请确定master节点、slave1节点、slave2节点不可开在同一个服务器的相同端口上，最好分开在不同主机上运行
# 否则爬虫可视化网页可能会出现问题


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res_ = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res_ == 0:
        pass
    elif res_ != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        pass


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


# 堵塞式操作单独开启线程，不影响web响应
def start_(node_name):

    global threads

    # 开启线程，将线程id存入数据库中
    if node_name == "ms":
        # mster节点功能特殊，进行单独的逻辑处理
        while redis.lpop("ms") is not None:
            pass                # 清理输出
        t1 = threading.Thread(target=get_film_id_vis.get_film_id)
        threads.append(t1)
        t1.start()
    else:
        # slave节点，多个节点可以重复使用该代码
        while redis.lpop(node_name) is not None:
            pass
        t2 = threading.Thread(target=get_all_info_vis.start, args=(node_name,))
        threads.append(t2)
        t2.start()


def stop_(node_name):

    global threads

    # 从redis中读取线程id，全部关掉
    for t in threads:
        stop_thread(t)
    while redis.lpop(node_name) is not None:
        pass


# 清空redis
def clear_():
    for k in redis.keys():
        while redis.lpop(k) is not None:
            pass


@app.route('/data_pop/<key>')
def data_pop(key):
    # 这里key的取值范围有 ms s1 s2 res 等，分别存储各节点的输出信息，这些变量名也可以认为是节点名字
    response = make_response(str(redis.lpop(key)))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/start/<node_name>')
def start(node_name):
    threading.Thread(target=start_, args=(node_name,)).start()
    response = make_response("")
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/stop/<node_name>')
def stop(node_name):
    threading.Thread(target=stop_, args=(node_name,)).start()
    response = make_response("")
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/clear')
def clear():
    threading.Thread(target=clear_).start()
    response = make_response("")
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':

    threads = []

    redis = Redis.from_url("redis://:fxb_fh@120.24.1.93:6379", decode_responses=True)

    app.run(host='0.0.0.0', port=32222)
