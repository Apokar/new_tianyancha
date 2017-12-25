# -*- coding: utf-8 -*-
# @Time         : 2017/12/12 15:08
# @Author       : Huaiz
# @Email        : Apokar@163.com
# @File         : tianyancha_main.py
# @Software     : PyCharm Community Edition
# @PROJECT_NAME : new_tianyancha
import json
import sys
import urllib
import traceback

reload(sys)
sys.setdefaultencoding('utf8')

import urllib3
import lxml

urllib3.disable_warnings()
import os
import re
import time
import requests
import threading
import random
import datetime
import MySQLdb
from bs4 import BeautifulSoup

static_js_code = """
var ne = "2633141825201321121345332721524273528936811101916293117022304236|1831735156281312241132340102520529171363214283321272634162219930|2332353860219720155312141629130102234183691124281413251227261733|2592811262018293062732141927100364232411333831161535317211222534|9715232833130331019112512913172124126035262343627321642220185148|3316362031032192529235212215274341412306269813312817111724201835|3293412148301016132183119242311021281920736172527353261533526224|3236623313013201625221912357142415851018341117262721294332103928|2619332514511302724163415617234183291312001227928218353622321031|3111952725113022716818421512203433241091723133635282932601432216";
var base64chars = "abcdefghijklmnopqrstuvwxyz1234567890-~!";
var _0x4fec = "f9D1x1Z2o1U2f5A1a1P1i7R1u2S1m1F1,o2A1x2F1u5~j1Y2z3!p2~r3G2m8S1c1,i3E5o1~d2!y2H1e2F1b6`g4v7,p1`t7D3x5#w2~l2Z1v4Y1k4M1n1,C2e3P1r7!s6U2n2~p5X1e3#,g4`b6W1x4R1r4#!u5!#D1f2,!z4U1f4`f2R2o3!l4I1v6F1h2F1x2!,b2~u9h2K1l3X2y9#B4t1,t5H1s7D1o2#p2#z1Q3v2`j6,r1#u5#f1Z2w7!r7#j3S1";
rs_decode = function(e) {
    return ne.split("|")[e]
};
    var r = t+"";
    r = r.length > 1 ? r[1] : r;
    for (var i = rs_decode(r), o = _0x4fec.split(",")[r], a = [], s = 0, u = 0; u < o.length; u++) {
        if ("`" != o[u] && "!" != o[u] && "~" != o[u] || (a.push(i.substring(s, s + 1)), s++), "#" == o[u] && (a.push(i.substring(s, s + 1)), a.push(i.substring(s + 1, s + 3)), a.push(i.substring(s + 3, s + 4)), s += 4), o.charCodeAt(u) > 96 && o.charCodeAt(u) < 123) for (var l = o[u + 1], c = 0; c < l; c++) a.push(i.substring(s, s + 2)),
        s += 2;
        if (o.charCodeAt(u) > 64 && o.charCodeAt(u) < 91) for (var l = o[u + 1], c = 0; c < l; c++) a.push(i.substring(s, s + 1)),
        s++
    }
    rsid = a;
for (var chars = "",  i = 0; i < rsid.length; i++) chars += base64chars[rsid[i]];
for (var fxck = wtf.split(","), fxckStr = "", i = 0; i < fxck.length; i++) fxckStr += chars[fxck[i]];
var utm = fxckStr;
console.log("{\\"utm\\":\\""+utm+"\\",\\"ssuid\\":\\""+Math.round(2147483647 * Math.random()) * (new Date).getUTCMilliseconds() % 1e10+"\\"}")
phantom.exit();
"""


def execCmd(cmd):
    text = os.popen(cmd).read()
    return (text)


# 正 则
def re_findall(pattern, html):
    if re.findall(pattern, html, re.S):
        return re.findall(pattern, html, re.S)
    else:
        return 'N'


def detag(html):
    detag = re.subn('<[^>]*>', ' ', html)[0]
    detag = re.subn('\\\\u\w{4}', ' ', detag)[0]
    detag = detag.replace('{', '')
    detag = detag.replace('}', '')
    detag = detag.replace('"', '')
    detag = detag.replace(' ', '')
    detag = detag.replace('\n', '')
    detag = detag.replace('\t', '')

    return detag


def get_proxy():
    proxy_list = list(set(urllib.urlopen(
        'http://60.205.92.109/api.do?name=3E30E00CFEDCD468E6862270F5E728AF&status=1&type=static').read().split('\n')[
                          :-1]))
    index = random.randint(0, len(proxy_list) - 1)
    current_proxy = proxy_list[index]
    print "NEW PROXY:\t%s" % current_proxy
    proxies = {"http": "http://" + current_proxy, "https": "http://" + current_proxy, }
    return proxies


def get_page(url):
    headers = {
        'Cookie': 'TYCID=8c420960894b11e79bb7cf4adc554d53; uccid=baeee58fe4d1d697092e61f6525e8719; ssuid=6805162414; aliyungf_tc=AQAAAOsOUQId4QcAlaRf3mqAPMUDMG/2; csrfToken=S2nttCpDrr4WCbvLkQRClEUt; bannerFlag=true; _csrf=i6MDX6NEr+KEpAxRAcWeaA==; OA=cxAohDKsDZv4yk4sQ70GtLb5KtPEhEnIp/d25AgGeuU=; _csrf_bk=76b9aab25bdab0db8930d22ee4171984; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1503634325,1504143041,1504148840,1504245847; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1504490343',
        'Host': 'www.tianyancha.com',
        'Referer': 'https://www.tianyancha.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla / 5.0(Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }
    proxies = get_proxy()
    html = requests.get(url, proxies=proxies, timeout=10, headers=headers)
    return html


###############################################


def jingpin(url, cursor, conn):
    print u'获取竞品信息  ' + str(datetime.datetime.now())
    corp_id = url.split('/company/')[1]

    while True:
        try:
            html = get_page(url)
            # print html.text

            if html.text.__contains__('天眼查-人人都在用企业信息调查工具_企业信息查询_公司查询_工商查询_信用查询平台'):
                print 'parse error , retry'
                continue
            else:
                corp_name = re.findall(
                    '<span class="f18 in-block vertival-middle sec-c2" style="font-weight: 600">(.*?)</span>',
                    html.text)[0]
                print corp_name
                if html.text.__contains__('nav-main-companyJingpin'):
                    soup = BeautifulSoup(html.text, 'lxml')
                    num = soup.select('#nav-main-companyJingpin > span')[0].text
                    if int(num) % 10 == 0:
                        all_page_no = int(num) / 10
                    else:
                        all_page_no = int(num) / 10 + 1
                    print all_page_no

                    for i in range(1, int(all_page_no) + 1):
                        soup2 = get_cookie_by_name('jingpin', i, 10, corp_name)
                        res = soup2.select('tr')

                        for x in range(1, len(res)):
                            source = str(res[x])
                            print source
                            if source.find('href') >= 0:
                                icon = re_findall('src="(.*?)"', source)[0]
                                name = re_findall('img alt="(.*?)"', source)[0]
                                jingpin_ID = re_findall('href="https://www.tianyancha.com/company/(.*?)"', source)[0]

                                location = re_findall('span class=".*?">(.*?)</span>', source)[0]
                                current_round = re_findall('span class=".*?">(.*?)</span>', source)[1]
                                industry = re_findall('span class=".*?">(.*?)</span>', source)[2]
                                business = re_findall('span class=".*?">(.*?)</span>', source)[3]
                                create_time = re_findall('span class=".*?">(.*?)</span>', source)[4]
                                valuation = re_findall('span class=".*?">(.*?)</span>', source)[5]
                            else:
                                icon = re_findall('src="(.*?)"', source)[0]
                                name = re_findall('img alt="(.*?)"', source)[0]
                                jingpin_ID = u'not found'
                                location = re_findall('span class=".*?">(.*?)</span>', source)[1]
                                current_round = re_findall('span class=".*?">(.*?)</span>', source)[2]
                                industry = re_findall('span class=".*?">(.*?)</span>', source)[3]
                                business = re_findall('span class=".*?">(.*?)</span>', source)[4]
                                create_time = re_findall('span class=".*?">(.*?)</span>', source)[5]
                                valuation = re_findall('span class=".*?">(.*?)</span>', source)[6]
                            print icon
                            print name
                            print jingpin_ID
                            print location
                            print current_round
                            print industry
                            print business
                            print create_time
                            print valuation
                            print u'插入成功 ok !!! @__ ' + str(datetime.datetime.now())
                            cursor.execute(
                                'insert into tyc_jingpin_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                                (
                                    corp_id,
                                    corp_name,
                                    url,
                                    icon.decode('utf-8'),
                                    name.decode('utf-8'),
                                    jingpin_ID,
                                    location.decode('utf-8'),
                                    current_round.decode('utf-8'),
                                    industry.decode('utf-8'),
                                    business.decode('utf-8'),
                                    create_time.decode('utf-8'),
                                    valuation.decode('utf-8'),
                                    str(datetime.datetime.now()),
                                    str(datetime.datetime.now())[:10])
                            )
                break
        except Exception, e:
            if str(e).find('HTTPSConnectionPool') >= 0:
                print 'HTTPSConnectionPool , retry '
                continue
            elif str(e).find("OperationalError: (2006, 'MySQL server has gone away')") >= 0:
                return 'MySql error 2006 ,restart'
            elif str(e).find('2003') >= 0:
                return 'MySql error 2003 ,restart'
            else:
                print str(e)
                break


