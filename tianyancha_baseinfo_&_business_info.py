# -*- coding: utf-8 -*-
# @Time         : 2017/12/7 17:54
# @Author       : Huaiz
# @Email        : Apokar@163.com
# @File         : tianyancha_baseinfo_&_business_info.py
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
    detag = detag.replace('"', ' ')
    detag = detag.replace("'"," ")
    detag = detag.replace('\n', '')
    detag = detag.replace('\t', '')
    return detag


# 获得中文
def get_chinese(str):
    b = re.compile(u"[\u4e00-\u9fa5]*")
    c = "".join(b.findall(str.decode('utf8')))
    return c


def get_info(url):
    while True:
        try:
            print 'parsing url : ' + url
            corp_id = url.split('/company/')[1]

            content_1 = get_parse(url)
            if content_1 != None:
                if content_1.text.__contains__('https://static.tianyancha.com/wap/images/notFound.png'):
                    print u'nofound.img'
                    break
                elif content_1.text.__contains__('https://m.tianyancha.com/login'):
                    print u'需要登录 重试一次'
                    time.sleep(2)
                    continue
                else:
                    conn = MySQLdb.connect(host="localhost", user="root", passwd="root",
                                           db="new_tyc",
                                           charset="utf8")
                    cursor = conn.cursor()

                    # print content_1.text

                    corp_name = \
                        re_findall(
                            '<span class="f18 in-block vertival-middle sec-c2" style="font-weight: 600">(.*?)</span>',
                            str(content_1.text))[
                            0]

                    phone = re_findall('<span class="sec-c3">电话：</span><span>(.*?)</span>', str(content_1.text))[0]

                    email = re_findall('class="in-block vertical-top overflow-width emailWidth">(.*?)</span></div>',
                                       str(content_1.text))[0]

                    website = \
                        re_findall('class="c9 hover_underline*">(.*?)</a></div><div class="in-block vertical-top"',
                                   str(content_1.text))[0]

                    address = \
                        re_findall('title=".*?">(.*?)</span><span class="tic tic-fujin c9"></span>',
                                   str(content_1.text))[
                            0]

                    juridical_person = \
                        re.findall("onclick=\"common.stopPropagation\(event\)\">(.*?)</a></div>", str(content_1.text),
                                   re.S)[0]
                    juridical_person_url = \
                        re.findall("onclick=\"common.openUrl\('(.*?)'\)\">", str(content_1.text), re.S)[0]
                    register_capital = \
                        re.findall('<text class="tyc-num" >(.*?)</text></div></div>', str(content_1.text), re.S)[0]
                    register_time = \
                        re.findall('<text class="tyc-num" >(.*?)</text></div></div>', str(content_1.text), re.S)[1]
                    company_status = \
                        re.findall('<div class="new-c1 pb5">公司状态</div><div><div title="(.*?)"', str(content_1.text),
                                   re.S)[0]
                    business_registration_number = re.findall('reg-number="(.*?)"', str(content_1.text), re.S)[0]
                    uniform_credit_code = \
                        re.findall('<td>(.*?)</td><td class="table-left">公司类型', str(content_1.text), re.S)[0]
                    taxpayer_identification_number = re.findall('纳税人识别号</td><td>(.*?)</td>', str(content_1.text), re.S)[
                        0]
                    business_term = re.findall('营业期限</td><td><span>(.*?)</span>', str(content_1.text), re.S)[0]
                    registration_authority = \
                        re.findall(
                            '<span class="sec-cyel">北大法宝</span>提供</span></span></span></span></td><td>(.*?)</td>',
                            str(content_1.text))[1]
                    registered_address = \
                        re.findall('<td colspan="4">(.*?)<span class="tic tic-fujin c9">', str(content_1.text))[0]
                    organization_code = re.findall('<td width="20%">(.*?)</td>', str(content_1.text))[1]
                    enterprise_type = \
                        re.findall('<td class="table-left">公司类型</td><td>(.*?)</td></tr>', str(content_1.text))[0]
                    industry = re.findall('<td colspan="2">(.*?)</td>', str(content_1.text))[0]
                    approval_date = re.findall('<text class="tyc-num" >(.*?)</text></td>', str(content_1.text))[0]
                    english_name = re.findall('<td colspan="2">(.*?)</td>', str(content_1.text))[2]
                    scope_of_business = \
                        re.findall(
                            '<span class="js-full-container ">(.*?)</span><span class="js-split-container hidden">',
                            str(content_1.text))[0]

                    css_link = re_findall('<link rel="stylesheet" href="(.*?)">', str(content_1.text))[1]
                    print css_link
                    content_2 = requests.get(css_link)
                    tyc_num = re_findall('(font-family: "tyc-num";.*?)\.tyc-num {', str(content_2.text))[0]

                    print url
                    print corp_name
                    print corp_id
                    print phone
                    print email
                    print website
                    print address

                    print juridical_person

                    print juridical_person_url

                    print register_capital

                    print register_time

                    print company_status

                    print business_registration_number

                    print organization_code

                    print uniform_credit_code

                    print enterprise_type

                    print taxpayer_identification_number

                    print industry

                    print business_term

                    print approval_date

                    print registration_authority

                    print registered_address

                    print english_name

                    print scope_of_business

                    print css_link

                    print detag(tyc_num)
                    cursor.execute(
                        'insert into tyc_base_business_info values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                        (
                            url
                            ,
                            corp_name
                            ,
                            corp_id
                            ,
                            phone
                            ,
                            email
                            ,
                            website
                            ,
                            address
                            ,
                            juridical_person
                            ,
                            juridical_person_url
                            ,
                            register_capital
                            ,
                            register_time
                            ,
                            company_status
                            ,
                            business_registration_number
                            ,
                            organization_code
                            ,
                            uniform_credit_code
                            ,
                            enterprise_type
                            ,
                            taxpayer_identification_number
                            ,
                            industry
                            ,
                            business_term
                            ,
                            approval_date
                            ,
                            registration_authority
                            ,
                            registered_address
                            ,
                            english_name
                            ,
                            scope_of_business
                            ,
                            css_link
                            ,
                            detag(tyc_num)
                            ,

                            str(datetime.datetime.now()),
                            str(datetime.datetime.now())[:10]
                        )

                    )
                    conn.commit()
                    print '插入时间 _@_ ' + str(datetime.datetime.now())
                    break


        except Exception, e:
            print str(e)
            print traceback.format_exc()

            break


if __name__ == '__main__':
    proxies = get_proxy()

    conn = MySQLdb.connect(host="localhost", user="root", passwd="root",
                           db="new_tyc",
                           charset="utf8")
    cursor = conn.cursor()
    cursor.execute('truncate table tyc_base_business_info')
    cursor.execute('select corp_url from tyc_prepare_info')
    all_urls = []
    urls = cursor.fetchall()
    for y in range(0, len(urls)):
        all_urls.append(urls[y][0])
    # cursor.execute('truncate table tyc_base_business_info')
    cursor.execute('select corp_url from tyc_base_business_info')
    old_urls = []
    old = cursor.fetchall()
    for y in range(0, len(old)):
        old_urls.append(urls[y][0])
    cursor.close()
    conn.close()

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
            threads.append(threading.Thread(target=get_info, args=(target_urls[start_no + inner_index],)))
        for t in threads:
            t.setDaemon(True)
            t.start()
        t.join()
        start_no += thread_num


        # for x in target_urls:
        #     get_info(x)
