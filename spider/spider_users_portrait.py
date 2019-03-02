from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import requests
import re
import hashlib
from hbase.ttypes import Mutation

from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase


def to_md5(arg_str):
    hash = hashlib.md5()
    hash.update(bytes(arg_str, encoding='utf-8'))
    return hash.hexdigest()


def get_one_page(url):
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


def parse_one_page(html):
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


# 将浮点数转换成字节流，因为直接写在里面太长了，这里封装成函数
def float_to_byte(num):
    return str(num).encode('utf-8')


def write_to_hbase(result):
    global socket
    global client

    mutations = [
        Mutation(column="f:n".encode('utf-8'), value=result["n"].encode('utf-8')),

        Mutation(column="f:m".encode('utf-8'), value=float_to_byte(result["m"])),
        Mutation(column="f:fm".encode('utf-8'), value=float_to_byte(result["fm"])),

        Mutation(column="f:un20".encode('utf-8'), value=float_to_byte(result["un20"])),
        Mutation(column="f:20to24".encode('utf-8'), value=float_to_byte(result["20to24"])),
        Mutation(column="f:25to29".encode('utf-8'), value=float_to_byte(result["25to29"])),
        Mutation(column="f:30to34".encode('utf-8'), value=float_to_byte(result["30to34"])),
        Mutation(column="f:35to39".encode('utf-8'), value=float_to_byte(result["35to39"])),
        Mutation(column="f:ab40".encode('utf-8'), value=float_to_byte(result["ab40"])),

        Mutation(column="f:dg_h".encode('utf-8'), value=float_to_byte(result["dg_h"])),
        Mutation(column="f:dg_l".encode('utf-8'), value=float_to_byte(result["dg_l"])),

        Mutation(column="f:ct1".encode('utf-8'), value=float_to_byte(result["ct1"])),
        Mutation(column="f:ct2".encode('utf-8'), value=float_to_byte(result["ct2"])),
        Mutation(column="f:ct3".encode('utf-8'), value=float_to_byte(result["ct3"])),
        Mutation(column="f:ct4".encode('utf-8'), value=float_to_byte(result["ct4"])),

        Mutation(column="f:oc_w".encode('utf-8'), value=float_to_byte(result["oc_w"])),
        Mutation(column="f:oc_s".encode('utf-8'), value=float_to_byte(result["oc_s"])),
        Mutation(column="f:oc_o".encode('utf-8'), value=float_to_byte(result["oc_o"])),

        Mutation(column="f:pf_ac".encode('utf-8'), value=float_to_byte(result["pf_ac"])),
        Mutation(column="f:pf_co".encode('utf-8'), value=float_to_byte(result["pf_co"])),
        Mutation(column="f:pf_ro".encode('utf-8'), value=float_to_byte(result["pf_ro"])),
        Mutation(column="f:pf_sc".encode('utf-8'), value=float_to_byte(result["pf_sc"])),
        Mutation(column="f:pf_an".encode('utf-8'), value=float_to_byte(result["pf_an"])),

    ]

    client.mutateRow("film22".encode('utf-8'), to_md5(result["n"]).encode('utf-8'), mutations, None)

    print(result)
    print("录入完成")


def do_spider(film_id):
    url = 'https://piaofang.maoyan.com/movie/' + str(film_id) + '/wantindex?'
    html = get_one_page(url)
    result = parse_one_page(html)
    if result  != None:
        try:
            write_to_hbase(result)
        except:
            pass


def start():
    for line in open("2016id.txt"):
        do_spider(line.replace("\n", ""))


if __name__ == '__main__':

    socket = TSocket.TSocket('192.168.200.16', 9090)
    socket.setTimeout(5000)
    transport = TTransport.TBufferedTransport(socket)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = Hbase.Client(protocol)
    socket.open()

    # 程序入口
    start()