def staff(url, cursor, conn):
    print u'爬取主要人员信息  ' + str(datetime.datetime.now())
    corp_id = url.split('/company/')[1]

    while True:
        try:
            html = get_page(url)
            if html.text.__contains__('天眼查-人人都在用企业信息调查工具_企业信息查询_公司查询_工商查询_信用查询平台'):
                print 'parse error , retry'
                continue
            else:
                corp_name = re.findall(
                    '<span class="f18 in-block vertival-middle sec-c2" style="font-weight: 600">(.*?)</span>',
                    html.text)[0]
                print corp_name
                if html.text.__contains__('nav-main-staffCount'):
                    soup = BeautifulSoup(html.text, 'lxml')
                    num = soup.select('#nav-main-staffCount > span')[0].text
                    if int(num) % 20 == 0:
                        all_page_no = int(num) / 20
                    else:
                        all_page_no = int(num) / 20 + 1
                    print all_page_no

                    for i in range(1, int(all_page_no) + 1):
                        soup2 = get_cookie_by_id('staff', i, 20, corp_id)
                        # print soup2
                        res = soup2.select('div.staffinfo-module-container')
                        for x in range(len(res)):
                            source = str(res[x])
                            print source
                            position = re_findall('f9f9f9;"><span>(.*?)</span></div>', source)[0]
                            print detag(position)
                            name = re_findall('target="_blank">(.*?)</a><div class="in-block', source)[0]
                            print name
                            ID = re_findall('"企业详情-主要人员" href="(.*?)"', source)[0]
                            print ID
                            cursor.execute(
                                'insert into tyc_staff_info values ("%s","%s","%s","%s","%s","%s","%s","%s")' %
                                (url,
                                 corp_name,
                                 corp_id,

                                 detag(position),
                                 name,
                                 ID,

                                 str(datetime.datetime.now()),
                                 str(datetime.datetime.now())[:10])
                            )
            break

        except Exception, e:
            if str(e).find('HTTPSConnectionPool') >= 0:
                print 'HTTPSConnectionPool , retry '
                continue
            elif str(e).find("OperationalError: (2006, 'MySQL server has gone away')") >= 0:
                return 'MySql error 2006 ,restart'
            elif str(e).find('2003') >= 0:
                return 'MySql error 2003 ,restart'
            else:
                print str(e)
                break


def shareholder(url, cursor, conn):
    print u'爬取股东信息  ' + str(datetime.datetime.now())
    corp_id = url.split('/company/')[1]
    while True:
        try:
            html = get_page(url)
            if html.text.__contains__('天眼查-人人都在用企业信息调查工具_企业信息查询_公司查询_工商查询_信用查询平台'):
                print 'parse error , retry'
                continue
            else:
                corp_name = re.findall(
                    '<span class="f18 in-block vertival-middle sec-c2" style="font-weight: 600">(.*?)</span>',
                    html.text)[0]
                print corp_name
            if html.text.__contains__('nav-main-holderCount'):
                soup = BeautifulSoup(html.text, 'lxml')
                num = soup.select('#nav-main-holderCount > span')[0].text
                if int(num) % 10 == 0:
                    all_page_no = int(num) / 10
                else:
                    all_page_no = int(num) / 10 + 1
                print all_page_no
                for i in range(1, int(all_page_no) + 1):
                    soup2 = get_cookie_by_id('holder', i, 20, corp_id)
                    print soup2
                    res = soup2.select('tr')
                    for x in range(1, len(res)):
                        source = str(res[x])

                        shareholder = re.findall('title="(.*?)"', source)[0]
                        ratio = re.findall('<span class="c-money-y">(.*?)</span>', source)[0]
                        value = re.findall('<span class="">(.*?)</span>', source)[0]
                        print shareholder
                        print ratio
                        print value
                        cursor.execute(
                            'insert into tyc_shareholder_info values ("%s","%s","%s","%s","%s","%s","%s","%s")' %
                            (url,
                             corp_name,
                             corp_id,
                             shareholder,
                             ratio,
                             value,

                             str(datetime.datetime.now()),
                             str(datetime.datetime.now())[:10])
                        )
            break
        except Exception, e:
            if str(e).find('HTTPSConnectionPool') >= 0:
                print 'HTTPSConnectionPool , retry '
                continue
            elif str(e).find("OperationalError: (2006, 'MySQL server has gone away')") >= 0:
                return 'MySql error 2006 ,restart'
            elif str(e).find('2003') >= 0:
                return 'MySql error 2003 ,restart'
            else:
                print str(e)
                break


def out_invest(url, cursor, conn):
    print u'爬取对外投资信息  ' + str(datetime.datetime.now())
    corp_id = url.split('/company/')[1]

    while True:
        try:
            html = get_page(url)
            if html.text.__contains__('天眼查-人人都在用企业信息调查工具_企业信息查询_公司查询_工商查询_信用查询平台'):
                print 'parse error , retry'
                continue
            else:
                corp_name = re.findall(
                    '<span class="f18 in-block vertival-middle sec-c2" style="font-weight: 600">(.*?)</span>',
                    html.text)[0]
                print corp_name
                if html.text.__contains__('nav-main-inverst'):
                    soup = BeautifulSoup(html.text, 'lxml')
                    num = soup.select('#nav-main-inverstCount > span')[0].text
                    if int(num) % 20 == 0:
                        all_page_no = int(num) / 20
                    else:
                        all_page_no = int(num) / 20 + 1
                    print all_page_no

                    for i in range(1, int(all_page_no) + 1):
                        soup2 = get_cookie_by_id('invest', i, 20, corp_id)
                        res = soup2.select('tr')
                        for x in range(len(res)):
                            source = str(res[x])
                            print source
                        invested_person = re_findall('title="(.*?)"', source)
                        span_part = re_findall('<span class=".*?">(.*?)</span>', source)
                        print span_part[0]  # 被投资企业名称
                        print invested_person[0]  # 被投资法定代表人
                        print span_part[2]  # 注册资本
                        print span_part[3]  # 投资数额
                        print span_part[4]  # 投资占比
                        print span_part[5]  # 注册时间
                        print span_part[6]  # 状态
                        print '--------------------------'
                        cursor.execute(
                            'insert tyc_out_investment_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                            (url,
                             corp_name,
                             corp_id,

                             span_part[0].decode('utf-8'),
                             invested_person[0].decode('utf-8'),
                             span_part[2].decode('utf-8'),
                             span_part[3].decode('utf-8'),
                             span_part[4].decode('utf-8'),
                             span_part[5].decode('utf-8'),
                             span_part[6].decode('utf-8'),
                             str(datetime.datetime.now()),
                             str(datetime.datetime.now())[:10])
                        )
            break
        except Exception, e:

            if str(e).find('HTTPSConnectionPool') >= 0:

                print 'HTTPSConnectionPool , retry '

                continue

            elif str(e).find("OperationalError: (2006, 'MySQL server has gone away')") >= 0:

                return 'MySql error 2006 ,restart'

            elif str(e).find('2003') >= 0:

                return 'MySql error 2003 ,restart'

            else:
                print str(e)
                break


def change_info(url, cursor, conn):
    print u'爬取变更记录信息  ' + str(datetime.datetime.now())
    corp_id = url.split('/company/')[1]

    while True:
        try:
            html = get_page(url)
            if html.text.__contains__('天眼查-人人都在用企业信息调查工具_企业信息查询_公司查询_工商查询_信用查询平台'):
                print 'parse error , retry'
                continue
            else:
                corp_name = re.findall(
                    '<span class="f18 in-block vertival-middle sec-c2" style="font-weight: 600">(.*?)</span>',
                    html.text)[0]
                print corp_name
                if html.text.__contains__('nav-main-changeCount'):
                    soup = BeautifulSoup(html.text, 'lxml')
                    num = soup.select('#nav-main-changeCount > span')[0].text
                    if int(num) % 5 == 0:
                        all_page_no = int(num) / 5
                    else:
                        all_page_no = int(num) / 5 + 1
                    print all_page_no

                    for i in range(1, int(all_page_no) + 1):
                        soup2 = get_cookie_by_id('changeinfo', i, 20, corp_id)
                        res = soup2.select('tr')
                        for x in range(1, len(res)):
                            source = str(res[x])
                            part_one = re_findall('<div>(.*?)</div>', source)
                            part_two = re_findall('<div class="textJustFy changeHoverText">(.*?)</div>', source)
                            change_time = part_one[0]
                            change_projects = part_one[1]
                            before_change = detag(part_two[0])
                            after_change = detag(part_two[1])
                            print change_time.decode('utf-8')
                            print change_projects.decode('utf-8')
                            print before_change.decode('utf-8')
                            print after_change.decode('utf-8')
                            cursor.execute(
                                'insert into tyc_change_record_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                                (url,
                                 corp_name,
                                 corp_id,
                                 change_time.decode('utf-8'),
                                 change_projects.decode('utf-8'),
                                 detag(before_change).decode('utf-8'),
                                 detag(after_change).decode('utf-8'),
                                 str(datetime.datetime.now()),
                                 str(datetime.datetime.now())[:10])
                            )
            break
        except Exception, e:
            if str(e).find('HTTPSConnectionPool') >= 0:
                print 'HTTPSConnectionPool , retry '
                continue
            elif str(e).find("OperationalError: (2006, 'MySQL server has gone away')") >= 0:
                return 'MySql error 2006 ,restart'
            elif str(e).find('2003') >= 0:
                return 'MySql error 2003 ,restart'
            else:
                print str(e)
                break


