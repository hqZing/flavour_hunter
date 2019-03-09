import os
import xml.dom.minidom as xmldom
from fontTools.ttLib import TTFont
import operator
from lxml import etree
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import requests
import re
import hashlib
from redis import Redis
import time

# 爬虫页专用，不会真正写入Hbase


def to_md5(arg_str):
    hs = hashlib.md5()
    hs.update(bytes(arg_str, encoding='utf-8'))
    return hs.hexdigest()


def to_byte(num):
    return str(num).encode('utf-8')


def get_portrait_page(url):
    try:
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'
        }
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


# 判断缺失值
def exist_null(soup):
    a = soup.select('.stackcolumn-bar').__len__() == 0
    b = soup.select('.bar-group g').__len__() == 0
    c = soup.select('.stackcolumn-bar').__len__() == 0
    d = soup.select('.linebars-value').__len__() == 0

    if a or b or c or d:
        return True
    else:
        return False


# 此函数用于解决猫眼字体反爬问题，传入soup和selector，利用beautifulsoup抓取并返回网页所需要的数字
def proc_font(soup, selector):
    titles = soup.select(selector)
    wotfs = soup.select('head > style')

    wotflist = str(wotfs[0]).split('\n')
    maoyanwotf = wotflist[5].replace(' ', '').replace('url(\'//', '').replace('format(\'woff\');', '').replace(
        '\')', '')

    r = requests.get('http://' + maoyanwotf)
    with open("demo.woff", "wb") as code:
        code.write(r.content)
    font = TTFont("demo.woff")
    font.saveXML('to.xml')

    # 加载字体模板
    num = [8, 6, 2, 1, 4, 3, 0, 9, 5, 7]
    data = []
    new_font = []
    xmlfilepath_temp = os.path.abspath("temp.xml")
    domobj_temp = xmldom.parse(xmlfilepath_temp)
    elementobj_temp = domobj_temp.documentElement
    subElementObj = elementobj_temp.getElementsByTagName("TTGlyph")
    for i in range(len(subElementObj)):
        rereobj = re.compile(r"name=\"(.*)\"")
        find_list = rereobj.findall(str(subElementObj[i].toprettyxml()))
        data.append(str(subElementObj[i].toprettyxml()).replace(find_list[0], '').replace("\n", ''))

    # 根据字体模板解码本次请求下载的字体
    xmlfilepath_find = os.path.abspath("to.xml")
    domobj_find = xmldom.parse(xmlfilepath_find)
    elementobj_find = domobj_find.documentElement
    tunicode = elementobj_find.getElementsByTagName("TTGlyph")
    for i in range(len(tunicode)):
        th = tunicode[i].toprettyxml()
        report = re.compile(r"name=\"(.*)\"")
        find_this = report.findall(th)
        get_code = th.replace(find_this[0], '').replace("\n", '')
        for j in range(len(data)):
            if operator.eq(get_code, data[j]):
                new_font.append(num[j])

    font = TTFont("demo.woff")
    font_list = font.getGlyphNames()
    font_list.remove('glyph00000')
    font_list.remove('x')

    # 匹配
    star_woff = re.findall(re.compile(r">(.*)<"), str(titles[0]))[0].split(';')
    k = 0  # 用于记录小数点的位置，匹配的时候需要把小数点去掉
    data = ''  # 用于保存数字，因为原本函数只能一个字一个字输出，我将其变成字符串拼接起来了
    for i in star_woff:
        k = k + 1
        getthis = i.upper()
        for j in range(len(font_list)):
            if operator.eq(getthis.replace(".", ""), font_list[j].replace("uni", "")):
                data = data + str(new_font[j])
        if operator.eq(k, ((re.findall(re.compile(r">(.*)<"), str(titles[0]))[0].find('.')) / 5)):
            data = data + '.'
    return data


