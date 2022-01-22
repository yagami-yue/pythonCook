# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:thread3.py
@time:2021/12/03
"""
# 通过给线程传递一个Event参数，通过wait，set两个接口来判断线程是否已经启动
# event对象最好只针对一次性的时间，也就是说创建一个时间，让线程等待事件被设置，一旦完成了设置，Event对象就被丢弃
# 尽管可以使用Event对象的clear方法来清除事件，但是要安全地清除事件并等待它可以再次设置这个过程很难同步协调，可能造成事件丢失，死锁
from threading import Thread, Event
import time


def countdown(n, started_evt):
    print('countdown starting')
    started_evt.set()
    while n > 0:
        print('T-minus', n)
        n -= 1
        time.sleep(5)


started_evt = Event()

print('Launching countdown')
t = Thread(target=countdown, args=(10, started_evt))
t.start()

started_evt.wait(timeout=5)   # 让线程阻塞，直到.set()被调用才会唤醒线程开始运行
print('countdown is running')