def product_info(url, cursor, conn):
    print u'爬取产品信息  ' + str(datetime.datetime.now())
    corp_id = url.split('/company/')[1]

    while True:
        try:
            html = get_page(url)
            if html.text.__contains__('天眼查-人人都在用企业信息调查工具_企业信息查询_公司查询_工商查询_信用查询平台'):
                print 'parse error , retry'
                continue
            else:
                corp_name = re.findall(
                    '<span class="f18 in-block vertival-middle sec-c2" style="font-weight: 600">(.*?)</span>',
                    html.text)[0]
                print corp_name
                if html.text.__contains__('nav-main-productinfo'):
                    soup = BeautifulSoup(html.text, 'lxml')
                    num = soup.select('#nav-main-productinfo > span')[0].text
                    if int(num) % 5 == 0:
                        all_page_no = int(num) / 5
                    else:
                        all_page_no = int(num) / 5 + 1
                    print all_page_no

                    for i in range(1, int(all_page_no) + 1):
                        soup2 = get_cookie_by_id('product', i, 5, corp_id)
                        res = soup2.select('tr')
                        for x in range(1, len(res)):
                            source = str(res[x])
                            image = re_findall('src="(.*?)"', source)
                            part_one = re_findall('<span>(.*?)</span>', source)
                            detail_info = re_findall('<td><script type="text/html">(.*?)</script>', source)
                            print image[0]
                            print part_one[0]
                            print part_one[1]
                            print part_one[2]
                            print part_one[3]
                            print detail_info[0]
                            print '--------------------'
                            cursor.execute(
                                'insert into tyc_product_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                                (url,
                                 corp_name,
                                 corp_id,

                                 image[0],
                                 part_one[0].decode('utf-8'),
                                 part_one[1].decode('utf-8'),
                                 part_one[2].decode('utf-8'),
                                 part_one[3].decode('utf-8'),
                                 detag(detail_info[0]).decode('utf-8'),
                                 str(datetime.datetime.now()),
                                 str(datetime.datetime.now())[:10]
                                 )
                            )
            break
        except Exception, e:
            if str(e).find('HTTPSConnectionPool') >= 0:
                print 'HTTPSConnectionPool , retry '
                continue
            elif str(e).find("OperationalError: (2006, 'MySQL server has gone away')") >= 0:
                return 'MySql error 2006 ,restart'
            elif str(e).find('2003') >= 0:
                return 'MySql error 2003 ,restart'
            else:
                print str(e)
                break


def wechat_info(url, cursor, conn):
    print u'爬取微信公众号信息  ' + str(datetime.datetime.now())
    corp_id = url.split('/company/')[1]

    while True:
        try:
            html = get_page(url)
            if html.text.__contains__('天眼查-人人都在用企业信息调查工具_企业信息查询_公司查询_工商查询_信用查询平台'):
                print 'parse error , retry'
                continue
            else:
                corp_name = re.findall(
                    '<span class="f18 in-block vertival-middle sec-c2" style="font-weight: 600">(.*?)</span>',
                    html.text)[0]
                print corp_name
                if html.text.__contains__('nav-main-weChatCount'):
                    soup = BeautifulSoup(html.text, 'lxml')
                    num = soup.select('#nav-main-weChatCount > span')[0].text
                    all_page_no = int(num) / 10 + 1
                    last_page_no = int(num) % 10
                    for i in range(1, int(all_page_no) + 1):
                        soup2 = get_cookie_by_id('wechat', i, 10, corp_id)
                        if i < int(all_page_no):

                            for n in range(1, 11):
                                wechat_icon = soup2.select(
                                    'body > div:nth-of-type(1) > div:nth-of-type(' + str(
                                        n) + ') > div.in-block.vertical-top.wechatImg > img')[0]['src']

                                wechat_name = soup2.select(
                                    'body > div:nth-of-type(1) > div:nth-of-type(' + str(
                                        n) + ') > div.in-block.vertical-top.itemRight > div:nth-of-type(1)')[0].text

                                wechat_num = soup2.select(
                                    'body > div:nth-of-type(1) > div:nth-of-type(' + str(
                                        n) + ') > div.in-block.vertical-top.itemRight > div:nth-of-type(2) > span:nth-of-type(2)')[
                                    0].text

                                wechat_introduce = soup2.select(
                                    'body > div:nth-of-type(1) > div:nth-of-type(' + str(
                                        n) + ') > div.in-block.vertical-top.itemRight > div:nth-of-type(3) > span.overflow-width.in-block.vertical-top')[
                                    0].text

                                QR_code = soup2.select(
                                    'body > div:nth-of-type(1) > div:nth-of-type(' + str(
                                        n) + ') > div.in-block.vertical-top.itemRight > div:nth-of-type(2) > div > div > img')[
                                    0][
                                    'src']

                                cursor.execute(
                                    'insert into tyc_wechat_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                                    (url,
                                     corp_name,
                                     corp_id,
                                     wechat_icon,
                                     wechat_name,
                                     wechat_num,
                                     wechat_introduce,
                                     QR_code,
                                     str(datetime.datetime.now()),
                                     str(datetime.datetime.now())[:10])
                                )


                        else:
                            for n in range(1, int(last_page_no) + 1):
                                wechat_icon = soup2.select(
                                    'body > div:nth-of-type(1) > div:nth-of-type(' + str(
                                        n) + ') > div.in-block.vertical-top.wechatImg > img')[0]['src']

                                wechat_name = soup2.select(
                                    'body > div:nth-of-type(1) > div:nth-of-type(' + str(
                                        n) + ') > div.in-block.vertical-top.itemRight > div:nth-of-type(1)')[0].text

                                wechat_num = soup2.select(
                                    'body > div:nth-of-type(1) > div:nth-of-type(' + str(
                                        n) + ') > div.in-block.vertical-top.itemRight > div:nth-of-type(2) > span:nth-of-type(2)')[
                                    0].text

                                wechat_introduce = soup2.select(
                                    'body > div:nth-of-type(1) > div:nth-of-type(' + str(
                                        n) + ') > div.in-block.vertical-top.itemRight > div:nth-of-type(3) > span.overflow-width.in-block.vertical-top')[
                                    0].text

                                QR_code = soup2.select(
                                    'body > div:nth-of-type(1) > div:nth-of-type(' + str(
                                        n) + ') > div.in-block.vertical-top.itemRight > div:nth-of-type(2) > div > div > img')[
                                    0][
                                    'src']

                                cursor.execute(
                                    'insert into tyc_wechat_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                                    (url,
                                     corp_name,
                                     corp_id,
                                     wechat_icon,
                                     wechat_name,
                                     wechat_num,
                                     wechat_introduce,
                                     QR_code,
                                     str(datetime.datetime.now()),
                                     str(datetime.datetime.now())[:10])
                                )
            break
        except Exception, e:
            if str(e).find('HTTPSConnectionPool') >= 0:
                print 'HTTPSConnectionPool , retry '
                continue
            elif str(e).find("OperationalError: (2006, 'MySQL server has gone away')") >= 0:
                return 'MySql error 2006 ,restart'
            elif str(e).find('2003') >= 0:
                return 'MySql error 2003 ,restart'
            else:
                print str(e)
                break


def website_record(url, cursor, conn):
    print u'爬取网站备案信息  ' + str(datetime.datetime.now())
    corp_id = url.split('/company/')[1]

    while True:
        try:
            html = get_page(url)
            if html.text.__contains__('天眼查-人人都在用企业信息调查工具_企业信息查询_公司查询_工商查询_信用查询平台'):
                print 'parse error , retry'
                continue
            else:
                corp_name = re.findall(
                    '<span class="f18 in-block vertival-middle sec-c2" style="font-weight: 600">(.*?)</span>',
                    html.text)[0]
                print corp_name
                if html.text.__contains__('nav-main-icpCount'):
                    soup = BeautifulSoup(html.text, 'lxml')
                    num = soup.select('#nav-main-icpCount > span')[0].text
                    if int(num) % 5 == 0:
                        all_page_no = int(num) / 5
                    else:
                        all_page_no = int(num) / 5 + 1
                    print all_page_no
                    for i in range(1, int(all_page_no) + 1):
                        soup2 = get_cookie_by_id('icp', i, 5, corp_id)
                        res = soup2.select('tr')
                        for x in range(1, len(res)):
                            source = str(res[x])
                            part_one = re_findall('<td><span>(.*?)</span></td>', source)
                            part_two = re_findall('target="_blank">(.*?)</a></td>', source)
                            check_time = part_one[0]
                            website_name = part_one[1]
                            homepage = part_two[0]
                            domain = re_findall('<td>(.*?)</td>', source)[3]
                            record_number = part_one[2]
                            state = part_one[3]
                            unit_character = part_one[4]
                            print part_one
                            print part_two
                            print check_time
                            print website_name
                            print homepage
                            print domain
                            print record_number
                            print state
                            print unit_character
                            print '--------------------------'
                            cursor.execute(
                                'insert into tyc_webrecord_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                                (url,
                                 corp_name,
                                 corp_id,
                                 check_time.decode('utf-8'),
                                 website_name.decode('utf-8'),
                                 homepage.decode('utf-8'),
                                 domain.decode('utf-8'),
                                 record_number.decode('utf-8'),
                                 state.decode('utf-8'),
                                 unit_character.decode('utf-8'),
                                 str(datetime.datetime.now()),
                                 str(datetime.datetime.now())[:10])
                            )
            break
        except Exception, e:
            if str(e).find('HTTPSConnectionPool') >= 0:
                print 'HTTPSConnectionPool , retry '
                continue
            elif str(e).find("OperationalError: (2006, 'MySQL server has gone away')") >= 0:
                return 'MySql error 2006 ,restart'
            elif str(e).find('2003') >= 0:
                return 'MySql error 2003 ,restart'
            else:
                print str(e)
                break


