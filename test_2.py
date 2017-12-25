# -*- coding: utf-8 -*-
# @Time         : 2017/12/7 09:41
# @Author       : Huaiz
# @Email        : Apokar@163.com
# @File         : test_2.py
# @Software     : PyCharm Community Edition
# @PROJECT_NAME : new_tyc
import time
import re

import requests

numbers = {1,2,3,4,5,6,7}

def get_odd(num):
    max_error = 5
    num_error = 0
    while True:
        try:
            if num % 2 == 1:
                print num
                time.sleep(2)
                break
            else:
                state = 'not odd'
                print 'error'
                time.sleep(2)
                if state == 'not odd':
                    num_error += 1

                    if num_error == max_error:
                        print '5ci le '
                        break
                    else:
                        continue
            break
        except:
            print 'iii error'
            break


if __name__ == '__main__':
    for num in numbers:
        get_odd(num)