# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:asyn_IO_client_test.py
@time:2021/11/17
"""

from socket import *

s = socket(AF_INET, SOCK_DGRAM)
s.sendto(b'', ('106.15.178.162', 14000))
print(s.recvfrom(128))

s.sendto(b'', ('106.15.178.162', 15000))
print(s.recvfrom(128))