def lawsuit(url, cursor, conn):
    print u'爬取法律诉讼信息  ' + str(datetime.datetime.now())
    corp_id = url.split('/company/')[1]

    while True:
        try:
            html = get_page(url)
            if html.text.__contains__('天眼查-人人都在用企业信息调查工具_企业信息查询_公司查询_工商查询_信用查询平台'):
                print 'parse error , retry'
                continue
            else:
                corp_name = re.findall(
                    '<span class="f18 in-block vertival-middle sec-c2" style="font-weight: 600">(.*?)</span>',
                    html.text)[0]
                print corp_name
                if html.text.__contains__('nav-main-lawsuitCount'):
                    soup = BeautifulSoup(html.text, 'lxml')
                    num = soup.select('#nav-main-lawsuitCount > span')[0].text
                    if int(num) % 5 == 0:
                        all_page_no = int(num) / 5
                    else:
                        all_page_no = int(num) / 5 + 1
                    print all_page_no
                    for i in range(1, int(all_page_no) + 1):
                        print u'爬第' + str(i) + u'页'
                        soup2 = get_cookie_by_name('lawsuit', i, 5, corp_name)
                        print soup2
                        res = soup2.select('tr')
                        for x in range(1, len(res)):
                            source = str(res[x])
                            print source

                            date = re_findall('<span class=".*?">(.*?)</span>', source)[0]
                            Judgment_document_url = re_findall('href="(.*?)" href-new-event', source)[0]
                            Judgment_document_name = re_findall('target="_blank">(.*?)</a>', source)[0]
                            cause = re_findall('<span class=".*?">(.*?)</span>', source)[1]
                            identity = detag(re_findall('<div class="text-dark-color">(.*?)</div>', source)[0])
                            docket_number = re_findall('<span class=".*?">(.*?)</span>', source)[2]
                            cursor.execute(
                                'insert into tyc_lawsuit_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                                (url,
                                 corp_name,
                                 corp_id,

                                 date.decode('utf-8'),
                                 Judgment_document_name.decode('utf-8'),
                                 Judgment_document_url.decode('utf-8'),
                                 cause.decode('utf-8'),
                                 identity.decode('utf-8'),
                                 docket_number.decode('utf-8'),

                                 str(datetime.datetime.now()),
                                 str(datetime.datetime.now())[:10]
                                 )
                            )
            break
        except Exception, e:
            if str(e).find('HTTPSConnectionPool') >= 0:
                print 'HTTPSConnectionPool , retry '
                continue
            elif str(e).find("OperationalError: (2006, 'MySQL server has gone away')") >= 0:
                return 'MySql error 2006 ,restart'
            elif str(e).find('2003') >= 0:
                return 'MySql error 2003 ,restart'
            else:
                print str(e)
                break


def court(url, cursor, conn):
    print u'爬取法院公告信息  ' + str(datetime.datetime.now())
    corp_id = url.split('/company/')[1]

    while True:
        try:
            html = get_page(url)
            if html.text.__contains__('天眼查-人人都在用企业信息调查工具_企业信息查询_公司查询_工商查询_信用查询平台'):
                print 'parse error , retry'
                continue
            else:
                corp_name = re.findall(
                    '<span class="f18 in-block vertival-middle sec-c2" style="font-weight: 600">(.*?)</span>',
                    html.text)[0]
                print corp_name
                if html.text.__contains__('nav-main-courtCount'):
                    soup = BeautifulSoup(html.text, 'lxml')
                    num = soup.select('#nav-main-courtCount > span')[0].text
                    if int(num) % 5 == 0:
                        all_page_no = int(num) / 5
                    else:
                        all_page_no = int(num) / 5 + 1
                    print all_page_no
                    for i in range(1, int(all_page_no) + 1):
                        soup2 = get_cookie_by_name('court', i, 5, corp_name)
                        res = soup2.select('tr')
                        for x in range(1, len(res)):
                            source = str(res[x])

                            date = re_findall('"publishdate":"(.*?)"', source)[0]
                            appellant = re_findall('"party1":"(.*?)"', source)[0]
                            defendant = re_findall('"party2":"(.*?)"', source)[0]
                            type = re_findall('"bltntypename":"(.*?)"', source)[0]
                            court = re_findall('"courtcode":"(.*?)"', source)[0]
                            detail = re_findall('"content":"(.*?)"', source)[0]
                            cursor.execute(
                                'insert into tyc_court_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                                (url,
                                 corp_name,
                                 corp_id,
                                 date.decode('utf-8'),
                                 appellant.decode('utf-8'),
                                 defendant.decode('utf-8'),
                                 type.decode('utf-8'),
                                 court.decode('utf-8'),
                                 detail.decode('utf-8'),
                                 str(datetime.datetime.now()),
                                 str(datetime.datetime.now())[:10]
                                 )
                            )
            break
        except Exception, e:
            if str(e).find('HTTPSConnectionPool') >= 0:
                print 'HTTPSConnectionPool , retry '
                continue
            elif str(e).find("OperationalError: (2006, 'MySQL server has gone away')") >= 0:
                return 'MySql error 2006 ,restart'
            elif str(e).find('2003') >= 0:
                return 'MySql error 2003 ,restart'
            else:
                print str(e)
                break


def zhixing(url, cursor, conn):
    print u'爬取执行信息  ' + str(datetime.datetime.now())
    corp_id = url.split('/company/')[1]

    while True:
        try:
            html = get_page(url)
            if html.text.__contains__('天眼查-人人都在用企业信息调查工具_企业信息查询_公司查询_工商查询_信用查询平台'):
                print 'parse error , retry'
                continue
            else:
                corp_name = re.findall(
                    '<span class="f18 in-block vertival-middle sec-c2" style="font-weight: 600">(.*?)</span>',
                    html.text)[0]
                print corp_name
                if html.text.__contains__('nav-main-zhixing'):
                    soup = BeautifulSoup(html.text, 'lxml')
                    num = soup.select('#nav-main-zhixing > span')[0].text
                    if int(num) % 5 == 0:
                        all_page_no = int(num) / 5
                    else:
                        all_page_no = int(num) / 5 + 1
                    print all_page_no

                    for i in range(1, int(all_page_no) + 1):
                        soup2 = get_cookie_by_id('zhixing', i, 5, corp_id)
                        res = soup2.select('tr')
                        for x in range(1, len(res)):
                            source = str(res[x])
                            part = re_findall('<span class=".*?">(.*?)</span>', source)
                            print part[0]
                            print part[1]
                            print part[2]
                            print part[3]
                            cursor.execute(
                                'insert into tyc_zhixing_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                                (url,
                                 corp_name,
                                 corp_id,
                                 part[0].decode('utf-8'),
                                 part[1].decode('utf-8'),
                                 part[2].decode('utf-8'),
                                 part[3].decode('utf-8'),
                                 str(datetime.datetime.now()),
                                 str(datetime.datetime.now())[:10]
                                 )
                            )
            break
        except Exception, e:
            if str(e).find('HTTPSConnectionPool') >= 0:
                print 'HTTPSConnectionPool , retry '
                continue
            elif str(e).find("OperationalError: (2006, 'MySQL server has gone away')") >= 0:
                return 'MySql error 2006 ,restart'
            elif str(e).find('2003') >= 0:
                return 'MySql error 2003 ,restart'
            else:
                print str(e)
                break


