# -*- coding: utf-8 -*-
import os
import re
import xml.dom.minidom as xmldom
from bs4 import BeautifulSoup
import requests
from fontTools.ttLib import TTFont
import operator
from lxml import etree
import csv
import threading
import time


# 此函数用于解决猫眼字体反爬问题，传入soup和selector，利用beautifulsoup抓取并返回网页所需要的数字
def get_data(soup, selector):
    titles = soup.select(selector)
    wotfs = soup.select('head > style')

    wotflist = str(wotfs[0]).split('\n')
    maoyanwotf = wotflist[5].replace(' ', '').replace('url(\'//', '').replace('format(\'woff\');', '').replace('\')',   '')

    r = requests.get('http://'+maoyanwotf)
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
        data.append(str(subElementObj[i].toprettyxml()).replace(find_list[0],'').replace("\n",''))

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
            if operator.eq(get_code,data[j]):
                new_font.append(num[j])

    font = TTFont("demo.woff")
    font_list = font.getGlyphNames()
    font_list.remove('glyph00000')
    font_list.remove('x')

    # 匹配
    star_woff = re.findall(re.compile(r">(.*)<"), str(titles[0]))[0].split(';')
    k = 0 #用于记录小数点的位置，匹配的时候需要把小数点去掉
    data = ''#用于保存数字，因为原本函数只能一个字一个字输出，我将其变成字符串拼接起来了
    for i in star_woff:
        k = k+1
        getthis = i.upper()
        for j in range(len(font_list)):
            if operator.eq(getthis.replace(".", ""),font_list[j].replace("uni", "")):
                data = data + str(new_font[j])
        if operator.eq(k,((re.findall(re.compile(r">(.*)<"), str(titles[0]))[0].find('.'))/5)):
             data = data + '.'
    return data

def parse_one_page(soup,html):
    result = {}
    try:
        # 片名
        item1 = soup.select('body > div.banner > div > div.celeInfo-right.clearfix > div.movie-brief-container > h3')
        # result.append(item1[0].string)
        result["n"] = item1[0].string
        print(item1[0].string)
    except:
        return None

    try:    
        # 导演
        item2 = soup.select('.info .name')
        # result.append(item2[0].string.replace("\n", "").replace(" ", ""))
        result["dr"] = item2[0].string.replace("\n", "").replace(" ", "")
    except:
        return None

    try:
        # 主演
        item2 = soup.select('.info .name')
        # result.append(item2[1].string.replace("\n","").replace(" ",""))
        # result.append(item2[2].string.replace("\n","").replace(" ",""))
        # result.append(item2[3].string.replace("\n","").replace(" ",""))
        # result.append(item2[4].string.replace("\n","").replace(" ",""))
        result["a1"] = item2[1].string.replace("\n", "").replace(" ", "")
        result["a2"] = item2[2].string.replace("\n", "").replace(" ", "")
        result["a3"] = item2[3].string.replace("\n", "").replace(" ", "")
        result["a4"] = item2[4].string.replace("\n", "").replace(" ", "")
    except:
        return None

    try:
        #类别
        item3 = soup.select('body > div.banner > div > div.celeInfo-right.clearfix > div.movie-brief-container > ul > li:nth-child(1)')
        # result.append(item3[0].string.replace("\n","").replace(" ",""))
        dict_temp = {
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
        # print(cls)
        for c in cls:
            dict_temp2[dict_temp[c]] = 1
        result.update(dict_temp2)
    except:
        return None



    try:
        #地区/时长
        item4 = soup.select('body > div.banner > div > div.celeInfo-right.clearfix > div.movie-brief-container > ul > li:nth-child(2)')
        # result.append()
        dict_temp = {
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
        print(country_and_len)

        # 国家地区列表
        countrys = country_and_len.split("/")[0].split(",")
        for e in countrys:
            dict_temp2[dict_temp[e]] = 1
        result.update(dict_temp2)

        # 电影时长
        result["len"] = country_and_len.split("/")[1].replace("分钟", "")
    except :
        return None

    try:
        #上映时间
        item5 = soup.select('body > div.banner > div > div.celeInfo-right.clearfix > div.movie-brief-container > ul > li:nth-child(3)')
        result["da"] = item5[0].string.replace("\n", "").replace(" ", "")[:10]
    except:
        return None


    try:
        #评分
        item6 = get_data(soup,'body > div.banner > div > div.celeInfo-right.clearfix > div.movie-stats-container > div:nth-child(1) > div > span > span')
        result.append(item6)
    except:
        result.append(None)
        return result

'''
    try:
        #评分人数
        item7 = get_data(soup,'body > div.banner > div > div.celeInfo-right.clearfix > div.movie-stats-container > div:nth-child(1) > div > div > span > span')
        if operator.eq('万', "".join(re.findall(r'[\u4e00-\u9fa5]+',str(soup.select('.stonefont')),re.S))):
            item7 = float(item7)*10000
        result.append(item7)
    except:
        result.append(None)

    try:
        #累计票房
        item8 = get_data(soup,'body > div.banner > div > div.celeInfo-right.clearfix > div.movie-stats-container > div:nth-child(2) > div > span.stonefont')
        if operator.eq('万',soup.select('.unit')[0].string):
            item8 = float(item8)*10000
        if operator.eq('万美元',soup.select('.unit')[0].string):
            item8 = float(item8)*60000
        if operator.eq('亿',soup.select('.unit')[0].string):
            item8 = float(item8)*100000000
        if operator.eq('亿美元',soup.select('.unit')[0].string):
            item8 = float(item8)*600000000
        result.append(item8)
        
    except:
        result.append(None)

    try:
        #剧情简介
        item9 = soup.select('#app > div > div.main-content > div > div.tab-content-container > div.tab-desc.tab-content.active > div:nth-child(1) > div.mod-content > span')
        result.append(item9[0].string.replace("\n","").replace(" ",""))
    except:
        result.append(None)

    try:
        #相关电影
        item10 = soup.select('.channel-detail a')
        result.append(item10[0].string)
        result.append(item10[1].string)
        result.append(item10[2].string)
        result.append(item10[3].string)
        result.append(item10[4].string)
        result.append(item10[5].string)
    except:
        result.append(None)

#     try:
#         #奖项
#         item11 = html.xpath('//*[@id="app"]/div/div[1]/div/div[2]/div[3]/ul/li[1]/div[1]/text()')
#         result.append(" ".join(item11).replace("\n","").replace(" ",""))
#         item11 = html.xpath('//*[@id="app"]/div/div[1]/div/div[2]/div[3]/ul/li[1]/div[2]/div/text()')
#         result.append(" ".join(item11).replace("\n","").replace(" ",""))
#     except IndexError:
#         result.append(None)

    try:
        #短评
        item12 = soup.select('.comment-content')
        result.append(" ".join('%s' %id for id in item12).replace(" ","").replace('<divclass="comment-content">',"").replace('</div>',""))
    except:
        result.append(None)
        
'''


def main(offset):    
    url = 'https://maoyan.com/films/'+offset
    header = {
        'Accept': '*/*;',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'maoyan.com',
        'Referer': 'http://maoyan.com/',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    }

    db_data = requests.get(url, headers=header)
    soup = BeautifulSoup(db_data.text.replace("&#x", ""), 'lxml')
    html = etree.HTML(db_data.text)
    # print(db_data.text)
    result = parse_one_page(soup, html)
    print(result)


if __name__=='__main__':
    for line in open("2016id.txt"):
        main(line.replace("\n", ""))
