# -*- coding: utf-8 -*-
# @Time         : 2017/12/1 14:45
# @Author       : Huaiz
# @Email        : Apokar@163.com
# @File         : tianyancha_business_info.py
# @Software     : PyCharm Community Edition
# @PROJECT_NAME : new_tyc
import csv
import sys
import traceback
import urllib

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
            response = requests.get(url, timeout=19, headers=headers, proxies=proxy)
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
    if re.findall(pattern, html, re.S):
        return re.findall(pattern, html, re.S)
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

def get_keywords():
    keywords_list = []
    # with open("/Users/huaiz/PycharmProjects/new_tyc/cmpy_list_mission_tianyancha.csv", "r") as csvFile:
    #     reader = csv.reader(csvFile)
    #     for crop_name in reader:
    #         item = crop_name[0].decode('utf-8')
    #         keywords_list.append(item)
    # csvFile.close()
    conn = MySQLdb.connect(host="139.198.189.129", port=20009, user="root", passwd="somao1129",
                           db="temp", charset="utf8")
    cursor = conn.cursor()

    cursor.execute('select corp_name from cmpy_list_mission_tianyancha')
    key = cursor.fetchall()
    for x in range(0, len(key)):
        keywords_list.append(key[x][0])
    return keywords_list


def get_first_info(keyword):
    max_error = 5
    num_error = 0
    print 'keyword : ' + str(keyword)
    if keyword in old_keywords:
        print '爬过了 跳过'

    else:
        url = 'https://www.tianyancha.com/search?key=' + urllib.quote(keyword.encode('utf8')) + '&checkFrom=searchBox'

        while True:
            try:
                content_1 = get_parse(url)
                if content_1 != None:
                    # print content_1.text

                    if content_1.text.__contains__('https://static.tianyancha.com/wap/images/noResult1013.jpg'):
                        print u'nofound.img'
                        break
                    elif content_1.text.__contains__('https://m.tianyancha.com/login'):
                        state = 'need login'
                        print u'需要登录 重试一次'
                        time.sleep(2)
                        if state == 'need login':

                            num_error += 1
                            print 'num_error' ,num_error
                            if num_error == max_error:
                                print u'尝试过5次 跳过'
                                break
                            else:
                                continue
                        break
                    else:
                        conn = MySQLdb.connect(host="139.198.189.129", port=20009, user="root", passwd="somao1129",
                                               db="tianyancha", charset="utf8")
                        cursor = conn.cursor()
                        print url
                        urls_result = re.findall('<div class="search_right_item ml10"><div><a href="(.*?)"', str(content_1.text),
                                                 re.S)
                        id_list = re.findall(
                            '<div class="search_right_item ml10"><div><a href="https://www.tianyancha.com/company/(.*?)"',
                            str(content_1.text), re.S)
                        corp_name = re.findall(
                            'class="query_name sv-search-company f18 in-block vertical-middle"><span>(.*?)</span>',
                            str(content_1.text), re.S)
                        print len(urls_result)
                        for x in range(len(urls_result)):
                            print keyword
                            print urls_result[x]
                            print id_list[x]
                            print detag(corp_name[x])
                            cursor.execute(
                                'insert into tyc_prepare_info values ("%s","%s","%s","%s","%s","%s")' %
                                (
                                    keyword,
                                    urls_result[x],
                                    id_list[x],
                                    detag(corp_name[x]),

                                    str(datetime.datetime.now()),
                                    str(datetime.datetime.now())[:10]
                                )

                            )
                            conn.commit()
                            print '插入时间 _@_ ' + str(datetime.datetime.now())
                        break
                else:
                    print 'content is none'
                    break
            except Exception, e:
                # print str(e)
                if str(e).find('HTTPSConnectionPool')>=0:
                    print 'HTTPSConnectionPool'
                    continue
                else:
                    print  'ABC ' + str(e)
                    print traceback.format_exc()
                    break


if __name__ == '__main__':
    proxies = get_proxy()
    keywords_list = get_keywords()
    print keywords_list
####TEST
    conn = MySQLdb.connect(host="139.198.189.129", port=20009, user="root", passwd="somao1129",
                           db="tianyancha", charset="utf8")
    cursor = conn.cursor()

    cursor.execute('select distinct keyword from tyc_prepare_info')
    old_keywords = []
    old = cursor.fetchall()
    for y in range(0, len(old)):
        old_keywords.append(old[y][0])
    cursor.close()


    conn.close()

    thread_num = 5
    start_no = 0
    end_no = len(keywords_list)
    while start_no < (end_no - thread_num + 1):
        threads = []

        for inner_index in range(0, thread_num):
            threads.append(threading.Thread(target=get_first_info, args=(keywords_list[start_no + inner_index],)))
        for t in threads:
            t.setDaemon(True)
            t.start()
        t.join()
        start_no += thread_num

    # keywords_list=['黑鸥科技有限公司','黑莓公司','香港青山发电有限公司','马仕智才设计公司']
    # keywords_list = ['黑鸥科技有限公司']
    for keyword in keywords_list:
        get_first_info(keyword)