def announcement(url, cursor, conn):
    print u'爬取开庭公告信息  ' + str(datetime.datetime.now())
    corp_id = url.split('/company/')[1]

    while True:
        try:
            html = get_page(url)
            if html.text.__contains__('天眼查-人人都在用企业信息调查工具_企业信息查询_公司查询_工商查询_信用查询平台'):
                print 'parse error , retry'
                continue
            else:
                # print html.text
                corp_name = re.findall(
                    '<span class="f18 in-block vertival-middle sec-c2" style="font-weight: 600">(.*?)</span>',
                    html.text)[0]
                print corp_name
                if html.text.__contains__('nav-main-announcementCount'):
                    soup = BeautifulSoup(html.text, 'lxml')
                    num = soup.select('#nav-main-announcementCount > span')[0].text

                    if int(num) % 5 == 0:
                        all_page_no = int(num) / 5
                    else:
                        all_page_no = int(num) / 5 + 1
                    print all_page_no

                    for i in range(1, int(all_page_no) + 1):
                        soup2 = get_cookie_by_id('announcementcourt', i, 5, corp_id)
                        res = soup2.select('tr')
                        for x in range(1, len(res)):
                            source = str(res[x])
                            date = re_findall('<td>(.*?)</td>', source)[0]
                            type = re_findall('<span class="text-dark-color">(.*?)</span>', source)[0]
                            appellant = re_findall('"name":"(.*?)",', source)[0]
                            defendant = re_findall('"name":"(.*?)",', source)[1]
                            case_no = re_findall('"caseNo":"(.*?)",', source)[0]

                            cursor.execute(
                                'insert into tyc_announcement_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                                (url,
                                 corp_name,
                                 corp_id,
                                 date.decode('utf-8'),
                                 type.decode('utf-8'),
                                 appellant.decode('utf-8'),
                                 defendant.decode('utf-8'),
                                 case_no.decode('utf-8'),
                                 str(datetime.datetime.now()),
                                 str(datetime.datetime.now())[:10])
                            )
                    break
                else:
                    print "no announcement "
                    break
            break

        except Exception, e:
            if str(e).find('HTTPSConnectionPool') >= 0:
                print 'HTTPSConnectionPool , retry '
                continue
            elif str(e).find("OperationalError: (2006, 'MySQL server has gone away')") >= 0:
                return 'MySql error 2006 ,restart'
            elif str(e).find('2003') >= 0:
                return 'MySql error 2003 ,restart'
            else:
                print str(e)
                break


def punish(url, cursor, conn):
    print u'爬取惩罚信息  ' + str(datetime.datetime.now())
    corp_id = url.split('/company/')[1]

    while True:
        try:
            html = get_page(url)
            if html.text.__contains__('天眼查-人人都在用企业信息调查工具_企业信息查询_公司查询_工商查询_信用查询平台'):
                print 'parse error , retry'
                continue
            else:
                corp_name = re.findall(
                    '<span class="f18 in-block vertival-middle sec-c2" style="font-weight: 600">(.*?)</span>',
                    html.text)[0]
                print corp_name
                if html.text.__contains__('nav-main-punishment'):
                    soup = BeautifulSoup(html.text, 'lxml')
                    num = soup.select('#nav-main-punishment > span')[0].text

                    if int(num) % 5 == 0:
                        all_page_no = int(num) / 5
                    else:
                        all_page_no = int(num) / 5 + 1
                    print all_page_no
                    for i in range(1, int(all_page_no) + 1):
                        soup2 = get_cookie_by_name('punish', i, 5, corp_name)
                        res = soup2.select('tr')
                        for x in range(1, len(res)):
                            source = str(res[x])
                            print source

                            date = re_findall('<span class=".*?">(.*?)</span>', source)[0]
                            document_no = re_findall('<span class=".*?">(.*?)</span>', source)[1]
                            type = re_findall('<span class=".*?">(.*?)</span>', source)[2]
                            decision_organ = re_findall('<div class=".*?">(.*?)</div>', source)[0]

                            print date
                            print document_no
                            print type
                            print decision_organ
                            cursor.execute(
                                'insert into tyc_punish_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                                (url,
                                 corp_name,
                                 corp_id,
                                 date.decode('utf-8'),
                                 document_no.decode('utf-8'),
                                 type.decode('utf-8'),
                                 decision_organ.decode('utf-8'),
                                 str(datetime.datetime.now()),
                                 str(datetime.datetime.now())[:10])
                            )
            break
        except Exception, e:
            if str(e).find('HTTPSConnectionPool') >= 0:
                print 'HTTPSConnectionPool , retry '
                continue
            elif str(e).find("OperationalError: (2006, 'MySQL server has gone away')") >= 0:
                return 'MySql error 2006 ,restart'
            elif str(e).find('2003') >= 0:
                return 'MySql error 2003 ,restart'
            else:
                print str(e)
                break


def recruit(url, cursor, conn):
    print u'爬取招聘信息  ' + str(datetime.datetime.now())
    corp_id = url.split('/company/')[1]

    while True:
        try:
            html = get_page(url)
            if html.text.__contains__('天眼查-人人都在用企业信息调查工具_企业信息查询_公司查询_工商查询_信用查询平台'):
                print 'parse error , retry'
                continue
            else:
                corp_name = re.findall(
                    '<span class="f18 in-block vertival-middle sec-c2" style="font-weight: 600">(.*?)</span>',
                    html.text)[0]
                print corp_name

                if html.text.__contains__('nav-main-recruitCount'):
                    soup = BeautifulSoup(html.text, 'lxml')
                    num = soup.select('#nav-main-recruitCount > span')[0].text
                    if int(num) % 5 == 0:
                        all_page_no = int(num) / 5
                    else:
                        all_page_no = int(num) / 5 + 1
                    print all_page_no
                    for i in range(1, int(all_page_no) + 1):
                        soup2 = get_cookie_by_name('recruit', i, 10, corp_name)
                        res = soup2.select('tr')
                        for x in range(1, len(res)):
                            source = str(res[x])
                            print source
                            date = re_findall('<span.*?>(.*?)</span>', source)[0]
                            job = re_findall('<span.*?>(.*?)</span>', source)[1]
                            exper = re_findall('<span.*?>(.*?)</span>', source)[2]
                            num = re_findall('<span.*?>(.*?)</span>', source)[3]
                            location = re_findall('<span.*?>(.*?)</span>', source)[4]
                            salary = re_findall('"oriSalary":"(.*?)"', source)[0]
                            detail = re_findall('"description":"(.*?)"', source)[0]
                            fromWeb = re_findall('"source":"(.*?)"', source)[0]
                            cursor.execute(
                                'insert into tyc_recruit_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                                (url,
                                 corp_name,
                                 corp_id,

                                 date.decode('utf-8'),
                                 job.decode('utf-8'),
                                 exper.decode('utf-8'),
                                 num.decode('utf-8'),
                                 location.decode('utf-8'),
                                 salary.decode('utf-8'),
                                 detag(detail.decode('utf-8')),
                                 fromWeb.decode('utf-8'),

                                 str(datetime.datetime.now()),
                                 str(datetime.datetime.now())[:10])
                            )
            break
        except Exception, e:
            if str(e).find('HTTPSConnectionPool') >= 0:
                print 'HTTPSConnectionPool , retry '
                continue
            elif str(e).find("OperationalError: (2006, 'MySQL server has gone away')") >= 0:
                return 'MySql error 2006 ,restart'
            elif str(e).find('2003') >= 0:
                return 'MySql error 2003 ,restart'
            else:
                print str(e)
                break


def patent(url, cursor, conn):
    print u'爬取专利信息  ' + str(datetime.datetime.now())
    corp_id = url.split('/company/')[1]

    while True:
        try:
            html = get_page(url)
            if html.text.__contains__('天眼查-人人都在用企业信息调查工具_企业信息查询_公司查询_工商查询_信用查询平台'):
                print 'parse error , retry'
                continue
            else:
                corp_name = re.findall(
                    '<span class="f18 in-block vertival-middle sec-c2" style="font-weight: 600">(.*?)</span>',
                    html.text)[0]
                print corp_name
                if html.text.__contains__('nav-main-patentCount'):
                    soup = BeautifulSoup(html.text, 'lxml')
                    num = soup.select('#nav-main-patentCount > span')[0].text
                    if int(num) % 5 == 0:
                        all_page_no = int(num) / 5
                    else:
                        all_page_no = int(num) / 5 + 1
                    print all_page_no

                    for i in range(1, int(all_page_no) + 1):
                        soup2 = get_cookie_by_id('patent', i, 5, corp_id)
                        res = soup2.select('tr')
                        for x in range(1, len(res)):
                            source = str(res[x])

                            date = re_findall('<span.*?>(.*?)</span>', source)[0]
                            name = re_findall('<span.*?>(.*?)</span>', source)[1]
                            application_num = re_findall('<span.*?>(.*?)</span>', source)[2]
                            application_for_pubnum = re_findall('<span.*?>(.*?)</span>', source)[3]

                            print date
                            print name
                            print application_num
                            print application_for_pubnum
                            cursor.execute(
                                'insert into tyc_patent_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                                (url,
                                 corp_name,
                                 corp_id,

                                 date.decode('utf-8'),
                                 name.decode('utf-8'),
                                 application_num.decode('utf-8'),
                                 application_for_pubnum.decode('utf-8'),

                                 str(datetime.datetime.now()),
                                 str(datetime.datetime.now())[:10])
                            )

            break

        except Exception, e:
            if str(e).find('HTTPSConnectionPool') >= 0:
                print 'HTTPSConnectionPool , retry '
                continue
            elif str(e).find("OperationalError: (2006, 'MySQL server has gone away')") >= 0:
                return 'MySql error 2006 ,restart'
            elif str(e).find('2003') >= 0:
                return 'MySql error 2003 ,restart'
            else:
                print str(e)
                break


