# -*- coding: UTF-8 -*-
"""
@author:wzc
@file:UDP_client.py
@time:2021/11/12
"""
from datetime import time, datetime
from socket import socket, AF_INET, SOCK_DGRAM

s = socket(AF_INET, SOCK_DGRAM)

s.sendto(b'', ('106.15.178.162', 20000))
recv_time, _ = s.recvfrom(8192)
print(_)
recv_time = float(recv_time.decode("utf-8"))
print(recv_time)
times = datetime.fromtimestamp(recv_time)



print(times)
