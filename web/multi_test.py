# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:multi_test.py
@time:2021/11/15
"""
from multiprocessing.connection import Client

c = Client(('106.15.178.162', 20000), authkey=b'light')
while True:
    msg = input('输入要发送的内容:')
    if c.closed:
        c.close()
        break
    if not msg:
        break
    c.send(msg)
    try:
        print('结果:', c.recv())
    except EOFError:
        print('connection closed')
        c.close()
        break