def copyR(url, cursor, conn):
    print u'获取软件著作权部分  ' + str(datetime.datetime.now())
    corp_id = url.split('/company/')[1]

    while True:
        try:
            html = get_page(url)
            if html.text.__contains__('天眼查-人人都在用企业信息调查工具_企业信息查询_公司查询_工商查询_信用查询平台'):
                print 'parse error , retry'
                continue
            else:
                corp_name = re.findall(
                    '<span class="f18 in-block vertival-middle sec-c2" style="font-weight: 600">(.*?)</span>',
                    html.text)[0]
                print corp_name
                if html.text.__contains__('nav-main-cpoyRCount'):
                    soup = BeautifulSoup(html.text, 'lxml')
                    num = soup.select('#nav-main-cpoyRCount > span')[0].text
                    if int(num) % 5 == 0:
                        all_page_no = int(num) / 5
                    else:
                        all_page_no = int(num) / 5 + 1
                    print all_page_no
                    for i in range(1, int(all_page_no) + 1):
                        soup2 = get_cookie_by_id('copyright', i, 5, corp_id)
                        res = soup2.select('tr')
                        for x in range(1, len(res)):
                            source = str(res[x])

                            obj = re_findall('<span>(.*?)</span>', source)
                            date = obj[0]
                            name = obj[1]
                            brief_name = obj[2]
                            registration_no = obj[3]
                            classification_no = obj[4]
                            version_no = obj[5]

                            print date
                            print name
                            print brief_name
                            print registration_no
                            print classification_no
                            print version_no
                            cursor.execute(
                                'insert into tyc_copyRcount_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s" )' %
                                (url,
                                 corp_name,
                                 corp_id,
                                 date.decode('utf-8'),
                                 name.decode('utf-8'),
                                 brief_name.decode('utf-8'),
                                 registration_no.decode('utf-8'),
                                 classification_no.decode('utf-8'),
                                 version_no.decode('utf-8'),

                                 str(datetime.datetime.now()),
                                 str(datetime.datetime.now())[:10])
                            )

            break

        except Exception, e:
            if str(e).find('HTTPSConnectionPool') >= 0:
                print 'HTTPSConnectionPool , retry '
                continue
            elif str(e).find("OperationalError: (2006, 'MySQL server has gone away')") >= 0:
                return 'MySql error 2006 ,restart'
            elif str(e).find('2003') >= 0:
                return 'MySql error 2003 ,restart'
            else:
                print str(e)
                break


def copyrightWorks(url, cursor, conn):
    print u'获取作品著作权部分  ' + str(datetime.datetime.now())
    corp_id = url.split('/company/')[1]

    while True:
        try:
            html = get_page(url)
            if html.text.__contains__('天眼查-人人都在用企业信息调查工具_企业信息查询_公司查询_工商查询_信用查询平台'):
                print 'parse error , retry'
                continue
            else:
                corp_name = re.findall(
                    '<span class="f18 in-block vertival-middle sec-c2" style="font-weight: 600">(.*?)</span>',
                    html.text)[0]
                print corp_name

                if html.text.__contains__('nav-main-copyrightWorks'):
                    soup = BeautifulSoup(html.text, 'lxml')
                    num = soup.select('#nav-main-copyrightWorks > span')[0].text
                    if int(num) % 5 == 0:
                        all_page_no = int(num) / 5
                    else:
                        all_page_no = int(num) / 5 + 1
                    print all_page_no
                    for i in range(1, int(all_page_no) + 1):
                        soup2 = get_cookie_by_id('copyrightWorks', i, 5, corp_id)
                        res = soup2.select('tr')
                        for x in range(1, len(res)):
                            source = str(res[x])

                            obj = re_findall('<span>(.*?)</span>', source)
                            name = obj[0]
                            register_no = obj[1]
                            category = obj[2]
                            finish_date = obj[3]
                            register_date = obj[4]
                            publish_date = obj[5]

                            print name
                            print register_no
                            print category
                            print finish_date
                            print register_date
                            print publish_date
                            cursor.execute(
                                'insert into tyc_copyRworks_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                                (url,
                                 corp_name,
                                 corp_id,

                                 name.decode('utf-8'),
                                 register_no.decode('utf-8'),
                                 category.decode('utf-8'),
                                 finish_date.decode('utf-8'),
                                 register_date.decode('utf-8'),
                                 publish_date.decode('utf-8'),

                                 str(datetime.datetime.now()),
                                 str(datetime.datetime.now())[:10])

                            )
            break
        except Exception, e:
            if str(e).find('HTTPSConnectionPool') >= 0:
                print 'HTTPSConnectionPool , retry '
                continue
            elif str(e).find("OperationalError: (2006, 'MySQL server has gone away')") >= 0:
                return 'MySql error 2006 ,restart'
            elif str(e).find('2003') >= 0:
                return 'MySql error 2003 ,restart'
            else:
                print str(e)
                break


def firmProduct(url, cursor, conn):
    print u'获取企业业务部分  ' + str(datetime.datetime.now())
    corp_id = url.split('/company/')[1]

    while True:
        try:
            html = get_page(url)
            if html.text.__contains__('天眼查-人人都在用企业信息调查工具_企业信息查询_公司查询_工商查询_信用查询平台'):
                print 'parse error , retry'
                continue
            else:
                corp_name = re.findall(
                    '<span class="f18 in-block vertival-middle sec-c2" style="font-weight: 600">(.*?)</span>',
                    html.text)[0]
                print corp_name
                if html.text.__contains__('nav-main-companyProduct'):
                    soup = BeautifulSoup(html.text, 'lxml')
                    num = soup.select('#nav-main-companyProduct > span')[0].text
                    if int(num) % 15 == 0:
                        all_page_no = int(num) / 15
                    else:
                        all_page_no = int(num) / 15 + 1

                    for i in range(1, int(all_page_no) + 1):
                        soup2 = get_cookie_by_name('firmProduct', i, 15, corp_name)
                        res = soup2.select('div[class="product-item"]')
                        for x in range(1, len(res)):
                            source = str(res[x])
                            name = re_findall('img alt="(.*?)"', source)[0]
                            img = re_findall('src="(.*?)"', source)[0]
                            category = detag(re_findall('<div class=".*?">(.*?)</div>', source)[2])
                            brief = detag(re_findall('<div class=".*?">(.*?)</div>', source)[3])

                            print name
                            print img
                            print category
                            print brief
                            cursor.execute(
                                'insert into tyc_companyProduct_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                                (url,
                                 corp_name,
                                 corp_id,

                                 name.decode('utf-8'),
                                 img.decode('utf-8'),
                                 category.decode('utf-8'),
                                 brief.decode('utf-8'),

                                 str(datetime.datetime.now()),
                                 str(datetime.datetime.now())[:10])
                            )
            break
        except Exception, e:
            if str(e).find('HTTPSConnectionPool') >= 0:
                print 'HTTPSConnectionPool , retry '
                continue
            elif str(e).find("OperationalError: (2006, 'MySQL server has gone away')") >= 0:
                return 'MySql error 2006 ,restart'
            elif str(e).find('2003') >= 0:
                return 'MySql error 2003 ,restart'
            else:
                print str(e)
                break


def investment_info(url, cursor, conn):
    print u'获取投资事件部分  ' + str(datetime.datetime.now())
    corp_id = url.split('/company/')[1]

    while True:
        try:
            html = get_page(url)
            if html.text.__contains__('天眼查-人人都在用企业信息调查工具_企业信息查询_公司查询_工商查询_信用查询平台'):
                print 'parse error , retry'
                continue
            else:
                corp_name = re.findall(
                    '<span class="f18 in-block vertival-middle sec-c2" style="font-weight: 600">(.*?)</span>',
                    html.text)[0]
                print corp_name
                if html.text.__contains__('nav-main-jigouTzanli'):
                    soup = BeautifulSoup(html.text, 'lxml')
                    num = soup.select('#nav-main-jigouTzanli > span')[0].text
                    if int(num) % 10 == 0:
                        all_page_no = int(num) / 10
                    else:
                        all_page_no = int(num) / 10 + 1
                    for i in range(1, int(all_page_no) + 1):
                        soup2 = get_cookie_by_name('touzi', i, 10, corp_name)
                        res = soup2.select('tr')
                        for x in range(1, len(res)):
                            source = str(res[x])

                            date = re_findall('<span class=".*?">(.*?)</span>', source)[0]
                            round = re_findall('<span class=".*?">(.*?)</span>', source)[1]
                            amount = re_findall('<span class=".*?">(.*?)</span>', source)[2]
                            investor = detag(re_findall('<div>(.*?)<img alt', source)[0])
                            product_name = re_findall('img alt="(.*?)"', source)[0]
                            product_icon = re_findall('src="(.*?)"', source)[0]
                            location = re_findall('<span class=".*?">(.*?)</span>', source)[3]
                            industry = re_findall('<span class=".*?">(.*?)</span>', source)[4]
                            business = re_findall('<span class=".*?">(.*?)</span>', source)[5]

                            print date
                            print round
                            print amount
                            print investor
                            print product_name
                            print product_icon
                            print location
                            print industry
                            print business
                            cursor.execute(
                                'insert into tyc_investment_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                                (url,
                                 corp_name,
                                 corp_id,

                                 date.decode('utf-8'),
                                 round.decode('utf-8'),
                                 amount.decode('utf-8'),
                                 investor.decode('utf-8'),
                                 product_name.decode('utf-8'),
                                 product_icon.decode('utf-8'),
                                 location.decode('utf-8'),
                                 industry.decode('utf-8'),
                                 business.decode('utf-8'),

                                 str(datetime.datetime.now()),
                                 str(datetime.datetime.now())[:10]))

            break
        except Exception, e:
            if str(e).find('HTTPSConnectionPool') >= 0:
                print 'HTTPSConnectionPool , retry '
                continue
            elif str(e).find("OperationalError: (2006, 'MySQL server has gone away')") >= 0:
                return 'MySql error 2006 ,restart'
            elif str(e).find('2003') >= 0:
                return 'MySql error 2003 ,restart'
            else:
                print str(e)
                break