# 处理用户画像页
def parse_portrait_page(html):
    result = {}
    soup = BeautifulSoup(str(html), 'lxml')

    if exist_null(soup):
        return None

    name = soup.select('#pageData')
    name = re.findall('movieName":"(.*?)"', str(name), re.S)
    result['n'] = str(name).replace("['", "").replace("']", "")

    for sex in soup.select('.stackcolumn-bar')[:1]:
        result['m'] = round(float(sex.attrs['style'].replace("width: ", "").replace('%', '')) / 100, 3)
    for sex in soup.select('.stackcolumn-bar')[1:2]:
        result['fm'] = round(float(sex.attrs['style'].replace("width: ", "").replace('%', '')) / 100, 3)

    for age in soup.select('.bar-group g')[:1]:
        result['un20'] = round(float(age.get_text().replace('%', '')) / 100, 3)
    for age in soup.select('.bar-group g')[1:2]:
        result['20to24'] = round(float(age.get_text().replace('%', '')) / 100, 3)
    for age in soup.select('.bar-group g')[2:3]:
        result['25to29'] = round(float(age.get_text().replace('%', '')) / 100, 3)
    for age in soup.select('.bar-group g')[3:4]:
        result['30to34'] = round(float(age.get_text().replace('%', '')) / 100, 3)
    for age in soup.select('.bar-group g')[4:5]:
        result['35to39'] = round(float(age.get_text().replace('%', '')) / 100, 3)
    for age in soup.select('.bar-group g')[5:6]:
        result['ab40'] = round(float(age.get_text().replace('%', '')) / 100, 3)

    for edu in soup.select('.stackcolumn-bar')[2:3]:
        result['dg_h'] = round(float(edu.attrs['style'].replace("width: ", "").replace("%", "")) / 100, 3)
    for edu in soup.select('.stackcolumn-bar')[3:]:
        result['dg_l'] = round(float(edu.attrs['style'].replace("width: ", "").replace("%", "")) / 100, 3)

    for area in soup.select('.linebars-value')[3:]:
        result['ct1'] = round(float(area.get_text().replace("%", "")) / 100, 3)
    for area in soup.select('.linebars-value')[:1]:
        result['ct2'] = round(float(area.get_text().replace("%", "")) / 100, 3)
    for area in soup.select('.linebars-value')[2:3]:
        result['ct3'] = round(float(area.get_text().replace("%", "")) / 100, 3)
    for area in soup.select('.linebars-value')[1:2]:
        result['ct4'] = round(float(area.get_text().replace("%", "")) / 100, 3)

    try:
        for occupation in soup.select('.pie-label-line text')[:3]:
            result[occupation.get_text()[:2]] = round(float(occupation.get_text()[2:].replace("%", "")) / 100, 2)

        result['oc_w'] = result.pop('白领')
        result['oc_o'] = result.pop('其他')
        result['oc_s'] = result.pop('学生')
    except KeyError:
        return None

    try:
        for preference in soup.select('.pie-label-line text')[3:]:
            result[preference.get_text()[:2]] = round(float(preference.get_text()[2:].replace("%", "")) / 100, 2)

        result['pf_ac'] = result.pop("动作")
        result['pf_co'] = result.pop("喜剧")
        result['pf_ro'] = result.pop("爱情")
        result['pf_sc'] = result.pop("科幻")
        result['pf_an'] = result.pop("动画")
    except KeyError:
        return None

    return result


