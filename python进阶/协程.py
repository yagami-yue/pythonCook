# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:协程.py
@time:2021/09/06
"""
def calc_avg():
    """流式计算平均值"""
    total, counter = 0, 0
    avg_value = None
    while True:
        value = yield avg_value
        total, counter = total + value, counter + 1
        avg_value = total / counter


gen = calc_avg()
next(gen)  # 启动携程
print(gen.send(10))
print(gen.send(20))
print(gen.send(30))
print(gen.send(40))


import threading
threading.RLock()