def dishonest(url, cursor, conn):
    print u'爬取失信人信息  ' + str(datetime.datetime.now())
    corp_id = url.split('/company/')[1]

    while True:
        try:
            html = get_page(url)
            if html.text.__contains__('天眼查-人人都在用企业信息调查工具_企业信息查询_公司查询_工商查询_信用查询平台'):
                print 'parse error , retry'
                continue
            else:
                corp_name = re.findall(
                    '<span class="f18 in-block vertival-middle sec-c2" style="font-weight: 600">(.*?)</span>',
                    html.text)[0]
                print corp_name
                if html.text.__contains__('nav-main-dishonest'):
                    soup = BeautifulSoup(html.text, 'lxml')
                    num = soup.select('#nav-main-dishonest > span')[0].text
                    for i in range(1, int(num) + 1):
                        date = soup.select(
                            '#web-content > div > div > div.container.company_container > div > div.col-9.company-main.pl0.pr10.company_new_2017 > div > div.pl30.pr30.pt25 > div:nth-of-type(14) > div:nth-of-type(2) > div > table > tbody > tr:nth-of-type(' + str(
                                i) + ') > td:nth-of-type(1) > span')[0].text
                        case_no = soup.select(
                            '#web-content > div > div > div.container.company_container > div > div.col-9.company-main.pl0.pr10.company_new_2017 > div > div.pl30.pr30.pt25 > div:nth-of-type(14) > div:nth-of-type(2) > div > table > tbody > tr:nth-of-type(' + str(
                                i) + ') > td:nth-of-type(2) > span')[0].text
                        court = soup.select(
                            '#web-content > div > div > div.container.company_container > div > div.col-9.company-main.pl0.pr10.company_new_2017 > div > div.pl30.pr30.pt25 > div:nth-of-type(14) > div:nth-of-type(2) > div > table > tbody > tr:nth-of-type(' + str(
                                i) + ') > td:nth-of-type(3) > span')[0].text
                        state = soup.select(
                            '#web-content > div > div > div.container.company_container > div > div.col-9.company-main.pl0.pr10.company_new_2017 > div > div.pl30.pr30.pt25 > div:nth-of-type(14) > div:nth-of-type(2) > div > table > tbody > tr:nth-of-type(' + str(
                                i) + ') > td:nth-of-type(4) > span')[0].text
                        reference = soup.select(
                            '#web-content > div > div > div.container.company_container > div > div.col-9.company-main.pl0.pr10.company_new_2017 > div > div.pl30.pr30.pt25 > div:nth-of-type(14) > div:nth-of-type(2) > div > table > tbody > tr:nth-of-type(' + str(
                                i) + ') > td:nth-of-type(5) > span')[0].text
                        print date
                        print case_no
                        print court
                        print state
                        print reference
                        cursor.execute(
                            'insert into tyc_dishonest_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
                                url,
                                corp_name,
                                corp_id,
                                date,
                                case_no,
                                court,
                                state,
                                reference,
                                str(datetime.datetime.now()),
                                str(datetime.datetime.now())[:10]))

            break
        except Exception, e:
            if str(e).find('HTTPSConnectionPool') >= 0:
                print 'HTTPSConnectionPool , retry '
                continue
            elif str(e).find("OperationalError: (2006, 'MySQL server has gone away')") >= 0:
                return 'MySql error 2006 ,restart'
            elif str(e).find('2003') >= 0:
                return 'MySql error 2003 ,restart'
            else:
                print str(e)
                break


def rongziHistory(url, cursor, conn):
    print u'获取融资历史  ' + str(datetime.datetime.now())
    corp_id = url.split('/company/')[1]

    while True:
        try:
            html = get_page(url)
            # print html.text

            if html.text.__contains__('天眼查-人人都在用企业信息调查工具_企业信息查询_公司查询_工商查询_信用查询平台'):
                print 'parse error , retry'
                continue
            else:
                corp_name = re.findall(
                    '<span class="f18 in-block vertival-middle sec-c2" style="font-weight: 600">(.*?)</span>',
                    html.text)[0]
                print corp_name
                if html.text.__contains__('nav-main-companyRongzi'):
                    soup = BeautifulSoup(html.text, 'lxml')
                    num = soup.select('#nav-main-companyRongzi > span')[0].text
                    if int(num) % 10 == 0:
                        all_page_no = int(num) / 10
                    else:
                        all_page_no = int(num) / 10 + 1
                    print all_page_no

                    for i in range(1, int(all_page_no) + 1):
                        soup2 = get_cookie_by_name('rongzi', i, 10, corp_name)
                        res = soup2.select('tr')

                        for x in range(1, len(res)):
                            source = str(res[x])
                            print source
                            all_1 = re_findall('<td><span class="text-dark-color .*?">(.*?)</span></td>', source)
                            print all_1[0]
                            print all_1[1]
                            print all_1[2]
                            print all_1[3]
                            print all_1[4]

                            asd = re_findall('<td><span class="text-dark-color">(.*?)</span></td>', source)
                            print detag(asd[0])
                            print detag(asd[1])
                            print u'插入成功 ok !!! @__ ' + str(datetime.datetime.now())
                            cursor.execute(
                                'insert into tyc_rongziCompany_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                                (
                                    corp_id,
                                    corp_name,
                                    url,

                                    all_1[0].decode('utf-8'),
                                    all_1[1].decode('utf-8'),
                                    all_1[2].decode('utf-8'),
                                    all_1[3].decode('utf-8'),
                                    all_1[4].decode('utf-8'),
                                    detag(asd[0]).decode('utf-8'),
                                    detag(asd[1]).decode('utf-8'),

                                    str(datetime.datetime.now()),
                                    str(datetime.datetime.now())[:10])
                            )
            break
        except Exception, e:

            if str(e).find('HTTPSConnectionPool') >= 0:
                print 'HTTPSConnectionPool , retry '
                continue
            elif str(e).find("OperationalError: (2006, 'MySQL server has gone away')") >= 0:
                return 'MySql error 2006 ,restart'
            elif str(e).find('2003') >= 0:
                return 'MySql error 2003 ,restart'
            else:
                print str(e)
                print traceback.format_exc()
                break


#####################################
def get_cookie_by_name(name, page_no, per_page, company_name):
    while True:
        try:
            proxies1 = get_proxy()
            timestamp = int(time.time() * 1000)
            head1 = {
                'Content-Type': 'application/json; charset=UTF-8',
                'Host': 'www.tianyancha.com',
                'Origin': 'https://www.tianyancha.com',
                'Referer': 'https://www.tianyancha.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'X-Requested-With': 'XMLHttpRequest'
            }
            tongji_url = "https://www.tianyancha.com/tongji/" + urllib.quote(
                company_name.encode('utf8')) + ".json?_=" + str(timestamp)

            tongji_page = requests.get(tongji_url, headers=head1, proxies=proxies1, verify=False)

            cookie = tongji_page.cookies.get_dict()
            js_code = "".join([chr(int(code)) for code in tongji_page.json()["data"].split(",")])

            token = re.findall(r"token=(\w+);", js_code)[0]
            utm_code = re.findall("return'([^']*?)'", js_code)[0]
            t = ord(company_name[0])
            fw = open("/Users/huaiz/PycharmProjects/new_tianyancha/" + name + "_rsid.js", "wb+")
            fw.write('var t = "' + str(t) + '",wtf = "' + utm_code + '";' + static_js_code)
            fw.close()
            phantomResStr = execCmd('phantomjs /Users/huaiz/PycharmProjects/new_tianyancha/' + name + '_rsid.js')
            # --print phantomResStr
            # print "phantomResStr: %s" % phantomResStr
            phantomRes = json.loads(phantomResStr)
            ssuid = phantomRes["ssuid"]
            utm = phantomRes["utm"]

            head2 = {
                'Host': 'www.tianyancha.com',
                # 'Referer': 'https://www.tianyancha.com/company/22822',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Connection': 'keep-alive',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, sdch, br',
                'Cookie': 'ssuid=' + ssuid + '; token=' + token + '; _utm=' + utm + '; aliyungf_tc=' + cookie[
                    "aliyungf_tc"] + '; TYCID=' + cookie["TYCID"] + '; csrfToken=' + cookie[
                              "csrfToken"] + '; uccid=baeee58fe4d1d697092e61f6525e8719',
                'X-Requested-With': 'XMLHttpRequest'
            }

            url = 'https://www.tianyancha.com/pagination/' + name + '.xhtml?ps=' + str(per_page) + '&pn=' + str(
                page_no) + '&name=' + urllib.quote(company_name.encode('utf8')) + '&_=' + str(timestamp - 1)
            print url
            resp = requests.get(url, headers=head2, proxies=proxies1, verify=False)
            # print resp
            html = resp.text
            soup2 = BeautifulSoup(html, 'lxml')
            return soup2
            break
        except Exception, e:
            if str(e).find('list index out of range') >= 0:
                print u'get cookie 失败 重试'
            continue


