# -*- coding: utf-8 -*-
# @Time         : 2017/12/6 17:09
# @Author       : Huaiz
# @Email        : Apokar@163.com
# @File         : tyc_baseinfo.py
# @Software     : PyCharm Community Edition
# @PROJECT_NAME : new_tyc

import csv
import sys
import urllib
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')

import urllib3

urllib3.disable_warnings()

import re
import time
import requests
import threading
import random
import datetime
import MySQLdb


# 代理部分
def get_proxy():
    proxies = list(set(requests.get(
        "http://60.205.92.109/api.do?name=3E30E00CFEDCD468E6862270F5E728AF&status=1&type=static").text.split('\n')))
    return proxies


def get_parse(url):
    headers = {
        'Cookie': 'TYCID=8c420960894b11e79bb7cf4adc554d53; uccid=baeee58fe4d1d697092e61f6525e8719; ssuid=6805162414; aliyungf_tc=AQAAAOsOUQId4QcAlaRf3mqAPMUDMG/2; csrfToken=S2nttCpDrr4WCbvLkQRClEUt; bannerFlag=true; _csrf=i6MDX6NEr+KEpAxRAcWeaA==; OA=cxAohDKsDZv4yk4sQ70GtLb5KtPEhEnIp/d25AgGeuU=; _csrf_bk=76b9aab25bdab0db8930d22ee4171984; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1503634325,1504143041,1504148840,1504245847; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1504490343',
        'Host': 'www.tianyancha.com',
        'Referer': 'https://www.tianyancha.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla / 5.0(Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }
    while True:
        try:
            index = random.randint(1, len(proxies) - 1)
            proxy = {"http": "http://" + str(proxies[index]), "https": "http://" + str(proxies[index])}
            print 'Now Proxy is : ' + str(proxy) + ' @ ' + str(datetime.datetime.now())
            response = requests.get(url, timeout=5, headers=headers, proxies=proxy)
            if response.status_code == 200:
                return response
                # return response
                break
            else:
                return None
                break
        except Exception, e:

            print e
            if str(e).find('HTTPSConnectionPool') >= 0:
                time.sleep(3)
                continue
            elif str(e).find('HTTPConnectionPool') >= 0:
                time.sleep(3)
                continue
            else:
                return None
                break


# 正 则
def re_findall(pattern, html):
    if re.findall(pattern, html):
        return re.findall(pattern, html)
    else:
        return 'N'


# 清理数据
def detag(html):
    detag = re.subn('<[^>]*>', ' ', html)[0]
    detag = re.subn('\\\\u\w{4}', ' ', detag)[0]
    detag = detag.replace('{', '')
    detag = detag.replace('}', '')
    detag = detag.replace('&nbsp;', '')
    detag = detag.replace(' ', '')
    detag = detag.replace('\n', '')
    detag = detag.replace('\t', '')
    return detag


# 获得中文
def get_chinese(str):
    b = re.compile(u"[\u4e00-\u9fa5]*")
    c = "".join(b.findall(str.decode('utf8')))
    return c


def get_info(id):
    url = 'https://www.tianyancha.com/company/' + str(id)
    # url ='https://www.tianyancha.com/company/31757870'

    while True:
        try:
            print 'parsing url:  '+url
            content = get_parse(url)
            # print content.text
            if content.text.__contains__('https://static.tianyancha.com/wap/images/notFound.png'):
                print u'nofound.img'
                break
            elif content.text.__contains__('<title>天眼查-人人都在用企业信息调查工具_企业信息查询_公司查询_工商查询_信用查询平台</title>'):
                print '解析失败 重试'
                continue
            else:
                conn = MySQLdb.connect(host="139.198.189.129", port=20009, user="root", passwd="somao1129",
                                       db="tianyancha",
                                       charset="utf8")
                cursor = conn.cursor()

                corp_name = \
                    re_findall(
                        '<span class="f18 in-block vertival-middle sec-c2" style="font-weight: 600">(.*?)</span>',
                        str(content.text))[
                        0]

                print corp_name
                phone = re_findall('<span class="sec-c3">电话：</span><span>(.*?)</span>', str(content.text))[0]
                print phone
                email = re_findall('class="in-block vertical-top overflow-width emailWidth">(.*?)</span></div>',
                                   str(content.text))[0]
                print email

                website = re_findall('class="c9 .*?">(.*?)</a></div><div class="in-block vertical-top"', str(content.text))[0]
                print website

                address = \
                re_findall('title=".*?">(.*?)</span><span class="tic tic-fujin c9"></span>', str(content.text))[0]
                print address

                cursor.execute(
                    'insert into tyc_baseinfo values ("%s","%s","%s","%s","%s","%s","%s","%s")' %
                    (
                        url,
                        corp_name,
                        phone,
                        email,
                        website,
                        address,

                        str(datetime.datetime.now()),
                        str(datetime.datetime.now())[:10]
                    )

                )
                conn.commit()
                print '__插入成功__  _@_ ' + str(datetime.datetime.now())
                break
        except Exception, e:
            print str(e)
            break

if __name__ == '__main__':
    proxies = get_proxy()
    conn = MySQLdb.connect(host="139.198.189.129", port=20009, user="root", passwd="somao1129", db="tianyancha",
                           charset="utf8")
    cursor = conn.cursor()

    cursor.execute('select corp_id from tyc_business_info')
    corp_ids = []
    ids = cursor.fetchall()
    for y in range(0, len(ids)):
        corp_ids.append(ids[y][0])
    print '获取id   ID ready '

    cursor.execute('select corp_url from tyc_baseinfo')
    old_ids = []
    oid = cursor.fetchall()
    cursor.close()
    conn.close()
    for y in range(0, len(oid)):
        old_ids.append(ids[y][0])
    print '获取old_id    OLD_ID ready '

    real_ids = []

    for id in corp_ids:
        if id not in old_ids:
            real_ids.append(id)


    start_no = 0
    end_no = len(real_ids)
    thread_num = 5
    while start_no < (end_no - thread_num + 1):
        threads = []

        for inner_index in range(0, thread_num):
            threads.append(threading.Thread(target=get_info, args=(real_ids[start_no + inner_index],)))
        for t in threads:
            t.setDaemon(True)
            t.start()
        t.join()
        start_no += thread_num