# 处理电影信息页
def parse_info_page(soup, html):
    result = {}
    try:
        # 片名
        item1 = soup.select('body > div.banner > div > div.celeInfo-right.clearfix > '
                            'div.movie-brief-container > h3')
        result["n"] = item1[0].string

    except:
        return None

    try:
        # 导演
        item2 = soup.select('.info .name')
        result["dr"] = item2[0].string.replace("\n", "").replace(" ", "")
    except:
        return None

    try:
        # 主演
        item2 = soup.select('.info .name')
        result["a1"] = item2[1].string.replace("\n", "").replace(" ", "")
        result["a2"] = item2[2].string.replace("\n", "").replace(" ", "")
        result["a3"] = item2[3].string.replace("\n", "").replace(" ", "")
        result["a4"] = item2[4].string.replace("\n", "").replace(" ", "")
    except:
        return None

    try:
        #类别
        item3 = soup.select('body > div.banner > div > div.celeInfo-right.clearfix >'
                            ' div.movie-brief-container > ul > li:nth-child(1)')
        dict_temp1 = {
            "爱情": "t_aq",
            "喜剧": "t_xj",
            "动画": "t_dh",
            "剧情": "t_jq",
            "恐怖": "t_kb",
            "惊悚": "t_js",
            "科幻": "t_kh",
            "动作": "t_dz",
            "悬疑": "t_xy",
            "犯罪": "t_fz",
            "冒险": "t_mx",
            "战争": "t_zz",
            "奇幻": "t_qh",
            "运动": "t_yd",
            "家庭": "t_jt",
            "古装": "t_gz",
            "武侠": "t_wx",
            "西部": "t_xb",
            "历史": "t_ls",
            "传记": "t_zj",
            "歌舞": "t_gw",
            "黑色电影": "t_hs",
            "短片": "t_dp",
            "纪录片": "t_jl",
            "其他": "t_qt",
        }
        dict_temp2 = {
            "t_aq": 0,
            "t_xj": 0,
            "t_dh": 0,
            "t_jq": 0,
            "t_kb": 0,
            "t_js": 0,
            "t_kh": 0,
            "t_dz": 0,
            "t_xy": 0,
            "t_fz": 0,
            "t_mx": 0,
            "t_zz": 0,
            "t_qh": 0,
            "t_yd": 0,
            "t_jt": 0,
            "t_gz": 0,
            "t_wx": 0,
            "t_xb": 0,
            "t_ls": 0,
            "t_zj": 0,
            "t_gw": 0,
            "t_hs": 0,
            "t_dp": 0,
            "t_jl": 0,
            "t_qt": 0
        }
        cls = item3[0].string.replace("\n", "").replace(" ", "").split(",")
        for c in cls:
            dict_temp2[dict_temp1[c]] = 1
        result.update(dict_temp2)
    except:
        return None

    try:
        # 地区/时长
        item4 = soup.select('body > div.banner > div > div.celeInfo-right.clearfix >'
                            ' div.movie-brief-container > ul > li:nth-child(2)')
        dict_temp1 = {
            "大陆": "c_dl",
            "美国": "c_mg",
            "韩国": "c_hg",
            "日本": "c_rb",
            "香港": "c_xg",
            "台湾": "c_tw",
            "泰国": "c_tg",
            "印度": "c_yd",
            "法国": "c_fg",
            "英国": "c_yg",
            "俄罗斯": "c_els",
            "意大利": "c_ydl",
            "西班牙": "c_xby",
            "德国": "c_dg",
            "波兰": "c_bl",
            "澳大利亚": "c_ad",
            "伊朗": "c_yl",
            "其他": "c_qt"
        }
        dict_temp2 = {
            "c_dl": 0,
            "c_mg": 0,
            "c_hg": 0,
            "c_rb": 0,
            "c_xg": 0,
            "c_tw": 0,
            "c_tg": 0,
            "c_yd": 0,
            "c_fg": 0,
            "c_yg": 0,
            "c_els": 0,
            "c_ydl": 0,
            "c_xby": 0,
            "c_dg": 0,
            "c_bl": 0,
            "c_ad": 0,
            "c_yl": 0,
            "c_qt": 0,
        }

        country_and_len = item4[0].string.replace("\n", "").replace(" ", "")

        # 国家地区
        countrys = country_and_len.split("/")[0].split(",")
        for e in countrys:
            dict_temp2[dict_temp1[e]] = 1
        result.update(dict_temp2)

        # 电影时长
        result["len"] = country_and_len.split("/")[1].replace("分钟", "")
    except :
        return None

    try:
        # 上映时间
        item5 = soup.select('body > div.banner > div > div.celeInfo-right.clearfix >'
                            ' div.movie-brief-container > ul > li:nth-child(3)')
        result["da"] = item5[0].string.replace("\n", "").replace(" ", "")[:10]
    except:
        return None

    try:
        # 评分
        item6 = proc_font(soup, 'body > div.banner > div > div.celeInfo-right.clearfix >'
                               ' div.movie-stats-container > div:nth-child(1) > div > span > span')
        result["sc"] = item6
    except:
        return None

    try:
        # 评分人数
        item7 = proc_font(soup, 'body > div.banner > div > div.celeInfo-right.clearfix >'
                               ' div.movie-stats-container > div:nth-child(1) > div > div > span > span')
        if operator.eq('万', "".join(re.findall(r'[\u4e00-\u9fa5]+', str(soup.select('.stonefont')), re.S))):
            item7 = float(item7)*10000
        result["sc_p"] = item7
    except:
        return None

    try:
        # 累计票房
        item8 = proc_font(soup, 'body > div.banner > div > div.celeInfo-right.clearfix >'
                               ' div.movie-stats-container > div:nth-child(2) > div > span.stonefont')
        if operator.eq('万', soup.select('.unit')[0].string):
            item8 = float(item8)*10000

        if operator.eq('万美元', soup.select('.unit')[0].string):
            item8 = float(item8)*60000

        if operator.eq('亿', soup.select('.unit')[0].string):
            item8 = float(item8)*100000000

        if operator.eq('亿美元', soup.select('.unit')[0].string):
            item8 = float(item8)*600000000

        result["bof"] = item8
    except:
        return None

    return result


