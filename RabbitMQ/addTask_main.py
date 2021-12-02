# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:addTask_main.py
@time:2021/09/26
"""
# addTask_main.py : RUN the AddTask example with
import time

from tasks import add
result = add.delay(10, 30)
print(result, type(result))
while True:
    time.sleep(2)
    if result.successful():
        print(result.result)
        break