def get_cookie_by_id(name, page_no, per_page, corp_id):
    while True:
        try:
            proxies1 = get_proxy()
            timestamp = int(time.time() * 1000)
            head1 = {
                'Content-Type': 'application/json; charset=UTF-8',
                'Host': 'www.tianyancha.com',
                'Origin': 'https://www.tianyancha.com',
                'Referer': 'https://www.tianyancha.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'X-Requested-With': 'XMLHttpRequest'
            }
            tongji_url = "https://www.tianyancha.com/tongji/" + corp_id + ".json?_=" + str(timestamp)

            tongji_page = requests.get(tongji_url, headers=head1, proxies=proxies1, verify=False)

            cookie = tongji_page.cookies.get_dict()
            js_code = "".join([chr(int(code)) for code in tongji_page.json()["data"].split(",")])

            token = re.findall(r"token=(\w+);", js_code)[0]
            utm_code = re.findall("return'([^']*?)'", js_code)[0]
            t = ord(corp_id[0])

            fw = open("/Users/huaiz/PycharmProjects/new_tianyancha/" + name + "_rsid.js", "wb+")
            fw.write('var t = "' + str(t) + '",wtf = "' + utm_code + '";' + static_js_code)
            fw.close()
            phantomResStr = execCmd('phantomjs /Users/huaiz/PycharmProjects/new_tianyancha/' + name + '_rsid.js')
            # --print phantomResStr
            # print "phantomResStr: %s" % phantomResStr
            phantomRes = json.loads(phantomResStr)
            ssuid = phantomRes["ssuid"]
            utm = phantomRes["utm"]

            head2 = {
                'Host': 'www.tianyancha.com',
                # 'Referer': 'https://www.tianyancha.com/company/22822',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Connection': 'keep-alive',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, sdch, br',
                'Cookie': 'ssuid=' + ssuid + '; token=' + token + '; _utm=' + utm + '; aliyungf_tc=' + cookie[
                    "aliyungf_tc"] + '; TYCID=' + cookie["TYCID"] + '; csrfToken=' + cookie[
                              "csrfToken"] + '; uccid=baeee58fe4d1d697092e61f6525e8719',
                'X-Requested-With': 'XMLHttpRequest'
            }

            url = 'https://www.tianyancha.com/pagination/' + name + '.xhtml?ps=' + str(per_page) + '&pn=' + str(
                page_no) + '&id=' + corp_id + '&_=' + str(timestamp - 1)
            print url
            resp = requests.get(url, headers=head2, proxies=proxies1, verify=False)
            # print resp
            html = resp.text
            soup2 = BeautifulSoup(html, 'lxml')
            return soup2
            break
        except Exception, e:
            if str(e).find('list index out of range') >= 0:
                print u'get cookie 失败 重试'
            continue


def crawl(url):
    while True:
        conn = MySQLdb.connect(host="localhost", user="root", passwd="root",
                               db="new_tianyancha", charset="utf8")
        cursor = conn.cursor()
        print 'parsing with : ' + url

        # -----------------------------------------------------------------------------
        jingpin(url, cursor, conn)
        if jingpin == 'MySql error 2003 ,restart':
            continue
        elif jingpin == 'MySql error 2006 ,restart':
            continue

        staff(url, cursor, conn)
        if staff == 'MySql error 2003 ,restart':
            continue
        elif staff == 'MySql error 2006 ,restart':
            continue

        shareholder(url, cursor, conn)
        if shareholder == 'MySql error 2003 ,restart':
            continue
        elif shareholder == 'MySql error 2006 ,restart':
            continue

        out_invest(url, cursor, conn)
        if out_invest == 'MySql error 2003 ,restart':
            continue
        elif out_invest == 'MySql error 2006 ,restart':
            continue

        change_info(url, cursor, conn)
        if change_info == 'MySql error 2003 ,restart':
            continue
        elif change_info == 'MySql error 2006 ,restart':
            continue

        product_info(url, cursor, conn)
        if product_info == 'MySql error 2003 ,restart':
            continue
        elif product_info == 'MySql error 2006 ,restart':
            continue

        wechat_info(url, cursor, conn)
        if wechat_info == 'MySql error 2003 ,restart':
            continue
        elif wechat_info == 'MySql error 2006 ,restart':
            continue

        website_record(url, cursor, conn)
        if website_record == 'MySql error 2003 ,restart':
            continue
        elif website_record == 'MySql error 2006 ,restart':
            continue

        lawsuit(url, cursor, conn)
        if lawsuit == 'MySql error 2003 ,restart':
            continue
        elif lawsuit == 'MySql error 2006 ,restart':
            continue

        court(url, cursor, conn)
        if court == 'MySql error 2003 ,restart':
            continue
        elif court == 'MySql error 2006 ,restart':
            continue

        zhixing(url, cursor, conn)
        if zhixing == 'MySql error 2003 ,restart':
            continue
        elif zhixing == 'MySql error 2006 ,restart':
            continue

        announcement(url, cursor, conn)
        if announcement == 'MySql error 2003 ,restart':
            continue
        elif announcement == 'MySql error 2006 ,restart':
            continue

        punish(url, cursor, conn)
        if punish == 'MySql error 2003 ,restart':
            continue
        elif punish == 'MySql error 2006 ,restart':
            continue

        recruit(url, cursor, conn)
        if recruit == 'MySql error 2003 ,restart':
            continue
        elif recruit == 'MySql error 2006 ,restart':
            continue

        patent(url, cursor, conn)
        if out_invest == 'MySql error 2003 ,restart':
            patent
        elif out_invest == 'MySql error 2006 ,restart':
            patent

        copyR(url, cursor, conn)
        if out_invest == 'MySql error 2003 ,restart':
            copyR
        elif out_invest == 'MySql error 2006 ,restart':
            copyR

        copyrightWorks(url, cursor, conn)
        if out_invest == 'MySql error 2003 ,restart':
            copyrightWorks
        elif out_invest == 'MySql error 2006 ,restart':
            copyrightWorks

        firmProduct(url, cursor, conn)
        if out_invest == 'MySql error 2003 ,restart':
            firmProduct
        elif out_invest == 'MySql error 2006 ,restart':
            firmProduct

        investment_info(url, cursor, conn)
        if investment_info == 'MySql error 2003 ,restart':
            continue
        elif investment_info == 'MySql error 2006 ,restart':
            continue

        dishonest(url, cursor, conn)
        if dishonest == 'MySql error 2003 ,restart':
            continue
        elif dishonest == 'MySql error 2006 ,restart':
            continue

        rongziHistory(url, cursor, conn)
        if rongziHistory == 'MySql error 2003 ,restart':
            continue
        elif rongziHistory == 'MySql error 2006 ,restart':
            continue

        # -------------------------------------------------------------------------------
        cursor.execute(
            'insert into tyc_log_info values ("%s","%s","%s")' %
            (url,
             str(datetime.datetime.now()),
             str(datetime.datetime.now())[:10])
        )
        print '录入log表'
        conn.commit()
        print 'insert success ~~~~~~~~~~~~'
        cursor.close()
        conn.close()
        break


if __name__ == "__main__":
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root",
                           db="new_tianyancha",
                           charset="utf8")
    cursor = conn.cursor()

    # print '清表'
    # cursor.execute('truncate table tyc_log_info')
    # cursor.execute('truncate table tyc_jingpin_info')
    # cursor.execute('truncate table tyc_staff_info')
    # cursor.execute('truncate table tyc_shareholder_info')

    cursor.execute('select corp_url from tyc_prepare_info')
    all_urls = []
    urls = cursor.fetchall()
    for y in range(0, len(urls)):
        all_urls.append(urls[y][0])

    cursor.execute('select corp_url from tyc_log_info')
    old_urls = []
    old = cursor.fetchall()
    for y in range(0, len(old)):
        old_urls.append(urls[y][0])
    cursor.close()
    conn.close()

    conn = MySQLdb.connect(host="localhost", user="root", passwd="root",
                           db="new_tianyancha", charset="utf8")
    cursor = conn.cursor()

    target_urls = []
    for url in all_urls:
        if url not in old_urls:
            target_urls.append(url)
    print 'got target urls'

    thread_num = 5
    start_no = 0
    end_no = len(target_urls)

    while start_no < (end_no - thread_num + 1):
        threads = []

        for inner_index in range(0, thread_num):
            threads.append(threading.Thread(target=crawl, args=(target_urls[start_no + inner_index],), ))
        for t in threads:
            t.setDaemon(True)
            t.start()
        t.join()
        start_no += thread_num

        # for target_url in target_urls:
        #     crawl(target_url)

    # conn = MySQLdb.connect(host="139.198.189.129", port=20009, user="root", passwd="somao1129",
    #                        db="tianyancha", charset="utf8")