# 得到用户画像的dict
def get_users_portrait(film_id):
    url = 'https://piaofang.maoyan.com/movie/' + str(film_id) + '/wantindex?'
    html = get_portrait_page(url)
    result = parse_portrait_page(html)
    return result


# 得到电影信息的dict
def get_film_info(film_id):
    url = 'https://maoyan.com/films/'+film_id
    header = {
        'Accept': '*/*;',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'maoyan.com',
        'Referer': 'http://maoyan.com/',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/67.0.3396.87 Safari/537.36'
    }

    db_data = requests.get(url, headers=header)
    soup = BeautifulSoup(db_data.text.replace("&#x", ""), 'lxml')
    html = etree.HTML(db_data.text)

    # 解析网页，得出dict
    result = parse_info_page(soup, html)
    return result


# 录入数据库
def write_to_hbase(result, client):

    pass


# 程序的主要入口
def start(node_name):

    # 连接redis
    redis = Redis.from_url("redis://:fxb_fh@120.24.1.93:6379", decode_responses=True)

    # 在不同服务器运行的时候更改一下这个节点名字，用来区分不同的爬虫从机
    # 从机1设置为s1，从机2设置为s2
    # node_name = "s1"

    # 依旧要先清空redis的队列
    while redis.lpop(node_name) is not None:
        pass
    while redis.lpop("res") is not None:
        pass

    # 从redis中领取爬虫任务
    while 1:

        # 如果任务列表为空,就放弃领取

        f_id = redis.lpop("film_id")
        if f_id is None:
            continue
        print(node_name, "领取到一个任务")

        # 若领取了任务，则更新到爬虫页中
        redis.lpush(node_name, node_name + " 领取到一个任务：" + f_id)

        # 领取到任务,拿去处理
        dict_users_portrait = get_users_portrait(f_id)
        dict_film_info = get_film_info(f_id)
        time.sleep(0.1)

        # 如果这部电影在用户画像站和猫眼主站都有信息，那么就算是完美的数据了，可以直接存数据库拿去分析
        if (dict_users_portrait is not None) and (dict_film_info is not None):
            result = {}
            result.update(dict_users_portrait)
            result.update(dict_film_info)

            # 输出到redis，以代替写入hbase
            print(result)
            redis.lpush(node_name, "经过清洗判断，%s数据合格，录入Hbase中，电影名为：%s" % (f_id, result["n"]))
            redis.lpush("res", str(dict_film_info))
        else:
            redis.lpush(node_name, "经过清洗判断，%s数据不合格，放弃录入" % f_id)


if __name__ == '__main__':

    # 程序入口
    start("s1")
