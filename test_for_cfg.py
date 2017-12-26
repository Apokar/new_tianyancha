# -*- coding: utf-8 -*-
import MySQLdb
import config
conn = MySQLdb.connect(host=config.server09_host, port=config.server09_port, user=config.server09_user, passwd=config.server09_passwd,
                       db=config.server09_dbname,
                       charset="utf8")
cursor = conn.cursor()

cursor.execute('select corp_name from tyc_base_business_info where corp_url="https://www.tianyancha.com/company/3028303171" ')
data = cursor.fetchall()
print data[0][0]